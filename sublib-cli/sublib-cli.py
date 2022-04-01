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


def main(path, form_to, log):

    path = os.path.normpath(path)
    path = os.path.abspath(path)


if __name__ == "__main__":

    try:
        main(*parser())
    except Exception:
        print("An unknown error has occurred:")
        print(sys.exc_info())
