import logging
import builtins

import pytest
import pytest_mock
import sublib
import sublib_cli


class TestWriteFileFunction:

    @pytest.fixture
    def set_details(self):
        return {
            "format": "mpl",
            "path": "file.txt",
            "encoding": "utf-8"
        }

    @pytest.fixture
    def set_subtitle(self, set_details):
        return sublib_cli.get_subtitle(set_details)

    @pytest.fixture
    def set_logger(self):
        return logging.getLogger(__name__)

    def test_write_file(self, set_subtitle, set_details, set_logger, mocker):
        mocker.patch("builtins.open", mocker.mock_open())
        try:
            sublib_cli.write_file(set_subtitle, set_details, "mpl", set_logger)
        except Exception:
            assert False
        else:
            assert True
