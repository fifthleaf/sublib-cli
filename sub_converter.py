import os
import re
import sys
import datetime as dt
import chardet as chdt
import argparse as arps


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


def form_detect(path_file, encoding):
    """
    Detect subtitle format
    """
    mpl_reg = "\\[[0-9]+\\]\\[[0-9]+\\] .*\n"                                                           # [START][STOP] TEXT\n
    srt_reg = "[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n"   # NUM\nSTART --> STOP\n
    sub_reg = "{[0-9]+}{[0-9]+}.*\n"                                                                    # {START}{STOP}TEXT\n
    tmp_reg = "[0-9]+:[0-9]+:[0-9]+:.*\n"                                                               # START:TEXT\n
    with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
        content = file.read()
    if len(re.findall(mpl_reg, content)) > 0:
        result = "mpl"
    elif len(re.findall(sub_reg, content)) > 0:
        result = "sub"
    elif len(re.findall(srt_reg, content)) > 0:
        result = "srt"
    elif len(re.findall(tmp_reg, content)) > 0:
        result = "tmp"
    else:
        result = False
    return result


def from_mpl(path_file, encoding):
    """
    Convert MPL to general list
    """
    with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
        lines = [line.split("]", 2) for line in (line.rstrip("\n") for line in file)]
    for line in lines:
        line[0] = dt.timedelta(seconds=round(float(line[0].replace("[", "")) / 10.0, 1))   # MPL use as time: sec * 10
        line[1] = dt.timedelta(seconds=round(float(line[1].replace("[", "")) / 10.0, 1))
        line[2] = line[2].lstrip()
    return lines


def from_srt(path_file, encoding):
    """
    Convert SRT to general list
    """
    with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
        lines, temp = [], []
        for line in file:
            if line != "\n":
                temp.append(line.rstrip("\n"))
            else:
                lines.append(temp)
                temp = []
    lines = [[*line[1].split(" --> "), "|".join(line[2:])] for line in lines]
    for line in lines:
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S,%f")
        line[1] = dt.datetime.strptime(line[1], "%H:%M:%S,%f")
        line[0] = dt.timedelta(hours=line[0].hour, minutes=line[0].minute, seconds=line[0].second, microseconds=line[0].microsecond)
        line[1] = dt.timedelta(hours=line[1].hour, minutes=line[1].minute, seconds=line[1].second, microseconds=line[1].microsecond)
        for style in re.findall(r"</.*>", line[2]):
            line[2] = line[2].replace(style, "")
        for style in re.findall(r"<.*>", line[2]):
            line[2] = line[2].replace(style, "")
    return lines


def from_sub(path_file, encoding):
    """
    Convert SUB to general list
    """
    with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
        lines = [line.split("}", 2) for line in (line.rstrip("\n") for line in file)]
    for line in lines:
        line[0] = dt.timedelta(seconds=round(float(line[0].replace("{", "")) / 23.976, 3))   # SUB use frames as time
        line[1] = dt.timedelta(seconds=round(float(line[1].replace("{", "")) / 23.976, 3))
        for style in re.findall(r"{.*}", line[2]):
            line[2] = line[2].replace(style, "")
    return lines


def from_tmp(path_file, encoding):
    """
    Convert TMP to general list
    """
    with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
        lines = [line.split(":", 3) for line in (line.rstrip("\n") for line in file)]
        lines = [[f"{line[0]}:{line[1]}:{line[2]}", f"{line[0]}:{line[1]}:{line[2]}", line[3]] for line in lines]
    for line in lines:
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S")
        line[1] = dt.datetime.strptime(line[1], "%H:%M:%S")
        line[0] = dt.timedelta(hours=line[0].hour, minutes=line[0].minute, seconds=line[0].second, microseconds=line[0].microsecond)
        line[1] = dt.timedelta(hours=line[1].hour, minutes=line[1].minute, seconds=line[1].second + 1, microseconds=line[1].microsecond)
    return lines


