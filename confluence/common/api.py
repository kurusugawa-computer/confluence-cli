from __future__ import annotations

import logging
import mimetypes
import time
from pathlib import Path
from typing import Any, Optional

from requests_toolbelt import sessions

logger = logging.getLogger(__name__)

QueryParams = dict[str, Any]
RequestBody = dict[str, Any]


class Api:
    """
    https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/

    Args:
        base_url: example: `https://kurusugawa.jp/confluence`
        delay_second: APIを連続で実行する際、何秒以上間隔を空けるか。Confluenceに負荷をかけすぎないようにするため、少なくとも0.3秒以上にすること。

    """

    def __init__(self, username: str, password: str, base_url: str, delay_second: float = 1) -> None:
        if delay_second < 0.3:
            raise RuntimeError(f"引数'delay_second'は0.3以上にしてください。 :: {delay_second=}")

        self.base_url = base_url
        self.session = sessions.BaseUrlSession(base_url=base_url + "/rest/api/")
        self.session.auth = (username, password)

        self.delay_second = delay_second
        self._previous_timestamp: float = 0

    def _request(
        self,
        http_method: str,
        url: str,
        *,
        headers: Optional[dict[str, Any]] = None,
        params: Optional[QueryParams] = None,
        data: Any = None,  # noqa: ANN401
        **kwargs,
    ) -> Any:  # noqa: ANN401
        """
        HTTP Requestを投げて、Responseを返す。

        Args:
            http_method:
            url_path:
            query_params:
            header_params:
            body:
            log_response_with_error: HTTP Errorが発生したときにレスポンスの中身をログに出力するか否か

        Returns:
            responseの中身。content_typeにより型が変わる。
            application/jsonならdict型, text/*ならばstr型, それ以外ならばbite型。

        """
        now = time.time()
        diff_time = now - self._previous_timestamp
        if diff_time < self.delay_second:
            time.sleep(self.delay_second - diff_time)

        response = self.session.request(http_method, url, params=params, data=data, headers=headers, **kwargs)
        self._previous_timestamp = time.time()

        logger.debug(
            "Sent a request :: %s",
            {
                "requests": {
                    "http_method": http_method,
                    "url": url,
                    "query_params": params,
                    "request_body_json": data,
                    "headers": response.request.headers,
                },
                "response": {
                    "status_code": response.status_code,
                    "content_length": len(response.content),
                },
            },
        )
        response.raise_for_status()
        return response

    def get_attachments(self, content_id: str, *, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
        url = f"content/{content_id}/child/attachment"
        return self._request("get", url, params=query_params).json()

    def create_attachment(
        self, content_id: str, file: Path, *, query_params: Optional[QueryParams] = None, mime_type: Optional[str] = None
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

    def get_content(self, *, query_params: Optional[QueryParams] = None) -> list[dict[str, Any]]:
        """
        Returns a paginated list of Content.

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getContent
        """
        return self._request("get", "content", params=query_params).json()

    def get_content_by_id(self, content_id: str, *, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
        """
        Returns a piece of Content.

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getContentById
        """
        return self._request("get", f"content/{content_id}", params=query_params).json()

    def update_content(
        self, content_id: str, *, query_params: Optional[QueryParams] = None, request_body: Optional[RequestBody] = None
    ) -> dict[str, Any]:
        """
        Updates a piece of Content, including changes to content status

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-update
        """
        headers = {"Content-Type": "application/json", "X-Atlassian-Token": "nocheck"}
        return self._request("put", f"content/{content_id}", headers=headers, params=query_params, data=request_body).json()

    def delete_content(self, content_id: str, *, query_params: Optional[QueryParams] = None) -> None:
        """
        Trashes or purges a piece of Content, based on its {@link ContentType} and {@link ContentStatus}.

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-delete

        Notes:
            クエリパラーメタ`status`に`trashed`を指定すると400エラーが発生した。
        """
        self._request("delete", f"content/{content_id}", params=query_params)

    def get_content_history(self, content_id: str, *, query_params: Optional[QueryParams] = None):
        """Returns the history of a particular piece of content

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getHistory
        """
        return self._request("get", f"content/{content_id}/history", params=query_params).json()

    def search_content(self, *, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
        """
        Fetch a list of content using the Confluence Query Language (CQL)

        https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-search
        """
        response = self.session.get("content/search", params=query_params)
        return response.json()
