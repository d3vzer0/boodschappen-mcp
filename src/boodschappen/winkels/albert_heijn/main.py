import asyncio

import httpx2
from fastmcp.dependencies import Depends
from fastmcp.server.server import StateValue
from fastmcp.server.sessions import UserSession
from key_value.aio.adapters.pydantic import PydanticAdapter
from key_value.aio.stores.memory import MemoryStore

from boodschappen.main import mcp
from .models import AccessToken, SearchProducts

DEFAULT_CLIENT_ID = 'appie'
DEFAULT_HEADERS = {
    'User-Agent': 'Appie/9.28',
    'x-client-version': '9.28',
    'x-application': 'AHWEBSHOP',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


async def get_token(session: UserSession) -> AccessToken:
    facts = await session.get("ah_session", default=None)
    if facts is not None:
        return AccessToken.model_validate(facts)

    data = {
        "clientId": DEFAULT_CLIENT_ID
    }
    get_response = httpx2.post('https://api.ah.nl/mobile-auth/v1/auth/token/anonymous', headers=DEFAULT_HEADERS,
                               json=data)
    get_response.raise_for_status()
    token = AccessToken(**get_response.json())
    await session.set("ah_session", token.model_dump(mode="json"))
    return token


@mcp.tool()
async def search_product(search: str, user_token=Depends(get_token)) -> SearchProducts:
    params = {'query': search, 'page': 0, 'size': 30, 'sortOn': 'RELEVANCE'}
    headers = {**DEFAULT_HEADERS, 'Authorization': f'Bearer {user_token.access_token}'}
    get_response = httpx2.get('https://api.ah.nl/mobile-services/product/search/v2',
                              params=params, headers=headers)
    get_response.raise_for_status()
    return SearchProducts(**get_response.json())


async def main():
    store = PydanticAdapter(
        key_value=MemoryStore(),
        pydantic_model=StateValue,
    )
    session = UserSession(store=store, principal='local-test-user', session_id='local-test-session')

    token = await get_token(session)
    zoek_product = await search_product(search='melk', user_token=token)
    print(zoek_product)


if __name__ == '__main__':
    asyncio.run(main())
