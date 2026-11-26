from unittest.mock import Mock

import pytest

from confluence.__main__ import main


@pytest.mark.parametrize(("expected_version", "updates"), [(None, True), ("7", True), ("6", False)])
def test_update_checks_the_version_used_for_editing(monkeypatch, tmp_path, expected_version, updates):
    api = Mock()
    api.get_content_by_id.return_value = {"version": {"number": 7}, "title": "Page", "space": {"key": "DOC"}, "type": "page"}
    monkeypatch.setattr("confluence.page.update_page.create_api_instance", lambda _args: api)
    xml_file = tmp_path / "page.xml"
    xml_file.write_text("<p>Edited</p>", encoding="utf-8")
    args = ["page", "update", "--page_id", "42", "--xml_file", str(xml_file), "--yes"]
    if expected_version is not None:
        args.extend(["--expected_version", expected_version])

    if updates:
        main(args)
        api.update_content.assert_called_once()
        assert api.update_content.call_args.kwargs["request_body"]["version"]["number"] == 8
    else:
        with pytest.raises(ValueError, match="指定: 6、現在: 7"):
            main(args)
        api.update_content.assert_not_called()
