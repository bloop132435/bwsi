"""
Firmware Bundle-and-Protect Tool

"""
<<<<<<< HEAD
import argparse
import struct
=======
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
        c = struct.pack("<i", size)[:-1]
        for i in range(size):
            c += chr(message[i]).encode()
        message = message[size:]
        cs.append(c)
    return cs
>>>>>>> bfa21e2129d8052dfa7a045ae4fd77455e77775f


def protect_firmware(infile, outfile, version, message):
    # Load firmware binary from infile
    with open(infile, 'rb') as fp:
        firmware = fp.read()

    # Append null-terminated message to end of firmware
    firmware_and_message = firmware + message.encode() + b'\00'
<<<<<<< HEAD

    # Pack version and size into two little-endian shorts
    metadata = struct.pack('<HH', version, len(firmware))

    # Append firmware and message to metadata
    firmware_blob = metadata + firmware_and_message

    # Write firmware blob to outfile
    with open(outfile, 'wb+') as outfile:
        outfile.write(firmware_blob)
=======
    chunks = chunk(firmware_and_message)
    lines = open("secret_build_output.txt", "rb").readlines()
    signature = lines[0]

    # Pack version and size into two little-endian shorts
    metadata = struct.pack('<HHH', version, len(firmware), len(message))

    keys = lines[1:]
    random.seed(time.time())
    data = [signature, metadata]
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
>>>>>>> bfa21e2129d8052dfa7a045ae4fd77455e77775f


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firmware Update Tool')
<<<<<<< HEAD
    parser.add_argument("--infile", help="Path to the firmware image to protect.", required=True)
    parser.add_argument("--outfile", help="Filename for the output firmware.", required=True)
    parser.add_argument("--version", help="Version number of this firmware.", required=True)
    parser.add_argument("--message", help="Release message for this firmware.", required=True)
    args = parser.parse_args()

    protect_firmware(infile=args.infile, outfile=args.outfile, version=int(args.version), message=args.message)
=======
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
>>>>>>> bfa21e2129d8052dfa7a045ae4fd77455e77775f
