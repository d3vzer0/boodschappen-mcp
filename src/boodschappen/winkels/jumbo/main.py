import json
from typing import Annotated
from urllib.parse import urlencode

import httpx2
from fastmcp import FastMCP
from pydantic import Field

from .models import SearchProducts, ShoppingListItem

SEARCH_QUERY_HASH = '6d88ecdd5a15ea52cb9c6e1e92f8206b36ac2636521fe66c80a9d89ba7d08453'
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.99; rv:159.0) Gecko/12345123 Firefox/159.9',
    'Content-Type': 'application/json',
    'apollographql-client-name': 'JUMBO_WEB-search',
    'apollographql-client-version': 'master-v40.4.0-web',
}

mcp = FastMCP("Jumbo")


@mcp.tool(description="Zoek producten bij Jumbo")
async def search_product(
        search: Annotated[str, Field(description="Zoekterm voor het product, zoals 'Melk'", min_length=1)],
) -> SearchProducts:
    variables = {
        'input': {
            'searchType': 'KEYWORD',
            'searchTerms': search,
        },
        'shelfTextInput': {'searchType': 'KEYWORD'},
        'withFacetChildren': False,
    }
    params = {
        'variables': json.dumps(variables, separators=(',', ':')),
        'extensions': json.dumps({
            'persistedQuery': {'version': 1, 'sha256Hash': SEARCH_QUERY_HASH},
        }, separators=(',', ':')),
    }
    response = httpx2.get('https://www.jumbo.com/api/graphql', params=params, headers=DEFAULT_HEADERS)
    response.raise_for_status()
    result = response.json()
    return SearchProducts.model_validate(result['data']['searchProducts'])


@mcp.tool(description="Maak een link om producten toe te voegen aan een Jumbo winkelmandje")
async def add_products(
        products: Annotated[list[ShoppingListItem], Field(min_length=1)],
) -> str:
    items = [product.model_dump(mode='json') for product in products]
    return 'https://www.jumbo.com/mandje/?' + urlencode({
        'add': json.dumps(items, separators=(',', ':')),
    })
