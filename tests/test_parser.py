import os
import sys

import pytest
import sublib_cli


class TestParserFunction:

    @pytest.fixture
    def set_argv(self):
        return [sys.argv[0]]

    def test_parser_convert_mpl_log_off(self, set_argv):
        sys.argv = set_argv
        sys.argv.extend(["convert", "data/subtitle.txt", "mpl"])
        arguments = sublib_cli.parser()
        assert arguments.command == "convert"
        assert arguments.path == "data/subtitle.txt"
        assert arguments.form == "mpl"
        assert arguments.log is None

    def test_parser_convert_mpl_log_on_file(self, set_argv):
        sys.argv = set_argv
        sys.argv.extend(["convert", "data/subtitle.txt", "mpl", "-l", "file.log"])
        arguments = sublib_cli.parser()
        assert arguments.command == "convert"
        assert arguments.path == "data/subtitle.txt"
        assert arguments.form == "mpl"
        assert arguments.log == "file.log"

    def test_parser_convert_mpl_log_on_default(self, set_argv):
        sys.argv = set_argv
        sys.argv.extend(["convert", "data/subtitle.txt", "mpl", "-l"])
        arguments = sublib_cli.parser()
        assert arguments.command == "convert"
        assert arguments.path == "data/subtitle.txt"
        assert arguments.form == "mpl"
        logfile = os.path.dirname(sublib_cli.__file__)
        logfile = os.path.join(logfile, os.path.basename(arguments.log))
        assert arguments.log == logfile
