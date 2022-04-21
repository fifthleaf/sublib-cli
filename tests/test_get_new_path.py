import pytest
import sublib_cli


class TestGetNewPathFunction:

    @pytest.fixture
    def set_details(self):
        return {"path": "file.txt"}

    def test_get_new_path_mpl(self, set_details):
        path = sublib_cli.get_new_path(set_details, "mpl")
        assert path == "file.txt"

    def test_get_new_path_srt(self, set_details):
        path = sublib_cli.get_new_path(set_details, "srt")
        assert path == "file.srt"

    def test_get_new_path_sub(self, set_details):
        path = sublib_cli.get_new_path(set_details, "sub")
        assert path == "file.sub"

    def test_get_new_path_tmp(self, set_details):
        path = sublib_cli.get_new_path(set_details, "tmp")
        assert path == "file.txt"
