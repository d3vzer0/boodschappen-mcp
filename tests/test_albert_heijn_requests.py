from unittest.mock import Mock

import pytest
from fastmcp import Client, FastMCP
from fastmcp.server import sessions
from fastmcp.server.auth import AccessToken

from boodschappen.winkels.albert_heijn.main import mcp as ah_server
from boodschappen.winkels.albert_heijn.models import SearchProducts
from test_albert_heijn_api import TEST_DATA_DIR, load_json


@pytest.mark.anyio
async def test_search_products(mock_ah_http: Mock, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sessions, "get_access_token",
        lambda: AccessToken(token="test", client_id="test-user", scopes=[]),
    )
    server = FastMCP("Test")
    server.mount(ah_server)

    async with Client(server) as client:
        result = await client.call_tool("search_product", {"search": "melk"})

    expected = SearchProducts.model_validate(load_json(TEST_DATA_DIR / "search.json"))

    assert result.structured_content == expected.model_dump(mode="json")
    assert mock_ah_http.call_count == 2
    token = load_json(TEST_DATA_DIR / "anonymous_token.json")["access_token"]
    assert mock_ah_http.call_args.kwargs["headers"]["Authorization"] == f"Bearer {token}"
