import json
from unittest.mock import Mock

import pytest

from confluence.__main__ import main
from confluence.common.cli import create_api_instance


@pytest.fixture
def page_update(monkeypatch, tmp_path):
    api = Mock(base_url="https://example.test/confluence")
    api.get_content_by_id.return_value = {
        "version": {"number": 7},
        "title": "Page",
        "space": {"key": "DOC"},
        "type": "page",
        "body": {"storage": {"value": "<p>Old</p>"}},
    }
    api.update_content.return_value = {"version": {"number": 8}}
    monkeypatch.setattr("confluence.page.update_page.create_api_instance", lambda _args: api)
    xml_file = tmp_path / "page.xml"
    xml_file.write_text("<p>Edited</p>", encoding="utf-8")
    return api, ["page", "update", "--page_id", "42", "--xml_file", str(xml_file)]


@pytest.mark.parametrize("as_json", [False, True])
def test_dry_run_has_diff_and_does_not_update(page_update, capsys, monkeypatch, as_json):
    api, args = page_update
    monkeypatch.setattr("builtins.input", Mock(side_effect=AssertionError("unexpected prompt")))

    main([*args, "--dry_run", *(["--json"] if as_json else [])])

    api.update_content.assert_not_called()
    output = capsys.readouterr().out
    if as_json:
        preview = json.loads(output)
        assert preview["status"] == "preview"
        assert preview["version"] == 7
        assert preview["page_id"] == "42"
        assert preview["url"] == "https://example.test/confluence/pages/viewpage.action?pageId=42"
        output = preview["diff"]
    assert "-<p>Old</p>\n" in output
    assert "+<p>Edited</p>\n" in output


@pytest.mark.parametrize(("answer", "status", "version"), [("y", "updated", 8), ("n", "cancelled", 7)])
def test_update_json_keeps_confirmation_out_of_stdout(page_update, capsys, monkeypatch, answer, status, version):
    api, args = page_update
    monkeypatch.setattr("builtins.input", lambda: answer)

    main([*args, "--json"])

    output = capsys.readouterr()
    assert json.loads(output.out) == {
        "page_id": "42",
        "title": "Page",
        "url": "https://example.test/confluence/pages/viewpage.action?pageId=42",
        "version": version,
        "status": status,
    }
    assert "[y/n]" in output.err
    assert api.update_content.call_count == (1 if answer == "y" else 0)


def test_json_keeps_credential_prompts_out_of_stdout(page_update, capsys, monkeypatch):
    api, args = page_update
    monkeypatch.setattr("confluence.page.update_page.create_api_instance", create_api_instance)
    monkeypatch.setattr("confluence.common.cli.Api", Mock(return_value=api))
    monkeypatch.delenv("CONFLUENCE_BASE_URL", raising=False)
    monkeypatch.delenv("CONFLUENCE_USER_NAME", raising=False)
    replies = iter(["https://example.test/confluence", "agent"])
    monkeypatch.setattr("builtins.input", lambda: next(replies))
    monkeypatch.setattr("confluence.common.cli.getpass.getpass", Mock(return_value="test-password"))

    main([*args, "--dry_run", "--json"])

    output = capsys.readouterr()
    assert json.loads(output.out)["status"] == "preview"
    assert "ConfluenceのURL" in output.err
    assert "Confluenceのユーザー名" in output.err
