"""
Firmware Bundle-and-Protect Tool

"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import argparse
import time
import random
import struct
import hashlib


def chunk(message):
    cs = []
    while len(message) > 0:
        size = 128
        if size > len(message):
            size = len(message)
        c = b""
        for i in range(size):
            c += chr(message[i]).encode()
        message = message[size:]
        cs.append(c)
    return cs


def protect_firmware(infile, outfile, version, message):
    # Load firmware binary from infile
    with open(infile, 'rb') as fp:
        firmware = fp.read()

    # Append null-terminated message to end of firmware
    firmware_and_message = firmware + message.encode()
    chunks = chunk(firmware_and_message)
    lines = open("secret_build_output.txt", "rb").readlines()
    signature = lines[0]
    random.seed(time.time())
    kn = random.randint(0, 199)
    keys = lines[1:]
    k = keys[kn]
    aes = AES.new(k, AES.MODE_CBC)
    auth = aes.encrypt(pad(signature, AES.block_size)) + struct.pack("<h", kn)

    # Pack version and size into two little-endian shorts
    metadata = struct.pack('<HHH', version, len(firmware), len(message))

    data = [auth, metadata]
    for c in chunks:
        hash = hashlib.sha256(c).digest()
        l = len(c)
        kn = random.randint(0, 199)
        k = keys[kn]
        a = AES.new(k, AES.MODE_CBC, iv=get_random_bytes(16))
        en = a.encrypt(pad(c, AES.block_size))
        d = b""
        d += struct.pack("<hh", kn, l)
        d += en
        d += hash
        d += a.IV
        data.append(d)

    # Write firmware blob to outfile
    with open(outfile, 'wb+') as outfile:
        outfile.writelines(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firmware Update Tool')
    parser.add_argument("--infile",
                        help="Path to the firmware image to protect.",
                        required=True)
    parser.add_argument("--outfile",
                        help="Filename for the output firmware.",
                        required=True)
    parser.add_argument("--version",
                        help="Version number of this firmware.",
                        required=True)
    parser.add_argument("--message",
                        help="Release message for this firmware.",
                        required=True)
    args = parser.parse_args()

    protect_firmware(infile=args.infile,
                     outfile=args.outfile,
                     version=int(args.version),
                     message=args.message)
