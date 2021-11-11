<h1 align="center">Offline Sub Converter</h1>

<p align="center">The CLI script made with Python for easy conversion of subtitles files</p>

<p  align="center">
	<a style="text-decoration:none" href="https://github.com/TheFifthLeaf/offline-sub-converter/releases">
		<img src="https://img.shields.io/github/v/release/TheFifthLeaf/offline-sub-converter?color=3C7DD9" alt="Releases">
	</a>
	<a style="text-decoration:none" href="https://www.python.org/downloads/">
		<img src="https://img.shields.io/badge/python-3.6%2B-3C7DD9" alt="Python Version">
	</a>
	<a style="text-decoration:none" href="https://choosealicense.com/licenses/gpl-3.0/">
		<img src="https://img.shields.io/badge/license-GPL%20V3-3C7DD9" alt="License GPLv3">
	</a>
	<a href="https://www.codefactor.io/repository/github/thefifthleaf/offline-sub-converter">
		<img src="https://img.shields.io/badge/codefactor-A%2B-3C7DD9" alt="CodeFactor" />
	</a>
</p>

## Installation

You will need an external module to use the .py script
- chardet

You can install it throught the requirements file

```bash
pip install -r requirements.txt
```

If the installation fails due to lack of access rights, try this

```bash
pip install --user -r requirements.txt
```

**However, feel free to use the portable .exe file, which does not require additional installations.**

## Usage

To convert using .exe, please type:

```bash
sub_converter.exe "path" format
```

And using .py, type:

```bash
python sub_converter.py "path" format
```

### Usage example

This will convert the specified file to SubRip format
```bash
sub_converter.exe "D:\Video\Se7en.sub" srt
```
This will convert all the subtitle files in the Video directory to MicroDVD format
```bash
sub_converter.exe "D:\Video" sub
```
This will convert all the subtitle files in the current folder to MPlayer2 format
```bash
sub_converter.exe "." mpl
```
This will display help information
```bash
sub_converter.exe -h
```

## Supported formats

- as **srt** - SubRip (.srt)
- as **sub** - MicroDVD (.sub)
- as **mpl** - MPlayer2 (.txt)
- as **tmp** - TMPlayer (.txt)

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)