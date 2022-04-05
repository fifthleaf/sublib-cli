import os
import sys
import timeit
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
        const=f"{os.path.splitext(__file__)[0]}.log",
        metavar="log",
        help="Enable logging. Optionally takes a file"
    )
    args = arg_parser.parse_args()
    return (args.path, args.form_to, args.log)


def set_logger(file, level):
    file = os.path.normpath(file)
    file = os.path.abspath(file)
    logging.basicConfig(
        filename=file,
        filemode="at",
        encoding="utf-8",
        format="%(asctime)s,%(levelname)s,"
               "%(module)s.%(funcName)s,%(message)s",
        level=level
    )
    logger = logging.getLogger(__name__)
    return logger


def find_files(path):
    if os.path.isfile(path):
        files = [path]
    if os.path.isdir(path):
        files = list(os.walk(path))
        files = [
            file.replace(file, path + "\\" + file)
            for file in files[0][2]
        ]
    return files


def detect_encoding(file):
    with open(file, "rb") as f:
        file_content = f.read()
    result = chardet.detect(file_content)
    result = result["encoding"]
    return result


def get_subtitle(subtitle):
    data = (subtitle["path"], subtitle["encoding"])
    if subtitle["format"] == "mpl":
        subtitle = sublib.MPlayer2(*data)
    elif subtitle["format"] == "srt":
        subtitle = sublib.SubRip(*data)
    elif subtitle["format"] == "sub":
        subtitle = sublib.MicroDVD(*data)
    elif subtitle["format"] == "tmp":
        subtitle = sublib.TMPlayer(*data)
    return subtitle


def get_new_path(file, form):
    path = file["path"]
    path = path[:path.rfind(".")]
    if form in ("mpl", "tmp"):
        path = f"{path}.txt"
    elif form in ("srt", "sub"):
        path = f"{path}.{form}"
    return path


def write_file(subtitle, file, form, logger):
    new = get_subtitle({
        "format": form,
        "path": "",
        "encoding": ""
    })
    lines = subtitle.get_general_format()
    new.set_from_general_format(lines)
    logger.info(f"Converted: {os.path.basename(subtitle.path)}")
    with open(file["path"], "wt", encoding=file["encoding"]) as f:
        f.writelines([f"{line}\n" for line in new.content])
    logger.info(f"Saved: {os.path.basename(file['path'])}")


def main(path, form_to, log):

    start = timeit.default_timer()

    path = os.path.normpath(path)
    path = os.path.abspath(path)

    if log:
        logger = set_logger(log, logging.INFO)
    else:
        log = f"{os.path.splitext(__file__)[0]}.log"
        logger = set_logger(log, logging.CRITICAL)

    logger.info("START")

    if os.path.exists(path) is False:
        logger.critical(f"Path does not exists: {path}")
        sys.exit(f"Path does not exists: {path}")
    else:
        logger.info(f"Path: {path}")

    input_files = []
    for file in find_files(path):
        input_files.append({
            "path": file,
            "encoding": detect_encoding(file),
            "format": sublib.detect(file, detect_encoding(file))
        })

    logger.info(
        f"Input files: "
        f"{[os.path.basename(file['path']) for file in input_files]}"
    )

    output_files = []
    for file in input_files:
        output_files.append({
            "path": get_new_path(file, form_to),
            "encoding": file["encoding"]
        })

    logger.info(
        f"Output files: "
        f"{[os.path.basename(file['path']) for file in output_files]}"
    )

    input_subtitles = [get_subtitle(file) for file in input_files]

    for subtitle, file in zip(input_subtitles, output_files):
        write_file(subtitle, file, form_to, logger)

    stop = timeit.default_timer()

    logger.info(f"Execution time: {stop-start}")
    logger.info("END")

    logging.shutdown()
    if os.path.getsize(log) == 0:
        os.remove(log)


if __name__ == "__main__":

    try:
        main(*parser())
    except Exception:
        print("An unknown error has occurred:")
        print(sys.exc_info())
