import os
import time

try:
    import exifread as exifread
except ImportError:
    exifread = None


# ======================================================================================================================
# import verifiedcopy



class Image(object):
    """
    A class to process and contain the metadata for an image
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 source_path,
                 catalog_path,
                 do_rename,
                 notify_obj,
                 count_str="",
                 include_sidecar=True,
                 sidecar_extensions=None):
        """
        Store some initial data for this image

        :param source_path: The full path on disk where this image lives.
        :param catalog_path: The full path where the image catalog lives.
        :param do_rename: A boolean that controls whether to rename the files on copy or not.
        :param notify_obj: A notification object.
        :param count_str: A string that displays the current count while reading exif data. Example: (1 of 10). Defaults
               to "".
        :param include_sidecar: If true, then a sidecar file will also be included if it exists. Defaults to True.
        :param sidecar_extensions: A list of possible file extensions for sidecar files. Defaults to ["xmp"].
        """

        self.source_path = source_path
        self.catalog_path = catalog_path
        self.notify_obj = notify_obj
        self.do_rename = do_rename
        self.count_str = count_str

        # self.base_name, self.ext = os.path.splitext(os.path.split(source_path)[1])
        self.year = None
        self.month = None
        self.day = None
        self.dest_path = None
        self.sidecar_path = None
        self.sidecar_dest_path = None

        if sidecar_extensions is None:
            self.sidecar_extensions = ["xmp"]
        else:
            self.sidecar_extensions = list()
            for sidecar_extension in sidecar_extensions:
                self.sidecar_extensions.append(sidecar_extension.lstrip("."))

        # Extract the image date
        self.process_image()

        # Find a sidecar image if it exists
        if include_sidecar:
            self.find_sidecar()

        # Build a destination path
        self.build_image_destination()

        # Build a sidecar destination path
        if include_sidecar:
            self.build_sidecar_destination()

    # ------------------------------------------------------------------------------------------------------------------
    def __read_image_exif(self,
                          exif_tag):
        """
        Reads in the specified exif tag from from the image given by image path.

        :param exif_tag: The name of the tag we want to extract

        :return: A string containing the exif data.
        """

        assert os.path.exists(self.source_path)
        assert not os.path.isdir(self.source_path)

        with open(self.source_path, 'rb') as image_file:
            self.notify_obj.notify((self.count_str + " Reading EXIF data: " + self.source_path).lstrip(" "))
            tags = exifread.process_file(image_file)

            if exif_tag not in tags.keys():
                return None

            return str(tags[exif_tag])

    # ------------------------------------------------------------------------------------------------------------------
    def process_image(self):
        """
        Extracts the date from the image exif data. If there is no exif data, extracts the file creation date instead.

        :return: Nothing.
        """

        assert os.path.exists(self.source_path)
        assert not os.path.isdir(self.source_path)

        image_date = self.__read_image_exif("EXIF DateTimeOriginal")
        if image_date is not None:
            image_date = image_date.split(" ")[0]
            self.year, self.month, self.day = image_date.split(":")
        else:
            self.year = time.strftime("%Y", time.localtime(os.path.getmtime(self.source_path)))
            self.month = time.strftime("%m", time.localtime(os.path.getmtime(self.source_path)))
            self.day = time.strftime("%d", time.localtime(os.path.getmtime(self.source_path)))

    # ------------------------------------------------------------------------------------------------------------------
    def find_sidecar(self):
        """
        Tries to find a sidecar file associated with the image. If there are more than one possible sidecar image file,
        only the first one found will be returned. The first one found will be the one associated with the first
        extension in the list.

        Looks for two different formats: image_name.ext (where ext is usually .xmp) OR image_name.original_ext.ext.

        So, for example, it will look for IMG_0001.xmp AND IMG_0001.cr2.xmp.

        :return: Nothing.
        """

        for ext in self.sidecar_extensions:

            # Look for cases where the sidecar image extension replaces the image file extension (upper and lower case)
            potential_sidecar_path = os.path.splitext(self.source_path)[0] + "." + ext.lstrip(".").lower()
            if os.path.exists(potential_sidecar_path):
                self.sidecar_path = potential_sidecar_path
                return
            potential_sidecar_path = os.path.splitext(self.source_path)[0] + "." + ext.lstrip(".").upper()
            if os.path.exists(potential_sidecar_path):
                self.sidecar_path = potential_sidecar_path
                return

            # Look for cases where the sidecar extension is added to the image file extension (upper and lower case)
            potential_sidecar_path = self.source_path + "." + ext.lstrip(".").lower()
            if os.path.exists(potential_sidecar_path):
                self.sidecar_path = potential_sidecar_path
                return
            potential_sidecar_path = self.source_path + "." + ext.lstrip(".").upper()
            if os.path.exists(potential_sidecar_path):
                self.sidecar_path = potential_sidecar_path
                return

    # ------------------------------------------------------------------------------------------------------------------
    def build_image_date(self):
        """
        Builds the image date based on the exif data.

        :return: A string containing the image date string.
        """

        return self.year + "-" + self.month + "-" + self.day

    # ------------------------------------------------------------------------------------------------------------------
    def build_dest_dir_path(self,
                            date_str):
        """
        Builds the path to the destination directory inside the catalog.

        :param date_str: A string that is built out of the date exif data.

        :return: A string containing the full path to the destination directory.
        """

        return os.path.join(self.catalog_path, self.year, date_str)

    # ------------------------------------------------------------------------------------------------------------------
    def build_image_destination(self):
        """
        Builds a path to the destination file.

        :return: Nothing.
        """

        date_str = self.build_image_date()
        full_dest_dir = self.build_dest_dir_path(date_str)
        if self.do_rename:
            dest_file_name = date_str + "-" + os.path.split(self.source_path)[1]
        else:
            dest_file_name = os.path.split(self.source_path)[1]
        self.dest_path = os.path.join(full_dest_dir, dest_file_name)

    # ------------------------------------------------------------------------------------------------------------------
    def build_sidecar_destination(self):
        """
        Builds a path to the sidecar's destination file.

        :return: Nothing.
        """

        if self.sidecar_path:
            date_str = self.build_image_date()
            full_dest_dir = self.build_dest_dir_path(date_str)
            dest_file_name = date_str + "-" + os.path.split(self.sidecar_path)[1]
            self.sidecar_dest_path = os.path.join(full_dest_dir, dest_file_name)

    # ------------------------------------------------------------------------------------------------------------------
    def copy_to_dest(self,
                     trial=False):
        """
        Does a verified copy of the source file to the destination.

        :param trial: If True, then the copy string will be printed, but no actual copy will be made. For debugging.
               Defaults to False.

        :return: Nothing.
        """

        copy_str = "Copying: "
        if trial:
            copy_str = "Trial copy: "

        if not trial:
            os.makedirs(os.path.split(self.dest_path)[0], exist_ok=True)

        msg = copy_str + self.source_path + " -> " + self.dest_path
        self.notify_obj.notify(msg=msg)
        if not trial:
            verifiedcopy.verified_copy_file(self.source_path, self.dest_path)

        if self.sidecar_path:
            msg = copy_str + self.sidecar_path + " -> " + self.sidecar_dest_path
            self.notify_obj.notify(msg=msg)
            if not trial:
                verifiedcopy.verified_copy_file(self.sidecar_path, self.sidecar_dest_path)
            self.notify_obj.notify("")
