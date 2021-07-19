"""
Bootloader Build Tool
This tool is responsible for building the bootloader from source and copying
the build outputs into the host tools directory for programming.
"""
import argparse
import os
import pathlib
import shutil
import subprocess

import secrets
from Crypto.Hash import SHA256

FILE_DIR = pathlib.Path(__file__).parent.absolute()


def copy_initial_firmware(binary_path):
    """
    Copy the initial firmware binary to the bootloader build directory
    Return:
        None
    """
    # Change into directory containing tools
    os.chdir(FILE_DIR)
    bootloader = FILE_DIR / '..' / 'bootloader'
    shutil.copy(binary_path, bootloader / 'src' / 'firmware.bin')


def make_bootloader():
    """
    Build the bootloader from source.
    Return:
        True if successful, False otherwise.
    """

    signature = secrets.token_bytes(256)
    f = open("secret_output.txt", "w")
    f.write(signature.decode() + "\n")
    h = SHA256.new()
    h.update(signature)
    keys = [b"" for _ in range(200)]
    for i in range(200):
        keys[i] = secrets.token_bytes(16)
    bc = open("filename", "r")
    bootloader = []
    x = 0
    for l in bc.readlines():
        if "Write Here" in l:
            # Add key
            index = l.find('""')
            final = l[:index] + keys[x] + l[index:]
            bootloader.append(final)
            x+=1
        else:
            bootloader.append(l)
    for i in range(200):
        f.write(keys[i].decode() + "\n")
    f.close()

    # Change into directory containing bootloader.
    bootloader = FILE_DIR / '..' / 'bootloader'
    os.chdir(bootloader)

    subprocess.call('make clean', shell=True)
    status = subprocess.call('make')

    # Return True if make returned 0, otherwise return False.
    return (status == 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bootloader Build Tool')
    parser.add_argument("--initial-firmware",
                        help="Path to the the firmware binary.",
                        default=None)
    args = parser.parse_args()
    if args.initial_firmware is None:
        binary_path = FILE_DIR / '..' / 'firmware' / 'firmware' / 'gcc' / 'main.bin'
    else:
        binary_path = os.path.abspath(pathlib.Path(args.initial_firmware))

    if not os.path.isfile(binary_path):
        raise FileNotFoundError(
            "ERROR: {} does not exist or is not a file. You may have to call \"make\" in the firmware directory."
            .format(binary_path))

    copy_initial_firmware(binary_path)
    make_bootloader()