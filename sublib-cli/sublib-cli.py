import os
import sys
import logging
import argparse

import sublib
import chardet


def parser():
    arg_parser = argparse.ArgumentParser(
        usage=f"{os.path.basename(__file__)} "
              f"[--help] [path form_to [--log <file>]]",
        description="CLI implementation of Sublib package.",
        epilog="Supported formats: mpl, srt, sub, tmp",
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=52
        )
    )
    arg_parser.add_argument(
        "path",
        type=str,
        metavar="path",
        help="Directory or single file to convert"
    )
    arg_parser.add_argument(
        "form_to",
        type=str,
        choices=["mpl", "srt", "sub", "tmp"],
        metavar="form_to",
        help="Target format"
    )
    arg_parser.add_argument(
        "-l", "--log",
        type=str,
        nargs="?",
        const=True,
        metavar="log",
        help="Enable logging. Optionally takes a file"
    )
    args = arg_parser.parse_args()
    return (args.path, args.form_to, args.log)


def get_files_from_path(path):
    if os.path.isfile(path):
        files = [path]
    if os.path.isdir(path):
        files = list(os.walk(path))
        files = [
            file.replace(file, path + "\\" + file)
            for file in files[0][2]
        ]
    return files


def get_file_encoding(file):
    with open(file, "rb") as f:
        file_content = f.read()
    result = chardet.detect(file_content)
    return result["encoding"]


def get_subtitle_object(subtitle):
    file = subtitle["path"]
    encoding = subtitle["encoding"]
    if subtitle["format"] == "mpl":
        subtitle = sublib.MPlayer2(file, encoding)
    elif subtitle["format"] == "srt":
        subtitle = sublib.SubRip(file, encoding)
    elif subtitle["format"] == "sub":
        subtitle = sublib.MicroDVD(file, encoding)
    elif subtitle["format"] == "tmp":
        subtitle = sublib.TMPlayer(file, encoding)
    return subtitle


def main(path, form_to, log):

    path = os.path.normpath(path)
    path = os.path.abspath(path)

    if os.path.exists(path) is False:
        exit()

    subtitles = [
        {"path": file}
        for file in get_files_from_path(path)
    ]

    for subtitle in subtitles:
        subtitle.update({
            "encoding": get_file_encoding(subtitle["path"])
        })

    for subtitle in subtitles:
        file = subtitle["path"]
        encoding = subtitle["encoding"]
        subtitle.update({
            "format": sublib.detect(file, encoding)
        })

    for i, subtitle in enumerate(subtitles):
        subtitles[i] = get_subtitle_object(subtitle)


if __name__ == "__main__":

    try:
        main(*parser())
    except Exception:
        print("An unknown error has occurred:")
        print(sys.exc_info())
