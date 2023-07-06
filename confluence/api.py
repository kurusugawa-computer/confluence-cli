import functools
import logging
from pathlib import Path
from typing import Any, Optional

import backoff
import requests
from requests_toolbelt import sessions

logger = logging.getLogger(__name__)

QueryParams = dict[str, Any]


def my_backoff(function):
    """
    リトライが必要な場合はリトライする
    """

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        def should_retry(e) -> bool:
            """
            リトライするかどうか
            status codeが5xxのときまたはToo many Requests(429)のときはリトライする。
            ただし500はリトライしない
            https://requests.kennethreitz.org/en/master/user/quickstart/#errors-and-exceptions

            Args:
                e: exception

            Returns:
                True: give up(リトライしない), False: リトライする

            """
            if isinstance(e, requests.exceptions.HTTPError):
                if e.response is None:
                    return True

                # status_codeの範囲は4XX ~ 5XX
                status_code = e.response.status_code

                if status_code == requests.codes.too_many_requests:
                    return False
                elif 400 <= status_code < 500:
                    return True
                elif 500 <= status_code < 600:
                    return False

            return False

        return backoff.on_exception(
            backoff.expo,
            (requests.exceptions.RequestException, ConnectionError),
            jitter=backoff.full_jitter,
            max_time=300,
            giveup=should_retry,
            logger=logger,
        )(function)(*args, **kwargs)

    return wrapped


class Api:
    """
    https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/

    Args:
        base_url: example: `https://kurusugawa.jp/confluence`

    """

    def __init__(self, username: str, password: str, base_url: str) -> None:
        self.base_url = base_url
        self.session = sessions.BaseUrlSession(base_url=base_url + "/rest/api/")
        self.session.auth = (username, password)

        self.content = self.Content(self.session)

    class Content:
        def __init__(self, session: requests.Session) -> None:
            self.session = session

        @my_backoff
        def get_content(self, query_params: Optional[QueryParams] = None) -> list[dict[str, Any]]:
            """
            Returns a paginated list of Content.

            https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getContent
            """
            return self.session.get("content", params=query_params)

        @my_backoff
        def get_content_by_id(self, id: str, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
            """
            Returns a piece of Content.

            https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-getContentById
            """
            response = self.session.get(f"content/{id}", params=query_params)
            return response

        @my_backoff
        def delete(self, id: str, query_params: Optional[QueryParams] = None) -> None:
            """
            Trashes or purges a piece of Content, based on its {@link ContentType} and {@link ContentStatus}.

            https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-delete
            """

            response = self.session.delete(f"content/{id}", params=query_params)
            return response

        @my_backoff
        def get_history(self, id: str, query_params: Optional[QueryParams] = None):
            """Returns the history of a particular piece of content

            https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-delete
            """
            response = self.session.get(f"content/{id}/history", params=query_params)
            return response.json()

        @my_backoff
        def search(self, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
            """
            Fetch a list of content using the Confluence Query Language (CQL)

            https://docs.atlassian.com/ConfluenceServer/rest/6.15.7/#api/content-search
            """
            response = self.session.get("content/search", params=query_params)
            return response.json()

    class ContentById:
        class ChildAttachment:
            def __init__(self, session: requests.Session, content_id: str) -> None:
                self.session = session
                self.content_id = content_id

            def get_attachments(self, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
                response = self.session.get(f"content/{self.content_id}/child/attachment", params=query_params)
                print(f"{self.session=}")
                print(f"{response.request.url=}, {response.status_code=}")
                print(f"{response.text=}")
                return response.json()

            def create_attachment(self, file: Path, query_params: Optional[QueryParams] = None) -> dict[str, Any]:
                headers = {"X-Atlassian-Token": "nocheck"}
                with file.open("rb") as f:
                    files = {"file": f}
                    response = self.session.post(f"content/{self.content_id}/child/attachment", params=query_params, files=files, headers=headers)
                response.raise_for_status()
                return response.json()

        def __init__(self, session: requests.Session, content_id: str) -> None:
            self.content_id = content_id
            self.child_attachment = Api.ContentById.ChildAttachment(session, content_id)

    def content_by_id(self, content_id: str) -> ContentById:
        return Api.ContentById(self.session, content_id)
