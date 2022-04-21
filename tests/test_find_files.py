import os

import pytest
import pytest_mock
import sublib_cli


class TestFindFilesFunction:

    @pytest.fixture
    def mock_isdir(self, mocker):
        mocker.patch("os.path.isdir", lambda x: True)

    def test_find_files_file(self, mocker):
        mocker.patch("os.path.isfile", lambda x: True)
        files = sublib_cli.find_files("path/to/file.txt")
        assert files == ["path/to/file.txt"]

    def test_find_files_dir(self, mock_isdir, mocker):
        mocker.patch(
            "os.walk",
            lambda x: [[[], [], ["file1.txt", "file2.txt"]], []]
        )
        files = sublib_cli.find_files("path\\to\\dir")
        assert files == ["path\\to\\dir\\file1.txt", "path\\to\\dir\\file2.txt"]

    def test_find_files_dir_empty(self, mock_isdir, mocker):
        mocker.patch(
            "os.walk",
            lambda x: [[[], [], []], []]
        )
        files = sublib_cli.find_files("path\\to\\dir")
        assert files == []
