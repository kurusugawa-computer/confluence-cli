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

    class ContentById:
        class ChildAttachment:
            def __init__(self, session: requests.Session, content_id: str) -> None:
                self.session = session
                self.content_id = content_id

            def get_attachments(self, query_params: Optional[QueryParams]=None) -> dict[str, Any]:
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
