#!/usr/bin/env python
"""
Firmware Updater Tool

A frame consists of two sections:
1. Two bytes for the length of the data section
2. A data section of length defined in the length section

[ 0x02 ]  [ variable ]
--------------------
| Length | Data... |
--------------------

In our case, the data is from one line of the Intel Hex formated .hex file

We write a frame to the bootloader, then wait for it to respond with an
OK message so we can write the next frame. The OK message in this case is
just a zero
"""





import argparse
import struct
import time

from serial import Serial

RESP_OK = b'\x00'
FRAME_SIZE = 16

debug = False


def encode(m):
    k = b""
    l = [int(i) for i in m.split(" ")]
    for i in l:
        k += bytes([i])
    return k
    
    
def main(ser, infile, debug):
    
    fp = open(infile, 'r')
    firmware_lines = [encode(i) for i in fp.readlines()]
    count = 0 
    ser.write(b'U')
    resp = b'asdf'
    while resp != b'U':
        resp = ser.read()
        print(resp)
    if debug:
        print("Done handshaking")
    for line in firmware_lines:
        
        ser.write(line)
        
        resp = ser.read()
        time.sleep(0.1)
        # Wait for an OK from the bootloader.
        if resp != RESP_OK:
            raise RuntimeError("ERROR: Bootloader responded with {}".format(repr(resp)))
        
        
        count += 1
        
        print("Line{}: {}".format(count, line.strip()))

    
    print("Done writing firmware.")
    ser.write(struct.pack('>Hh', 0x0000,0x0000))  #send zero bytes 

    
    return ser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firmware Update Tool')

    parser.add_argument("--port", help="Serial port to send update over.",
                        required=True)
    parser.add_argument("--firmware", help="Path to firmware image to load.",
                        required=True)
    parser.add_argument("--debug", help="Enable debugging messages.",
                        action='store_true')
    args = parser.parse_args()

    print('Opening serial port...')
    ser = Serial(args.port, baudrate=115200, timeout=1)
    main(ser=ser, infile=args.firmware, debug=args.debug)

