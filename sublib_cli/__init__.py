"""
CLI implementation of the sublib package.

VARIABLES

    __version__
        Contains the package version.

FUNCTONS

    detect_encoding(file)
        Detect file encoding.

    end(logger, logfile, start)
        End executing of script.

    find_files(path)
        Search for files in a path.

    get_new_path(file, form)
        Create path to desired subtitle file.

    get_subtitle(subtitle)
        Create Subtitle class instance.

    main(arguments)
        Main function of the script.

    parser()
        Parse CLI arguments.

    set_logger(file, level)
        Configure logging system.

    write_file(subtitle, file, form, logger)
        Write converted subtitle to new file.
"""

from sublib_cli.sublib_cli import parser, set_logger, find_files
from sublib_cli.sublib_cli import detect_encoding, get_subtitle, get_new_path
from sublib_cli.sublib_cli import write_file, end, main

__version__ = "1.3.0"
