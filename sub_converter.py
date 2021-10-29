import os
import re
import sys
import datetime as dt
import chardet as chdt
import argparse as arps


def parser():
    # Parses given arguments

    parser = arps.ArgumentParser(
        usage='sub_converter.py [-h] path form_from form_to',
        description='Offline Sub Converter allows you to change subtitle formats using the command shell.',
        epilog='Supported formats: mpl, srt, sub, tmp'
    )

    parser.add_argument(
        'path',
        type=str,
        metavar='path',
        help='Directory or single file to convert'
    )
    parser.add_argument(
        'form_from',
        type=str,
        choices=['mpl', 'srt', 'sub', 'tmp'],
        metavar='form_from',
        help='Format of your file(s)'
    )
    parser.add_argument(
        'form_to',
        type=str,
        choices=['mpl', 'srt', 'sub', 'tmp'],
        metavar='form_to',
        help='Target format'
    )

    args = parser.parse_args()
    return (args.path, args.form_from, args.form_to)


def from_mpl(path_file):
    # Convert MPL to general list

    lines, enc = [], chdt.detect(open(path_file, 'rb').read())['encoding']

    with open(path_file, 'rt', encoding=enc, errors='ignore') as file:
        for x in file.readlines():
            line = x.rstrip('\n')
            line = line.split(']', 2)
            lines.append(line)

    for x in lines:
        x[0] = dt.timedelta(seconds=round(float(x[0].replace('[', '')) / 10, 1))
        x[1] = dt.timedelta(seconds=round(float(x[1].replace('[', '')) / 10, 1))
        x[2] = x[2].replace('|', '\n').lstrip()
        styles = re.findall(r'/[.*/]', x[2])
        for y in styles:
            x[2] = x[2].replace(y, '')

    return lines, enc


def from_srt(path_file):
    # Convert SRT to general list

    lines, enc = [], chdt.detect(open(path_file, 'rb').read())['encoding']

    with open(path_file, 'rt', encoding=enc, errors='ignore') as file:
        tmp, i = [], iter(file)
        while True:
            try:
                line = next(i)
                if line != '\n':
                    line = line.rstrip('\n')
                    if len(tmp) in (0, 1, 2):
                        tmp.append(line)
                    else:
                        tmp[2] = tmp[2] + '\n' + line
                else:
                    lines.append(tmp)
                    tmp = []
            except StopIteration:
                break

    new_lines = []
    for x in lines:
        start, end = x[1].split(' --> ')
        start = dt.datetime.strptime(start, '%H:%M:%S,%f')
        end = dt.datetime.strptime(end, '%H:%M:%S,%f')
        start = dt.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second, microseconds=start.microsecond)
        end = dt.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
        styles = re.findall(r'</.*>', x[2])
        for y in styles:
            x[2] = x[2].replace(y, '')
        styles = re.findall(r'<.*>', x[2])
        for y in styles:
            x[2] = x[2].replace(y, '')
        new_lines.append([start, end, x[2]])

    return new_lines, enc


def from_sub(path_file):
    # Convert SUB to general list

    lines, enc = [], chdt.detect(open(path_file, 'rb').read())['encoding']

    with open(path_file, 'rt', encoding=enc, errors='ignore') as file:
        for x in file.readlines():
            line = x.replace('\ufeff', '')
            line = line.rstrip('\n')
            line = line.split('}', 2)
            lines.append(line)

    for x in lines:
        x[0] = dt.timedelta(seconds=round(float(x[0].replace('{', '')) / 23.976, 3))
        x[1] = dt.timedelta(seconds=round(float(x[1].replace('{', '')) / 23.976, 3))
        x[2] = x[2].replace('|', '\n')
        styles = re.findall(r'{.*}', x[2])
        for y in styles:
            x[2] = x[2].replace(y, '')

    return lines, enc


def from_tmp(path_file):
    # Convert TMP to general list

    lines, enc = [], chdt.detect(open(path_file, 'rb').read())['encoding']

    with open(path_file, 'rt', encoding=enc, errors='ignore') as file:
        for x in file.readlines():
            tmp = x.rstrip('\n')
            tmp = tmp.split(':', 3)
            start = end = f'{tmp[0]}:{tmp[1]}:{tmp[2]}'
            line = [start, end, tmp[3]]
            lines.append(line)

    for x in lines:
        x[0] = dt.datetime.strptime(x[0], '%H:%M:%S')
        x[1] = dt.datetime.strptime(x[1], '%H:%M:%S')
        x[0] = dt.timedelta(hours=x[0].hour, minutes=x[0].minute, seconds=x[0].second, microseconds=x[0].microsecond)
        x[1] = dt.timedelta(hours=x[1].hour, minutes=x[1].minute, seconds=x[1].second + 1, microseconds=x[1].microsecond)
        x[2] = x[2].replace('|', '\n')

    return lines, enc


