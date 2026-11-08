from functools import partial
from typing import Any
from unittest.mock import Mock
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient

from test_albert_heijn_api import mock_ah_api, mock_ah_service  # noqa: F401


@pytest.fixture
def mock_ah_http(mock_ah_service: TestClient, monkeypatch: pytest.MonkeyPatch) -> Mock:
    from boodschappen.winkels.albert_heijn import main as ah

    def send(method: str, url: str, **kwargs: Any):
        parsed = urlsplit(url)
        assert (parsed.scheme, parsed.netloc) == ("https", "api.ah.nl"), (
            f"Unexpected external request: {url}"
        )
        return mock_ah_service.request(method, url, **kwargs)

    request = Mock(side_effect=send)
    monkeypatch.setattr(ah.httpx2, "get", partial(request, "GET"))
    monkeypatch.setattr(ah.httpx2, "post", partial(request, "POST"))
    return request
