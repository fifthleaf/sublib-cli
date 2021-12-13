import re
import os
import datetime as dt
import logging as lg


logger = lg.getLogger(__name__)


def detect(path_file, encoding):
    """Detect subtitle format"""
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
    logger.info("Detected format: " + str(result))
    return result


def write(form_to, path_file, encoding, lines):
    if form_to in ("mpl", "tmp"):
        extension = "txt"
    elif form_to in ("srt", "sub"):
        extension = form_to
    file_name = f"{path_file[:path_file.rfind('.')]}.{extension}"
    with open(file_name, "wt", encoding=encoding, errors="ignore") as file:
        for line in lines:
            file.write(line + "\n")
    logger.info(f"Write {form_to.upper()} to new .{extension} file: {os.path.basename(file_name)}")


# MPL Functions


def from_mpl(file, path_file):
    """Convert MPL to general list"""
    lines = [line.split("]", 2) for line in (line.rstrip("\n") for line in file)]
    for line in lines:
        line[0] = dt.timedelta(seconds=round(float(line[0].replace("[", "")) / 10.0, 1))   # MPL use as time: sec * 10
        line[1] = dt.timedelta(seconds=round(float(line[1].replace("[", "")) / 10.0, 1))
        line[2] = line[2].lstrip()
    logger.info(f"Make general format from MPL file: {str(os.path.basename(path_file))}")
    return lines


def to_mpl(lines, path_file):
    """Convert general list to MPL"""
    for line in lines:
        line[0] = round(line[0].total_seconds() * 10)   # MPL use as time: sec * 10
        line[1] = round(line[1].total_seconds() * 10)
    logger.info(f"Make MPL from general format: {str(os.path.basename(path_file))}")
    return [f"[{line[0]}][{line[1]}] {line[2]}" for line in lines]


# SRT Functions


def from_srt(file, path_file):
    """Convert SRT to general list"""
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
    logger.info(f"Make general format from SRT file: {str(os.path.basename(path_file))}")
    return lines


def to_srt(lines, path_file):
    """Convert general list to SRT"""
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
    logger.info(f"Make SRT from general format: {str(os.path.basename(path_file))}")
    return [f"{num}\n{line[0]} --> {line[1]}\n{line[2]}\n" for num, line in enumerate(lines, 1)]


# SUB Functions


def from_sub(file, path_file):
    """Convert SUB to general list"""
    lines = [line.split("}", 2) for line in (line.rstrip("\n") for line in file)]
    for line in lines:
        line[0] = dt.timedelta(seconds=round(float(line[0].replace("{", "")) / 23.976, 3))   # SUB use frames as time
        line[1] = dt.timedelta(seconds=round(float(line[1].replace("{", "")) / 23.976, 3))
        for style in re.findall(r"{.*}", line[2]):
            line[2] = line[2].replace(style, "")
    logger.info(f"Make general format from SUB file: {str(os.path.basename(path_file))}")
    return lines


def to_sub(lines, path_file):
    """Convert general list to SUB"""
    for line in lines:
        line[0] = round(line[0].total_seconds() * 23.976)   # SUB use frames as time
        line[1] = round(line[1].total_seconds() * 23.976)
    logger.info(f"Make SUB from general format: {str(os.path.basename(path_file))}")
    return [f"{{{line[0]}}}{{{line[1]}}}{line[2]}" for line in lines]


# TMP Functions


def from_tmp(file, path_file):
    """Convert TMP to general list"""
    lines = [line.split(":", 3) for line in (line.rstrip("\n") for line in file)]
    lines = [[f"{line[0]}:{line[1]}:{line[2]}", f"{line[0]}:{line[1]}:{line[2]}", line[3]] for line in lines]
    for line in lines:
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S")
        line[1] = dt.datetime.strptime(line[1], "%H:%M:%S")
        line[0] = dt.timedelta(hours=line[0].hour, minutes=line[0].minute, seconds=line[0].second, microseconds=line[0].microsecond)
        line[1] = dt.timedelta(hours=line[1].hour, minutes=line[1].minute, seconds=line[1].second + 1, microseconds=line[1].microsecond)
    logger.info(f"Make general format from TMP file: {str(os.path.basename(path_file))}")
    return lines


def to_tmp(lines, path_file):
    """Convert general list to TMP"""
    for line in lines:
        line[0] = str(line[0])
        if len(line[0]) == 7:
            line[0] = line[0] + "." + "".zfill(6)   # If no microsecons, fill with zeros
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
        line[0] = line[0].strftime("%H:%M:%S.%f")
        line[0] = line[0][:len(line[0]) - 7]
    logger.info(f"Make TMP from general format: {str(os.path.basename(path_file))}")
    return [f"{line[0]}:{line[2]}" for line in lines]
