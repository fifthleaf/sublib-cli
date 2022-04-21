import logging

import pytest
import sublib_cli


class TestSetLoggerFunction:

    def test_set_logger_instance(self):
        logger = sublib_cli.set_logger("file.log", logging.INFO)
        assert isinstance(logger, logging.Logger)
