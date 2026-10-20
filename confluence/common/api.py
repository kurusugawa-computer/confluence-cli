from __future__ import annotations

import copy
import logging
import mimetypes
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from requests import HTTPError, Response
from requests_toolbelt import sessions

logger = logging.getLogger(__name__)

QueryParams = dict[str, Any]
RequestBody = dict[str, Any]


class ResponseByteBoundExceeded(RuntimeError):
    """Response body が configured byte bound を超えたことを表す。"""


@dataclass(frozen=True)
class TransportPolicy:
    """Confluence HTTP transport に共通する bounded execution policy。"""

    timeout_second: float = 30
    follow_redirects: bool = True
    response_byte_bound: int | None = None

    def __post_init__(self) -> None:
        if self.timeout_second <= 0:
            raise ValueError("timeout_secondは0より大きい値にしてください。")
        if self.response_byte_bound is not None and self.response_byte_bound < 1:
            raise ValueError("response_byte_boundは1以上の値にしてください。")


class Api:
    """
    https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/

    Args:
        base_url: example: `https://kurusugawa.jp/confluence`
        delay_second: APIを連続で実行する際、何秒以上間隔を空けるか。Confluenceに負荷をかけすぎないようにするため、少なくとも0.3秒以上にすること。
        transport_policy: timeout, redirect, response size の共通policy。

    """

    def __init__(
        self,
        username: str,
        password: str,
        base_url: str,
        delay_second: float = 1,
        *,
        transport_policy: TransportPolicy | None = None,
    ) -> None:
        if delay_second < 0.3:
            raise RuntimeError(f"引数'delay_second'は0.3以上にしてください。 :: {delay_second=}")

        self.base_url = base_url
        self.session = sessions.BaseUrlSession(base_url=base_url + "/rest/api/")
        self.session.auth = (username, password)

        self.delay_second = delay_second
        self.transport_policy = transport_policy or TransportPolicy()
        self._previous_timestamp: float = 0

    @staticmethod
    def mask_sensitive_info_of_headers(headers: dict[str, str] | None) -> dict[str, str] | None:
        """HTTP headerのセンシティブな情報を`***`でマスクする"""
        if headers is None:
            return None
        new_headers = copy.deepcopy(headers)

        if "Authorization" in new_headers:
            new_headers["Authorization"] = "***"

        return new_headers

    def _request(
        self,
        http_method: str,
        url: str,
        *,
        headers: dict[str, Any] | None = None,
        params: QueryParams | None = None,
        data: Any = None,  # noqa: ANN401
        **kwargs,
    ) -> Response:
        """
        HTTP Requestを投げて、Responseを返す。

        Args:
            http_method:
            url:
            headers:
            params:
            data:
            kwargs:

        Returns:
            HTTP response。response byte bound が指定されている場合は、bodyをbound内で読み込んだresponseを返す。

        Raises:
            HTTPError: HTTP status がerrorを表す場合。
            ResponseByteBoundExceeded: Response body がconfigured byte boundを超えた場合。

        """
        now = time.time()
        diff_time = now - self._previous_timestamp
        if diff_time < self.delay_second:
            time.sleep(self.delay_second - diff_time)

        kwargs.setdefault("timeout", self.transport_policy.timeout_second)
        kwargs.setdefault("allow_redirects", self.transport_policy.follow_redirects)
        if self.transport_policy.response_byte_bound is not None:
            kwargs["stream"] = True

        response = self.session.request(http_method, url, params=params, data=data, headers=headers, **kwargs)
        self._previous_timestamp = time.time()

        try:
            response.raise_for_status()
        except HTTPError:
            response.close()
            raise
        response_content = self._response_content(response)

        # `kwargs["json"]` は credential やcontentを含みうるため、arbitrary JSON payloadは意図的にlogへ複製しない。
        logger.debug(
            "Sent a request :: %s",
            {
                "requests": {
                    "http_method": http_method,
                    "url": url,
                    "query_params": params,
                    "request_body_json": data,
                    "headers": self.mask_sensitive_info_of_headers(headers),
                },
                "response": {
                    "status_code": response.status_code,
                    "content_length": len(response_content),
                },
            },
        )
        return response

    def _response_content(self, response: Response) -> bytes:
        byte_bound = self.transport_policy.response_byte_bound
        if byte_bound is None:
            return response.content

        body = bytearray()
        try:
            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                try:
                    if int(content_length) > byte_bound:
                        raise ResponseByteBoundExceeded(f"Response bodyがbyte boundを超えました。 :: {byte_bound=}")
                except ValueError:
                    pass

            for chunk in response.iter_content(chunk_size=min(64 * 1024, byte_bound + 1)):
                body.extend(chunk)
                if len(body) > byte_bound:
                    raise ResponseByteBoundExceeded(f"Response bodyがbyte boundを超えました。 :: {byte_bound=}")
        finally:
            response.close()

        response_content = bytes(body)
        response._content = response_content
        cast(Any, response)._content_consumed = True
        return response_content

    def get_attachments(self, content_id: str, *, query_params: QueryParams | None = None) -> dict[str, Any]:
        url = f"content/{content_id}/child/attachment"
        return self._request("get", url, params=query_params).json()

    def create_attachment(
        self, content_id: str, file: Path, *, query_params: QueryParams | None = None, mime_type: str | None = None
    ) -> dict[str, Any]:
        """
        Args:
            mime_type: mimetypes.guess_type()で自動判定でMIMEタイプを取得できないときに、この値をMIMEタイプにします。
        """
        headers = {"X-Atlassian-Token": "nocheck"}
        url = f"content/{content_id}/child/attachment"
        new_mime_type, _ = mimetypes.guess_type(file)
        if new_mime_type is None:
            new_mime_type = mime_type

        with file.open("rb") as f:
            files = {"file": (file.name, f, new_mime_type)}
            return self._request("post", url, params=query_params, files=files, headers=headers).json()

    def get_content(self, *, query_params: QueryParams | None = None) -> list[dict[str, Any]]:
        """
        Returns a paginated list of Content.

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getContent
        """
        return self._request("get", "content", params=query_params).json()

    def get_content_by_id(self, content_id: str, *, query_params: QueryParams | None = None) -> dict[str, Any]:
        """
        Returns a piece of Content.

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getContentById
        """
        return self._request("get", f"content/{content_id}", params=query_params).json()

    def update_content(self, content_id: str, *, query_params: QueryParams | None = None, request_body: RequestBody | None = None) -> dict[str, Any]:
        """
        Updates a piece of Content, including changes to content status

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-update
        """
        return self._request("put", f"content/{content_id}", params=query_params, json=request_body).json()

    def delete_content(self, content_id: str, *, query_params: QueryParams | None = None) -> None:
        """
        Trashes or purges a piece of Content, based on its {@link ContentType} and {@link ContentStatus}.

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-delete

        Notes:
            クエリパラーメタ`status`に`trashed`を指定すると400エラーが発生した。
        """
        self._request("delete", f"content/{content_id}", params=query_params)

    def get_content_history(self, content_id: str, *, query_params: QueryParams | None = None):  # noqa: ANN201
        """Returns the history of a particular piece of content

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getHistory
        """
        return self._request("get", f"content/{content_id}/history", params=query_params).json()

    def search_content(self, *, query_params: QueryParams | None = None) -> dict[str, Any]:
        """
        Fetch a list of content using the Confluence Query Language (CQL)

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-search
        """
        return self._request("get", "content/search", params=query_params).json()
