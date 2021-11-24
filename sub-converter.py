import os
import sys
import chardet as chdt
import argparse as arps
import logging as lg
import sublib as sbl


def parser():
    """Parses given arguments"""
    arg_parser = arps.ArgumentParser(
        usage="sub-converter [--help] [path form_to [--log <file>]]",
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


def set_logger(path_file, lvl):
    """Set logger ready to use"""
    path_file = os.path.normpath(path_file)
    path_file = os.path.abspath(path_file)
    lg.basicConfig(
        filename=path_file, filemode="wt", encoding="utf-8",
        format="[%(levelname)s][%(asctime)s][%(module)s.%(funcName)s] %(message)s",
        level=lvl
    )
    lg.info("Set up logger")
    return lg.getLogger(__name__)


def main():

    path, form_to, log_file = parser()
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

    if os.path.exists(path) is False:
        logger.critical("Entered path does not exists")
        sys.exit("Entered path does not exists")
    logger.info("Correct path: " + str(path))

    form_from, encodings, lines_list = [], [], []

    if os.path.isfile(path):

        with open(path, "rb") as f:
            encoding = chdt.detect(f.read())["encoding"]
            logger.info("Encoding detected: " + str(encoding))
        form = sbl.detect(path, encoding)
        if form is False:
            logger.critical("Cannot convert this file")
            sys.exit("Cannot convert this file")
        logger.info("Correct file: " + str(os.path.basename(path)))
        files = [path]
        form_from.append(form)
        encodings.append(encoding)
        logger.info("Ready file: " + str(os.path.basename(path)))

    elif os.path.isdir(path):

        files = list(os.walk(path))[0][2]
        logger.info("File list: " + str(files))
        files = [file.replace(file, path + "\\" + file) for file in files]
        for file in files:
            with open(file, "rb") as f:
                encoding = chdt.detect(f.read())["encoding"]
                logger.info("Encoding detected: " + str(encoding))
            form = sbl.detect(file, encoding)
            if form is False:
                files.remove(file)
                logger.info("Remove unsupported file: " + str(os.path.basename(file)))
            else:
                form_from.append(form)
                encodings.append(encoding)
                logger.info("Ready file: " + str(os.path.basename(file)))
        if len(form_from) <= 0:
            logger.critical("No valid files in the path")
            sys.exit("No valid files in the path")
        logger.info("All files ready")

    for form, *param in zip(form_from, files, encodings):

        if form == "mpl":
            new_file = sbl.from_mpl(*param)
        elif form == "srt":
            new_file = sbl.from_srt(*param)
        elif form == "sub":
            new_file = sbl.from_sub(*param)
        elif form == "tmp":
            new_file = sbl.from_tmp(*param)
        lines_list.append(new_file)

    logger.info("All files converted to general format")

    if form_to == "mpl":

        for parameters in zip(files, lines_list, encodings):
            sbl.to_mpl(*parameters)

    elif form_to == "srt":

        for parameters in zip(files, lines_list, encodings):
            sbl.to_srt(*parameters)

    elif form_to == "sub":

        for parameters in zip(files, lines_list, encodings):
            sbl.to_sub(*parameters)

    elif form_to == "tmp":

        for parameters in zip(files, lines_list, encodings):
            sbl.to_tmp(*parameters)

    logger.info("All files writed")

    lg.shutdown()
    if os.path.getsize(log_file) == 0:
        os.remove(log_file)


if __name__ == "__main__":

    try:
        main()
    except Exception:
        print("An unknown error has occurred:")
        print(sys.exc_info())