def to_mpl(path_file, lines, enc):
    # Convert general list to MLP

    new_lines = []
    for x in lines:
        start = round(x[0].total_seconds() * 10)
        end = round(x[1].total_seconds() * 10)
        text = x[2].replace('\n', '|')
        new_lines.append('[' + f'{start}' + '][' + f'{end}' + ']' + f' {text}')

    with open(path_file[:path_file.rfind('.')] + '.txt', 'wt', encoding=enc, errors='ignore') as file:
        for x in new_lines:
            file.write(x + '\n')


def to_srt(path_file, lines, enc):
    # Convert general list to SRT

    new_lines, num = [], 1
    for x in lines:
        start = str(x[0])
        end = str(x[1])
        if len(start) == 7:
            start = start + '.' + ''.zfill(6)
        if len(end) == 7:
            end = end + '.' + ''.zfill(6)
        start = dt.datetime.strptime(start, '%H:%M:%S.%f')
        end = dt.datetime.strptime(end, '%H:%M:%S.%f')
        start = start.strftime('%H:%M:%S.%f').replace('.', ',')
        end = end.strftime('%H:%M:%S.%f').replace('.', ',')
        start = start[:len(start) - 3]
        end = end[:len(end) - 3]
        new_lines.append(str(num) + '\n' + f'{start} --> {end}' + '\n' + x[2] + '\n')
        num += 1

    with open(path_file[:path_file.rfind('.')] + '.srt', 'wt', encoding=enc, errors='ignore') as file:
        for x in new_lines:
            file.write(x + '\n')


def to_sub(path_file, lines, enc):
    # Convert general list to SUB

    new_lines = []
    for x in lines:
        start = round(x[0].total_seconds() * 23.976)
        end = round(x[1].total_seconds() * 23.976)
        text = x[2].replace('\n', '|')
        new_lines.append('{' + f'{start}' + '}{' + f'{end}' + '}' + f'{text}')

    with open(path_file[:path_file.rfind('.')] + '.sub', 'wt', encoding=enc, errors='ignore') as file:
        for x in new_lines:
            file.write(x + '\n')


def to_tmp(path_file, lines, enc):
    # Convert general list to TMP

    new_lines = []
    for x in lines:
        start = str(x[0])
        if len(start) == 7:
            start = start + '.' + ''.zfill(6)
        start = dt.datetime.strptime(start, '%H:%M:%S.%f')
        start = start.strftime('%H:%M:%S.%f')
        start = start[:len(start) - 7]
        text = x[2].replace('\n', '|')
        new_lines.append(f'{start}:{text}')

    with open(path_file[:path_file.rfind('.')] + '.txt', 'wt', encoding=enc, errors='ignore') as file:
        for x in new_lines:
            file.write(x + '\n')


def main():
    # Main function, run script

    # Parses arguments to tuple
    inp = parser()

    # Set path
    path = inp[0]

    # Normalize path
    path = os.path.normpath(path)
    path = os.path.normcase(path)
    path = os.path.abspath(path)

    # Check if path exist
    try:
        if os.path.exists(path) is False:
            raise Exception
    except Exception:
        print('The entered path does not exists')
        sys.exit()

    # Check files extensions
    if os.path.isfile(path):

        try:
            if os.path.splitext(path)[1] not in ('.srt', '.sub', '.txt'):
                raise Exception
        except Exception:
            print('You cannot convert this file')
            sys.exit()

        files = [path]

    elif os.path.isdir(path):

        files = list(os.walk(path))[0][2]

        for file in files:
            if os.path.splitext(file)[1] not in ('.srt', '.sub', '.txt'):
                files.remove(file)

        try:
            if len(files) == 0:
                raise Exception
        except Exception:
            print('There are no valid files in the path')
            sys.exit()

        for x, file in enumerate(files):
            files[x] = path + '\\' + file

    else:

        print('Invalid path')
        sys.exit()

    # Set form_from, form_to
    form_from, form_to = inp[1], inp[2]

    # Set lists for lines and encodings of files
    lines, encodings = [], []

    # Convert given format to CSV
    if form_from == 'mpl':

        for file in files:
            tmp = from_mpl(file)
            lines.append(tmp[0])
            encodings.append(tmp[1])

    elif form_from == 'srt':

        for file in files:
            tmp = from_srt(file)
            lines.append(tmp[0])
            encodings.append(tmp[1])

    elif form_from == 'sub':

        for file in files:
            tmp = from_sub(file)
            lines.append(tmp[0])
            encodings.append(tmp[1])

    elif form_from == 'tmp':

        for file in files:
            tmp = from_tmp(file)
            lines.append(tmp[0])
            encodings.append(tmp[1])

    # Convert CSV to new format
    if form_to == 'mpl':

        for parameters in zip(files, lines, encodings):
            to_mpl(*parameters)

    elif form_to == 'srt':

        for parameters in zip(files, lines, encodings):
            to_srt(*parameters)

    elif form_to == 'sub':

        for parameters in zip(files, lines, encodings):
            to_sub(*parameters)

    elif form_to == 'tmp':

        for parameters in zip(files, lines, encodings):
            to_tmp(*parameters)


if __name__ == '__main__':

    try:

        main()
        sys.exit()

    except Exception:

        print('An unknown error has occurred:')
        print(sys.exc_info())
        sys.exit()
