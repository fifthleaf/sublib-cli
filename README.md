# Offline Sub Converter

Offline Sub Converter allows you to change subtitle formats using the command shell.

## Installation

This program uses an external module. You can install it with the command:

```bash
pip install -r requirements.txt
```

If the installation fails due to lack of access rights, try this:

```bash
pip install --user -r requirements.txt
```

## Usage

Run:

```bash
python sub_converter.py
```

Usage inside script:

```bash
convert [path] [format_from] [format_to]
```

For help:

```bash
help
```

For exit:

```bash
exit
```

## Supported formats

- SubRip (srt), .srt
- MicroDVD (sub), .sub
- MPlayer2 (mpl), .txt
- TMPlayer (tmp), .txt

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)