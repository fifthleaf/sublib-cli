import pytest
import sublib
import sublib_cli


class TestGetSubtitleFunction:

    @pytest.fixture
    def set_details(self):
        return {
            "path": "file.txt",
            "encoding": "utf-8"
        }

    def test_get_subtitle_mpl(self, set_details):
        details = set_details
        details["format"] = "mpl"
        subtitle = sublib_cli.get_subtitle(details)
        assert isinstance(subtitle, sublib.MPlayer2)

    def test_get_subtitle_srt(self, set_details):
        details = set_details
        details["format"] = "srt"
        subtitle = sublib_cli.get_subtitle(details)
        assert isinstance(subtitle, sublib.SubRip)

    def test_get_subtitle_sub(self, set_details):
        details = set_details
        details["format"] = "sub"
        subtitle = sublib_cli.get_subtitle(details)
        assert isinstance(subtitle, sublib.MicroDVD)

    def test_get_subtitle_tmp(self, set_details):
        details = set_details
        details["format"] = "tmp"
        subtitle = sublib_cli.get_subtitle(details)
        assert isinstance(subtitle, sublib.TMPlayer)
