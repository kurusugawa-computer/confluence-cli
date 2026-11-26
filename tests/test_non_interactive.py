from unittest.mock import Mock

import pytest

from confluence.__main__ import main

CREDENTIALS = {
    "CONFLUENCE_BASE_URL": "https://example.test/confluence/",
    "CONFLUENCE_USER_NAME": "agent",
    "CONFLUENCE_USER_PASSWORD": "test-password",
}


@pytest.fixture(autouse=True)
def configure_environment(monkeypatch):
    for name, value in CREDENTIALS.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr("builtins.input", Mock(side_effect=AssertionError("unexpected prompt")))
    monkeypatch.setattr("confluence.common.cli.getpass.getpass", Mock(side_effect=AssertionError("unexpected password prompt")))


@pytest.mark.parametrize("missing", CREDENTIALS)
def test_non_interactive_reports_missing_credentials(monkeypatch, capsys, missing):
    monkeypatch.delenv(missing)

    with pytest.raises(SystemExit) as exc_info:
        main(["page", "get_body", "--page_id", "42", "--non_interactive"])

    assert exc_info.value.code == 2
    stderr = capsys.readouterr().err
    assert missing in stderr
    assert CREDENTIALS["CONFLUENCE_USER_PASSWORD"] not in stderr


def test_non_interactive_combines_options_and_environment(monkeypatch):
    api_factory = Mock()
    api_factory.return_value.get_content_by_id.return_value = {
        "id": "42",
        "type": "page",
        "title": "Page",
        "body": {"storage": {"value": "<p>Body</p>"}},
    }
    monkeypatch.setattr("confluence.common.cli.Api", api_factory)

    main(["page", "get_body", "--page_id", "42", "--non_interactive", "--confluence_user_name", "override"])

    api_factory.assert_called_once_with("override", "test-password", "https://example.test/confluence")


def test_non_interactive_update_requires_yes(monkeypatch, tmp_path, capsys):
    api = Mock()
    api.get_content_by_id.return_value = {"title": "Page", "space": {"key": "DOC"}, "version": {"number": 7}}
    monkeypatch.setattr("confluence.page.update_page.create_api_instance", lambda _args: api)
    xml_file = tmp_path / "page.xml"
    xml_file.write_text("<p>Edited</p>", encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        main(["page", "update", "--page_id", "42", "--xml_file", str(xml_file), "--non_interactive"])

    assert exc_info.value.code == 2
    assert "--yes" in capsys.readouterr().err
    api.update_content.assert_not_called()


def test_non_interactive_attachment_delete_exits_without_request(monkeypatch):
    api_factory = Mock()
    monkeypatch.setattr("confluence.attachment.delete_attachment.create_api_instance", api_factory)
    with pytest.raises(SystemExit) as exc_info:
        main(["attachment", "delete", "--page_id", "42", "--non_interactive"])

    assert exc_info.value.code == 2
    api_factory.assert_not_called()
