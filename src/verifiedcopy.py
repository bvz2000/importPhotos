import hashlib
import os.path
import shutil


# ----------------------------------------------------------------------------------------------------------------------
def md5_for_file(file_p,
                 block_size=2**20):
    """
    Create an md5 checksum for a file without reading the whole file in in a single chunk.

    :param file_p: The path to the file we are getting a checksum for.
    :param block_size: How much to read in in a single chunk. Defaults to 1MB

    :return: The md5 checksum.
    """

    assert os.path.exists(file_p)
    assert type(block_size) is int

    md5 = hashlib.md5()
    with open(file_p, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)

    return md5.digest()


# ----------------------------------------------------------------------------------------------------------------------
def files_are_identical(file_a_p,
                        file_b_p,
                        block_size=2**20):
    """
    Compares two files to see if they are identical. First compares sizes. If the sizes match, then it does an md5
    checksum on the files to see if they match. Ignores all metadata when comparing (name, creation or modification
    dates, etc.) Returns True if they match, False otherwise.

    :param file_a_p: The path to the first file we are comparing.
    :param file_b_p: The path to the second file we are comparing
    :param block_size: How much to read in in a single chunk when doing the md5 checksum. Defaults to 1MB

    :return: True if the files match, False otherwise.
    """

    assert os.path.exists(file_a_p)
    assert os.path.isfile(file_a_p)
    assert os.path.exists(file_b_p)
    assert os.path.isfile(file_b_p)

    if os.path.getsize(file_a_p) == os.path.getsize(file_b_p):
        md5_a = md5_for_file(file_a_p, block_size)
        md5_b = md5_for_file(file_b_p, block_size)
        return md5_a == md5_b

    return False


# ----------------------------------------------------------------------------------------------------------------------
def verified_copy_file(src,
                       dst):
    """
    Given a source file and a destination, copies the file, and then does a checksum of both files to ensure that the
    copy matches the source. Raises an error if the copied file's md5 checksum does not match the source file's md5
    checksum.

    :param src: The source file to be copied.
    :param dst: The destination file name where the file will be copied. If the destination file already exists, an
           error will be raised. You must supply the destination file name, not just the destination dir.

    :return: Nothing.
    """

    assert os.path.exists(src)
    assert os.path.isfile(src)
    assert os.path.exists(os.path.split(dst)[0])
    assert os.path.isdir(os.path.split(dst)[0])

    shutil.copy(src, dst)

    if not files_are_identical(src, dst):
        msg = "Verification of copy failed (md5 checksums to not match): "
        raise IOError(msg + src + " --> " + dst)
