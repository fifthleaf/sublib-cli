# Offline Sub Converter

Offline Sub Converter allows you to change subtitle formats using the command shell.

## Installation

This program uses an external module:
- chardet

You can install it with the command:

```bash
pip install -r requirements.txt
```

If the installation fails due to lack of access rights, try this:

```bash
pip install --user -r requirements.txt
```

## Usage

To convert, type:

```bash
python sub_converter.py "path" format_to
```

path 		- Directory or single file to convert\
format_to 	- Target format

## Supported formats

- SubRip (srt), .srt
- MicroDVD (sub), .sub
- MPlayer2 (mpl), .txt
- TMPlayer (tmp), .txt

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)