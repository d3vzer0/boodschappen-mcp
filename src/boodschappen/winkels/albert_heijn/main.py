from time import monotonic
from typing import Annotated

import httpx2
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from .models import AccessToken, SearchProducts, ShoppingListItems

DEFAULT_CLIENT_ID = 'appie'
DEFAULT_HEADERS = {
    'User-Agent': 'Appie/9.28',
    'x-client-version': '9.28',
    'x-application': 'AHWEBSHOP',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

mcp = FastMCP("Albert Heijn")
_access_token: AccessToken | None = None
_token_expires_at: float = 0


async def get_token() -> AccessToken:
    global _access_token, _token_expires_at

    now = monotonic()
    if _access_token is not None and now < _token_expires_at:
        return _access_token

    data = {
        "clientId": DEFAULT_CLIENT_ID
    }
    get_response = httpx2.post('https://api.ah.nl/mobile-auth/v1/auth/token/anonymous', headers=DEFAULT_HEADERS,
                               json=data)
    get_response.raise_for_status()
    token = AccessToken(**get_response.json())
    _access_token = token
    _token_expires_at = now + token.expires_in
    return token


@mcp.tool(description="Zoek producten bij de Albert Heijn")
async def search_product(
        search: Annotated[str, Field(description="Zoekterm voor het product, zoals 'Melk'", min_length=1)],
        user_token: AccessToken = Depends(get_token),
) -> SearchProducts:
    params = {'query': search, 'page': 0, 'size': 30, 'sortOn': 'RELEVANCE'}
    headers = {**DEFAULT_HEADERS, 'Authorization': f'Bearer {user_token.access_token}'}
    get_response = httpx2.get('https://api.ah.nl/mobile-services/product/search/v2',
                              params=params, headers=headers)
    get_response.raise_for_status()
    return SearchProducts(**get_response.json())


@mcp.tool(description="Maak een Albert Heijn boodschappenlijst-link")
async def add_products(
        products: Annotated[list[ShoppingListItems], Field(min_length=1)],
) -> str:
    return "https://www.ah.nl/mijnlijst/add-multiple?" + "&".join(
        f"p={int(product.prod_id)}:{product.count}" for product in products
    )
