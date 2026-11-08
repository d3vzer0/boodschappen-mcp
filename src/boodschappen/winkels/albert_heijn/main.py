from typing import Annotated

import httpx2
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.server.sessions import UserSession
from pydantic import Field

from .models import AccessToken, SearchProducts

DEFAULT_CLIENT_ID = 'appie'
DEFAULT_HEADERS = {
    'User-Agent': 'Appie/9.28',
    'x-client-version': '9.28',
    'x-application': 'AHWEBSHOP',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

mcp = FastMCP("Albert Heijn")


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


@mcp.tool(description="Zoek producten bij de Albert Heijn")
async def search_product(
        search: Annotated[str, Field(description="Zoekterm voor het product, zoals 'Melk'", min_length=1)],
        user_token=Depends(get_token)) -> SearchProducts:
    params = {'query': search, 'page': 0, 'size': 30, 'sortOn': 'RELEVANCE'}
    headers = {**DEFAULT_HEADERS, 'Authorization': f'Bearer {user_token.access_token}'}
    get_response = httpx2.get('https://api.ah.nl/mobile-services/product/search/v2',
                              params=params, headers=headers)
    get_response.raise_for_status()
    return SearchProducts(**get_response.json())
