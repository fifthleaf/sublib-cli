import unittest as ut
from unittest.mock import patch, mock_open
import datetime
import sublib as sbl


class DetectTest(ut.TestCase):

    def test_mpl(self):
        test_data = "[601][631] Line 01|Line 02\n[633][654] Line 03|Line 04\n[656][668] Line 04\n"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual(False, sbl.detect(mock_file, "utf-8"))

    def test_srt(self):
        test_data = "1\n00:01:00,060 --> 00:01:03,105\nLine 01\nLine 02\n\n2\n00:01:03,272 --> 00:01:05,440\nLine 03\nLine 04\n\n3\n00:01:05,607 --> 00:01:06,775\nLine 04\n\n"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual(False, sbl.detect(mock_file, "utf-8"))

    def test_sub(self):
        test_data = "{1440}{1513}Line 01|Line 02\n{1517}{1569}Line 03|Line 04\n{1573}{1601}Line 04\n"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual(False, sbl.detect(mock_file, "utf-8"))

    def test_tmp(self):
        test_data = "00:01:00:Line 01|Line 02\n00:01:03:Line 03|Line 04\n00:01:05:Line 04"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual(False, sbl.detect(mock_file, "utf-8"))

    def test_false(self):
        test_data = "Line 01\nLine 02\nLine 03"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertEqual(False, sbl.detect(mock_file, "utf-8"))


class MPlayer2Test(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60, microseconds=100000), datetime.timedelta(seconds=63, microseconds=100000), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63, microseconds=300000), datetime.timedelta(seconds=65, microseconds=400000), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65, microseconds=600000), datetime.timedelta(seconds=66, microseconds=800000), 'Line 04']
        ]

    def test_from(self):
        format_lines = "[601][631] Line 01|Line 02\n[633][654] Line 03|Line 04\n[656][668] Line 04\n"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            with open(mock_file, "rt", encoding="utf-8", errors="ignore") as path_file:
                self.assertEqual(self.general_lines, sbl.from_mpl(path_file, "file.txt"))

    def test_to(self):
        format_lines = ["[601][631] Line 01|Line 02", "[633][654] Line 03|Line 04", "[656][668] Line 04"]
        self.assertEqual(format_lines, sbl.to_mpl(self.general_lines, "file.txt"))


class SubRipTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60, microseconds=60000), datetime.timedelta(seconds=63, microseconds=105000), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63, microseconds=272000), datetime.timedelta(seconds=65, microseconds=440000), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65, microseconds=607000), datetime.timedelta(seconds=66, microseconds=775000), 'Line 04']
        ]

    def test_from(self):
        format_lines = "1\n00:01:00,060 --> 00:01:03,105\nLine 01\nLine 02\n\n2\n00:01:03,272 --> 00:01:05,440\nLine 03\nLine 04\n\n3\n00:01:05,607 --> 00:01:06,775\nLine 04\n\n"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            with open(mock_file, "rt", encoding="utf-8", errors="ignore") as path_file:
                self.assertEqual(self.general_lines, sbl.from_srt(path_file, "file.txt"))

    def test_to(self):
        format_lines = ["1\n00:01:00,060 --> 00:01:03,105\nLine 01\nLine 02\n", "2\n00:01:03,272 --> 00:01:05,440\nLine 03\nLine 04\n", "3\n00:01:05,607 --> 00:01:06,775\nLine 04\n"]
        self.assertEqual(format_lines, sbl.to_srt(self.general_lines, "file.txt"))


class MicroDVDTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60, microseconds=60000), datetime.timedelta(seconds=63, microseconds=105000), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63, microseconds=272000), datetime.timedelta(seconds=65, microseconds=440000), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65, microseconds=607000), datetime.timedelta(seconds=66, microseconds=775000), 'Line 04']
        ]

    def test_from(self):
        format_lines = "{1440}{1513}Line 01|Line 02\n{1517}{1569}Line 03|Line 04\n{1573}{1601}Line 04\n"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            with open(mock_file, "rt", encoding="utf-8", errors="ignore") as path_file:
                self.assertEqual(self.general_lines, sbl.from_sub(path_file, "file.txt"))

    def test_to(self):
        format_lines = ["{1440}{1513}Line 01|Line 02", "{1517}{1569}Line 03|Line 04", "{1573}{1601}Line 04"]
        self.assertEqual(format_lines, sbl.to_sub(self.general_lines, "file.txt"))


class TMPlayerTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60), datetime.timedelta(seconds=61), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63), datetime.timedelta(seconds=64), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65), datetime.timedelta(seconds=66), 'Line 04']
        ]

    def test_from(self):
        format_lines = "00:01:00:Line 01|Line 02\n00:01:03:Line 03|Line 04\n00:01:05:Line 04"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            with open(mock_file, "rt", encoding="utf-8", errors="ignore") as path_file:
                self.assertEqual(self.general_lines, sbl.from_tmp(path_file, "file.txt"))

    def test_to(self):
        format_lines = ["00:01:00:Line 01|Line 02", "00:01:03:Line 03|Line 04", "00:01:05:Line 04"]
        self.assertEqual(format_lines, sbl.to_tmp(self.general_lines, "file.txt"))


if __name__ == '__main__':
    ut.main()
