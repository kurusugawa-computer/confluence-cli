from __future__ import annotations

from typing import Any

import pytest
from requests import HTTPError, Response

from confluence.common.api import Api, ResponseByteBoundExceeded, TransportPolicy


def _json_response(body: bytes = b'{"id":"123456"}') -> Response:
    response = Response()
    response.status_code = 200
    response.url = "https://confluence.example.test/confluence/rest/api/content/123456"
    response.headers["Content-Type"] = "application/json"
    response._content = body  # noqa: SLF001
    response._content_consumed = True  # noqa: SLF001
    return response


def test_transport_policy_is_applied_to_protocol_request(monkeypatch: pytest.MonkeyPatch) -> None:
    api = Api(
        "reader",
        "secret",
        "https://confluence.example.test/confluence",
        transport_policy=TransportPolicy(timeout_second=7, follow_redirects=False, response_byte_bound=1024),
    )
    request_argument: dict[str, Any] = {}

    def fake_request(method: str, url: str, **kwargs: Any) -> Response:  # noqa: ANN401
        request_argument.update(method=method, url=url, **kwargs)
        return _json_response()

    monkeypatch.setattr(api.session, "request", fake_request)

    result = api.get_content_by_id("123456", query_params={"expand": "space,body.storage"})

    assert result == {"id": "123456"}
    assert request_argument == {
        "method": "get",
        "url": "content/123456",
        "params": {"expand": "space,body.storage"},
        "data": None,
        "headers": None,
        "timeout": 7,
        "allow_redirects": False,
        "stream": True,
    }


@pytest.mark.parametrize(
    ("policy", "message"),
    [
        (TransportPolicy(timeout_second=1, response_byte_bound=4), "byte bound"),
    ],
)
def test_response_byte_bound_is_enforced(
    monkeypatch: pytest.MonkeyPatch,
    policy: TransportPolicy,
    message: str,
) -> None:
    api = Api("reader", "secret", "https://confluence.example.test/confluence", transport_policy=policy)
    response = _json_response(b"12345")
    monkeypatch.setattr(api.session, "request", lambda *_args, **_kwargs: response)

    with pytest.raises(ResponseByteBoundExceeded, match=message):
        api.get_content_by_id("123456")


def test_streamed_error_response_is_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    api = Api(
        "reader",
        "secret",
        "https://confluence.example.test/confluence",
        transport_policy=TransportPolicy(response_byte_bound=1024),
    )
    response = _json_response()
    response.status_code = 500
    closed = False

    def close() -> None:
        nonlocal closed
        closed = True

    monkeypatch.setattr(response, "close", close)
    monkeypatch.setattr(api.session, "request", lambda *_args, **_kwargs: response)

    with pytest.raises(HTTPError):
        api.get_content_by_id("123456")

    assert closed is True


def test_streamed_success_response_is_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    api = Api(
        "reader",
        "secret",
        "https://confluence.example.test/confluence",
        transport_policy=TransportPolicy(response_byte_bound=1024),
    )
    response = _json_response()
    closed = False

    def close() -> None:
        nonlocal closed
        closed = True

    monkeypatch.setattr(response, "close", close)
    monkeypatch.setattr(api.session, "request", lambda *_args, **_kwargs: response)

    assert api.get_content_by_id("123456") == {"id": "123456"}
    assert closed is True


def test_transport_policy_rejects_non_positive_bounds() -> None:
    with pytest.raises(ValueError, match="timeout_second"):
        TransportPolicy(timeout_second=0)
    with pytest.raises(ValueError, match="response_byte_bound"):
        TransportPolicy(response_byte_bound=0)


def test_search_uses_common_transport_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    api = Api("reader", "secret", "https://confluence.example.test/confluence")
    request_argument: dict[str, Any] = {}

    def fake_request(method: str, url: str, **kwargs: Any) -> Response:  # noqa: ANN401
        request_argument.update(method=method, url=url, **kwargs)
        return _json_response(b"{}")

    monkeypatch.setattr(api.session, "request", fake_request)

    assert api.search_content(query_params={"cql": "type=page"}) == {}
    assert request_argument["timeout"] == 30
    assert request_argument["allow_redirects"] is True
