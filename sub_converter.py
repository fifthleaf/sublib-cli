import os
import sys
import chardet as chdt
import argparse as arps
import sublib as sbl


def parser():
    """
    Parses given arguments
    """
    arg_parser = arps.ArgumentParser(
        usage="sub_converter.py [-h] path form_to",
        description="Offline Sub Converter allows you to change subtitle formats using the command console.",
        epilog="Supported formats: mpl, srt, sub, tmp"
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
    args = arg_parser.parse_args()
    return (args.path, args.form_to)


if __name__ == "__main__":

    path, form_to = parser()
    path = os.path.normpath(path)
    path = os.path.abspath(path)

    if os.path.exists(path) is False:
        sys.exit("Entered path does not exists")

    form_from, encodings, lines_list = [], [], []

    if os.path.isfile(path):

        with open(path, "rb") as f:
            encoding = chdt.detect(f.read())["encoding"]
        form = sbl.detect(path, encoding)
        if form is False:
            sys.exit("Cannot convert this file")
        files = [path]
        form_from.append(form)
        encodings.append(encoding)

    elif os.path.isdir(path):

        files = list(os.walk(path))[0][2]
        files = [file.replace(file, path + "\\" + file) for file in files]
        for file in files:
            with open(file, "rb") as f:
                encoding = chdt.detect(f.read())["encoding"]
            form = sbl.detect(file, encoding)
            if form is False:
                files.remove(file)
            else:
                form_from.append(form)
                encodings.append(encoding)
        if len(form_from) <= 0:
            sys.exit("No valid files in the path")

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
