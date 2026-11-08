import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

TEST_DATA_DIR = Path(__file__).parent / "test_data" / "albert_heijn"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def mock_ah_api() -> FastAPI:
    app = FastAPI()

    @app.post("/mobile-auth/v1/auth/token/anonymous")
    async def anonymous_token() -> dict[str, Any]:
        return load_json(TEST_DATA_DIR / "anonymous_token.json")

    @app.get("/mobile-services/product/search/v2")
    async def search(query: str, sortOn: str = "RELEVANCE") -> dict:
        return load_json(TEST_DATA_DIR / 'search.json')

    return app


@pytest.fixture
def mock_ah_service(mock_ah_api: FastAPI) -> Iterator[TestClient]:
    with TestClient(mock_ah_api, base_url="https://api.ah.nl") as client:
        yield client


def test_anonymous_token(mock_ah_service: TestClient) -> None:
    response = mock_ah_service.post("/mobile-auth/v1/auth/token/anonymous", json={"clientId": "appie"})

    assert response.status_code == 200
    assert response.json() == load_json(TEST_DATA_DIR / "anonymous_token.json")


def test_search_returns_sample(mock_ah_service: TestClient) -> None:
    response = mock_ah_service.get(
        "/mobile-services/product/search/v2", params={"query": "ice tea", "sortOn": "RELEVANCE"}
    )

    assert response.status_code == 200
    assert response.json() == load_json(TEST_DATA_DIR / 'search.json')