def to_mpl(path_file, lines, encoding):
    """
    Convert general list to MPL
    """
    for line in lines:
        line[0] = round(line[0].total_seconds() * 10)   # MPL use as time: sec * 10
        line[1] = round(line[1].total_seconds() * 10)
    formated_lines = [f"[{line[0]}][{line[1]}] {line[2]}" for line in lines]
    with open(path_file[:path_file.rfind(".")] + ".txt", "wt", encoding=encoding, errors="ignore") as file:
        for line in formated_lines:
            file.write(line + "\n")


def to_srt(path_file, lines, encoding):
    """
    Convert general list to SRT
    """
    for line in lines:
        line[0] = str(line[0])
        line[1] = str(line[1])
        if len(line[0]) == 7:
            line[0] = line[0] + "." + "".zfill(6)   # If no microsecons, fill with zeros
        if len(line[1]) == 7:
            line[1] = line[1] + "." + "".zfill(6)
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
        line[1] = dt.datetime.strptime(line[1], "%H:%M:%S.%f")
        line[0] = line[0].strftime("%H:%M:%S.%f").replace(".", ",")
        line[1] = line[1].strftime("%H:%M:%S.%f").replace(".", ",")
        line[0] = line[0][:len(line[0]) - 3]
        line[1] = line[1][:len(line[1]) - 3]
        line[2] = line[2].replace("|", "\n")
    formated_lines = [f"{num}\n{line[0]} --> {line[1]}\n{line[2]}\n" for num, line in enumerate(lines, 1)]
    with open(path_file[:path_file.rfind(".")] + ".srt", "wt", encoding=encoding, errors="ignore") as file:
        for line in formated_lines:
            file.write(line + "\n")


def to_sub(path_file, lines, encoding):
    """
    Convert general list to SUB
    """
    for line in lines:
        line[0] = round(line[0].total_seconds() * 23.976)   # SUB use frames as time
        line[1] = round(line[1].total_seconds() * 23.976)
    formated_lines = [f"{{{line[0]}}}{{{line[1]}}}{line[2]}" for line in lines]
    with open(path_file[:path_file.rfind(".")] + ".sub", "wt", encoding=encoding, errors="ignore") as file:
        for line in formated_lines:
            file.write(line + "\n")


def to_tmp(path_file, lines, encoding):
    """
    Convert general list to TMP
    """
    for line in lines:
        line[0] = str(line[0])
        if len(line[0]) == 7:
            line[0] = line[0] + "." + "".zfill(6)   # If no microsecons, fill with zeros
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
        line[0] = line[0].strftime("%H:%M:%S.%f")
        line[0] = line[0][:len(line[0]) - 7]
    formated_lines = [f"{line[0]}:{line[2]}" for line in lines]
    with open(path_file[:path_file.rfind(".")] + ".txt", "wt", encoding=encoding, errors="ignore") as file:
        for line in formated_lines:
            file.write(line + "\n")


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
        form = form_detect(path, encoding)
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
            form = form_detect(file, encoding)
            if form is False:
                files.remove(file)
            else:
                form_from.append(form)
                encodings.append(encoding)
        if len(form_from) <= 0:
            sys.exit("No valid files in the path")

    for form, *param in zip(form_from, files, encodings):

        if form == "mpl":
            new_file = from_mpl(*param)
        elif form == "srt":
            new_file = from_srt(*param)
        elif form == "sub":
            new_file = from_sub(*param)
        elif form == "tmp":
            new_file = from_tmp(*param)
        lines_list.append(new_file)

    if form_to == "mpl":

        for parameters in zip(files, lines_list, encodings):
            to_mpl(*parameters)

    elif form_to == "srt":

        for parameters in zip(files, lines_list, encodings):
            to_srt(*parameters)

    elif form_to == "sub":

        for parameters in zip(files, lines_list, encodings):
            to_sub(*parameters)

    elif form_to == "tmp":

        for parameters in zip(files, lines_list, encodings):
            to_tmp(*parameters)
