from __future__ import annotations

import pytest

from confluence.__main__ import main
from confluence.__version__ import __version__


def test__command__version_option(capsys):
    with pytest.raises(SystemExit):
        main(
            [
                "--version",
            ]
        )
        captured = capsys.readouterr()
        assert captured.out == f"confluence {__version__}\n"
