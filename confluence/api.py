from typing import Any, Optional

import requests
from requests_toolbelt import sessions

QueryParams = dict[str, Any]


class Api:
    """

    Args:
        base_url: example: `https://kurusugawa.jp/confluence`

    """

    def __init__(self, username: str, password: str, base_url: str):
        self.base_url = base_url
        self.session = sessions.BaseUrlSession(base_url=base_url + "/rest/api/")
        self.session.auth = (username, password)

        self.content = self.Content(self.session)

    class Content:
        def __init__(self, session: requests.Session) -> None:
            self.session = session

        def get_content(self, query_params: Optional[QueryParams] = None):
            return self.session.get(f"content", params=query_params)

        def get_content_by_id(self, id: str, query_params: Optional[QueryParams] = None):
            response = self.session.get(f"content/{id}", params=query_params)
            return response

        def delete(self, id: str, query_params: Optional[QueryParams] = None):
            response = self.session.delete(f"content/{id}", params=query_params)
            return response

        def get_history(self, id: str, query_params: Optional[QueryParams] = None):
            response = self.session.get(f"content/{id}/history", params=query_params)
            return response.json()

        def search(self, query_params: Optional[QueryParams] = None):
            response = self.session.get(f"content/search", params=query_params)
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

        def __init__(self, session: requests.Session, content_id: str):
            self.content_id = content_id
            self.child_attachment = Api.ContentById.ChildAttachment(session, content_id)

    def content_by_id(self, content_id: str) -> ContentById:
        return Api.ContentById(self.session, content_id)
