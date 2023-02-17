#! /usr/bin/env python3
"""
A module to manage command line parsing for the bin command.
"""
from argparse import ArgumentParser

help_msg = """
A program to import image files to a catalog location, sorting them by date.
"""


class Parser(object):
    """
    A class to manage a single argparse object.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 commandline_args):
        """
        Creates and initializes the parser object.

        :param commandline_args: The arguments passed on the command line.

        :return: Nothing.
        """

        self.parser = ArgumentParser(description=help_msg)

        help_str = "A pattern of files you want to import AND/OR directories which contain files you want to import. "
        help_str += "Files and directories may be given with or without full paths. If without, the current working "
        help_str += "directory is prepended to the given paths.\n"
        help_str += "You may provide either files or directories or a mixture of both. You may provide any number of "
        help_str += "these files or directories."
        self.parser.add_argument("import_files",
                                 nargs="+",
                                 type=str,
                                 help=help_str)

        help_str = "Catalog location. This is the path to the root of the photo catalog."
        self.parser.add_argument("catalog",
                                 type=str,
                                 help=help_str)

        help_str = "If one or more directories from which to import images are provided, using this flag will make "
        help_str += "the app also search subdirectories."
        self.parser.add_argument("-r",
                                 "--recursive",
                                 action="store_true",
                                 help=help_str)

        help_str = "If one or more directories from which to import images are provided, and if the recursive flag has "
        help_str += "been set, then this option is used to provide names of sub-directories to ignore. You may provide "
        help_str += "as many patterns here as you like. For example: -i @eaDir .DS_store. That said, often the only "
        help_str += "directories you would want ignore are hidden directories. For that you can also use the -h option "
        help_str += "described below."
        self.parser.add_argument("-i",
                                 "--ignore-dirs",
                                 nargs="+",
                                 type=str,
                                 help=help_str)

        help_str = "If one or more directories from which to import images are provided, and if the recursive flag has "
        help_str += "been set, then this option is used to automatically ignore any hidden subdirectories "
        help_str += "(subdirectories that begin with a leading dot)."
        self.parser.add_argument("-H",
                                 "--ignore-hidden",
                                 action="store_true",
                                 help=help_str)

        help_str = "By default the system will rename the files to pre-pend the EXIF date (or file creation date if "
        help_str += "no EXIF data exists for the file). If you do not wish to have the files renamed, use this flag."
        self.parser.add_argument("-n",
                                 "--no-rename",
                                 action="store_true",
                                 help=help_str)

        help_str = "An optional list of additional file types to import. If omitted, then a default list of: [cr2, "
        help_str += "jpg, png, tif, exr] will be used. You may list as many additional file types as is needed. "
        help_str += "These additional types will be in addition to the list above. Example: -t tiff img. If you "
        help_str += "ONLY want the types imported that you provide here, use the -f option IN ADDITION to this option. "
        help_str += "See below for more information."
        self.parser.add_argument("-t",
                                 "--additional-types",
                                 nargs="+",
                                 help=help_str)

        help_str = "Prevents the default list of file types from being imported. Only those file types that are "
        help_str += "defined using the -t option above will be imported."
        self.parser.add_argument("-f",
                                 "--force-types",
                                 action="store_true",
                                 help=help_str)

        help_str = "By default sidecar (xmp) files will be imported if they are found. If you do not wish for these "
        help_str += "files to be imported, use this flag."
        self.parser.add_argument("-k",
                                 "--skip-sidecars",
                                 action="store_true",
                                 help=help_str)

        help_str = "An optional list of additional sidecar file types to import. If omitted, then a default sidecar "
        help_str += "type of .xmp will be imported. You may list as many additional sidecar file types as needed. "
        help_str += "These additional types will be in addition to the .xmp type listed above. Example: -s .vrt blb. "
        help_str += "If you ONLY want the sidecar types imported that you provide here, use the -F option IN ADDITION "
        help_str += "to this option. See below for more information."
        self.parser.add_argument("-s",
                                 "--sidecar-types",
                                 nargs="+",
                                 default=["xmp"],
                                 help=help_str)

        help_str = "Prevents the default list of sidecar file types from being imported. Only those sidecar file types "
        help_str += "that are defined using the -s option above will be imported."
        self.parser.add_argument("-F",
                                 "--force-sidecar-types",
                                 action="store_true",
                                 help=help_str)

        help_str = "Runs silently. Does not print status to the command line as the program processes images."
        self.parser.add_argument("-S",
                                 "--silent",
                                 action="store_true",
                                 help=help_str)

        help_str = "Use this flag to run the import as a trial run. This will display all the files that would have "
        help_str += "been copied, but not actually make any changes on disk. This is a good way to evaluate the "
        help_str += "import before actually running it."
        self.parser.add_argument("-T",
                                 "--trial-run",
                                 action="store_true",
                                 help=help_str)

        self.args = self.parser.parse_args(commandline_args)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self):
        """
        Validates that the command line arguments are valid. Raises an appropriate error if any of the checks fail
        validation.

        :return: Nothing.
        """

        pass

