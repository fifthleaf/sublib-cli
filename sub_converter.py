import os
import sys
import argparse as arps
import logging as lg

import chardet as chdt
import lib.sublib as sbl


def parser():
    """Parses given arguments"""
    arg_parser = arps.ArgumentParser(
        usage=f"{os.path.basename(__file__)} [--help] [path form_to [--log <file>]]",
        description="Offline Sub Converter allows you to change subtitle formats using the command console.",
        epilog="Supported formats: mpl, srt, sub, tmp",
        formatter_class=lambda prog: arps.HelpFormatter(prog, max_help_position=52)
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


def check_file(path_file, path_files, forms_from, encodings, logger):
    """Check if file is correct"""
    with open(path_file, "rb") as f:
        encoding = chdt.detect(f.read())["encoding"]
    logger.info("Encoding detected: " + str(encoding))
    form = sbl.detect(path_file, encoding)
    if form is False:
        path_files.remove(path_file)
        logger.info("Invalid file: " + str(os.path.basename(path_file)))
    else:
        forms_from.append(form)
        encodings.append(encoding)
        logger.info("Correct file: " + str(os.path.basename(path_file)))


def set_logger(path_file, lvl):
    """Set logger ready to use"""
    path_file = os.path.normpath(path_file)
    path_file = os.path.abspath(path_file)
    lg.basicConfig(
        filename=path_file, filemode="wt", encoding="utf-8",
        format="[%(levelname)s][%(asctime)s][%(module)s.%(funcName)s] %(message)s",
        level=lvl
    )
    return lg.getLogger(__name__)


def main(path, form_to, log_file):
    """The main function of the program that control and performs all the actions."""

    path = os.path.normpath(path)
    path = os.path.abspath(path)

    if log_file is None:
        log_file = f"{os.path.splitext(__file__)[0]}.log"
        logger = set_logger(log_file, lg.CRITICAL)
    elif log_file is True:
        log_file = f"{os.path.splitext(__file__)[0]}.log"
        logger = set_logger(log_file, lg.INFO)
    else:
        logger = set_logger(log_file, lg.INFO)

    logger.info("Logger setted up")

    if os.path.exists(path) is False:
        logger.critical("Entered path does not exists")
        sys.exit("Entered path does not exists")

    logger.info("Correct path: " + str(path))

    if os.path.isfile(path):
        path_files = [path]
    elif os.path.isdir(path):
        path_files = list(os.walk(path))[0][2]
        path_files = [path_file.replace(path_file, path + "\\" + path_file) for path_file in path_files]

    logger.info(f"All files: {str([os.path.basename(path_file) for path_file in path_files])}")

    forms_from, encodings = [], []

    for path_file in path_files:
        check_file(path_file, path_files, forms_from, encodings, logger)

    if len(path_files) <= 0:
        logger.critical("No valid files in the path")
        sys.exit("No valid files in the path")

    logger.info(f"Valid files: {str([os.path.basename(path_file) for path_file in path_files])}")

    general_lines = []

    for form, path_file, encoding in zip(forms_from, path_files, encodings):
        with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
            if form == "mpl":
                new_lines = sbl.from_mpl(file, path_file)
            elif form == "srt":
                new_lines = sbl.from_srt(file, path_file)
            elif form == "sub":
                new_lines = sbl.from_sub(file, path_file)
            elif form == "tmp":
                new_lines = sbl.from_tmp(file, path_file)
        general_lines.append(new_lines)

    logger.info("All files converted to general format")

    if form_to == "mpl":
        formatted_lines = map(sbl.to_mpl, general_lines, path_files)
    elif form_to == "srt":
        formatted_lines = map(sbl.to_srt, general_lines, path_files)
    elif form_to == "sub":
        formatted_lines = map(sbl.to_sub, general_lines, path_files)
    elif form_to == "tmp":
        formatted_lines = map(sbl.to_tmp, general_lines, path_files)

    logger.info("All lines converted to desired format")

    for parameters in zip(path_files, encodings, formatted_lines):
        sbl.write(form_to, *parameters)

    logger.info("All files writed")

    lg.shutdown()
    if os.path.getsize(log_file) == 0:
        os.remove(log_file)


if __name__ == "__main__":

    try:
        main(*parser())
    except Exception:
        print("An unknown error has occurred:")
        print(sys.exc_info())
