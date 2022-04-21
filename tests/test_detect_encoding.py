import pytest
import pytest_mock
import sublib_cli


class TestDetectEncodingFunction:

    def test_detect_encoding(self, mocker):
        test_data = "Line 01|Line 02".encode("ascii")
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        encoding = sublib_cli.detect_encoding("file.txt")
        assert encoding == "ascii"
