import os
import timeit
import logging

import pytest
import pytest_mock
import sublib_cli


class TestEndFunction:

    @pytest.fixture
    def mock_getsize(self, mocker):
        mocker.patch("os.remove", lambda x: True)
        mocker.patch("os.path.getsize", lambda x: True)

    @pytest.fixture
    def set_timer(self):
        return timeit.default_timer()

    @pytest.fixture
    def set_logger(self):
        return logging.getLogger(__name__)

    def test_end(self, set_timer, set_logger, mock_getsize):
        try:
            sublib_cli.end(set_logger, "file.txt", set_timer)
        except Exception:
            assert False
        else:
            assert True
