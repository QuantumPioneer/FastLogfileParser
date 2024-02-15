import lzma
import sys
import tarfile

TAR_XZ_FILENAME = "data.tar.xz"
DIRECTORY_NAME = "data"

if sys.argv[1] == "compress":
    xz_file = lzma.LZMAFile(TAR_XZ_FILENAME, mode="w")
    with tarfile.open(mode="w", fileobj=xz_file) as tar_xz_file:
        tar_xz_file.add(DIRECTORY_NAME)
    xz_file.close()
elif sys.argv[1] == "decompress":
    with tarfile.open("data.tar.xz") as f:
        f.extractall(".")
else:
    print(f"Unrecognized option {sys.argv[1]}, must be either 'compress' or 'decompress'.")
    exit(1)
