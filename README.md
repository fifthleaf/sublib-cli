# Sublib-CLI

[![Release](https://img.shields.io/github/v/release/TheFifthLeaf/sublib-cli?color=3C7DD9)](https://github.com/TheFifthLeaf/sublib-cli/releases)
[![Min. Python version](https://img.shields.io/badge/python-3.6%2B-3C7DD9)](https://www.python.org/downloads/)
[![License GPLv3](https://img.shields.io/badge/license-GPL%20V3-3C7DD9)](https://choosealicense.com/licenses/gpl-3.0/)
[![Code quality](https://img.shields.io/codefactor/grade/github/TheFifthLeaf/sublib-cli/main?color=3C7DD9)](https://www.codefactor.io/repository/github/thefifthleaf/sublib-cli)
[![Tests](https://github.com/TheFifthLeaf/sublib-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/TheFifthLeaf/sublib-cli/actions/workflows/tests.yml)

CLI implementation of the [sublib](https://github.com/TheFifthLeaf/sublib) package.

Features
- Detect used format
- Convert subtitles formats

## Installation
Users on all platforms can use [python](https://github.com/TheFifthLeaf/sublib-cli/blob/main/sublib_cli/sublib_cli.py) script. For Windows users there is also [executable](https://github.com/TheFifthLeaf/sublib-cli/releases/download/1.3.0/sublib-cli.exe) version made with [pyinstaller](https://github.com/pyinstaller/pyinstaller).  

If you are developer please download whole project via `git clone` or [archive](https://github.com/TheFifthLeaf/sublib-cli/releases/tag/1.3.0).

Remember to install dependencies! \
**User**: ```pip install -r requirements.txt``` \
**Developer**: ```pip install -r requirements_dev.txt```

## Testing
Perform the tests with `pytest` and `pytest-mock`.
```bash
python -m pytest tests
```

## Usage
To check your current format:
```bash
python sublib_cli.py detect <path>
```
To convert subtitles to a different format:
```bash
python sublib_cli.py convert <path> <format>
```
For more help:
```bash
python sublib_cli.py --help
```

### Examples
This will display format of the specified subtitle file.
```bash
python sublib_cli.py detect "D:\Video\Se7en.txt"
```
This will display format for each subtitle file in Video directory.
```bash
python sublib_cli.py detect "D:\Video"
```
This will convert the specified file to SubRip format.
```bash
python sublib_cli.py convert "D:\Video\Se7en.sub" srt
```
This will convert all the subtitle files in the Video directory to MicroDVD format.
```bash
python sublib_cli.py convert "D:\Video" sub
```
This will convert all the subtitle files in the current folder to MPlayer2 format.
```bash
python sublib_cli.py convert "." mpl
```
### Logging
By default, the program creates logs only when it encounters a fatal error. You can this behavior using `log` flag. 

To log into the default file:
```bash
python sublib_cli.py convert "D:\Video\Se7en.sub" srt --log
```
To log to a specific file:
```bash
python sublib_cli.py detect "D:\Video\Se7en.sub" --log "mylog.log"
```

## Formats
Supported:
| Full name | Short name | Default ext. |
|:---------:|:----------:|:------------:|
| MPlayer2  | mpl        | .txt         |
| SubRip    | srt        | .srt         |
| MicroDVD  | sub        | .sub         |
| TMPlayer  | tmp        | .txt         |

## Contributing
Pull requests are welcome!
