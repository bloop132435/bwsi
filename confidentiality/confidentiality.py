# Confidentiality
# 
#  In this lesson you will learn about confidentiality. Good luck!
# ### Challenge Name: caesar_easy (/embsec/confidentiality/caesar_easy)
# 
# 
#         The serial device is sending you a message which includes a ciphertext 
#         encrypted with a caesar cipher! 
#         
#         The message is in the following format:
#     
#         [      0x2       ] [ variable... ] <-- Field Size(s) in Bytes
#         ----------------------------------
#         | Ciphertext Size |  Ciphertext  | <-- Field Name
#         ----------------------------------
#     
#         1. Read the ciphertext size (formatted as a little-endian short) from the serial device
#         2. Read the ciphertext from the serial device
#         3. Decrypt the ciphertext using the key 20 (rotate each letter by 20)
#         4. Send the plaintext back to the device
#         5. Read the flag from the serial device!
#     
#     Hint: Print the decrypted message, it should be in english and make sense!
#     
#     Resources:
#     
#     <https://docs.python.org/3/library/struct.html>
#     
#     <https://en.wikipedia.org/wiki/Caesar_cipher>
#     
#     <http://www.asciitable.com/>
#     
# 
from embsec import Serial

def caesar_easy():
    ser = Serial("/embsec/confidentiality/caesar_easy")
    # Your code goes here!

caesar_easy()
### Challenge Name: caesar_hard (/embsec/confidentiality/caesar_hard)
# 
# 
#         The serial device is sending you a message which includes a ciphertext 
#         encrypted with a caesar cipher! But now...you don't know the key!
#         
#         The message is in the following format:
# 
#         [      0x2       ] [ variable... ] <-- Field Size(s) in Bytes
#         ----------------------------------
#         | Ciphertext Size |  Ciphertext  | <-- Field Name
#         ----------------------------------
# 
#         1. Read the ciphertext size (formatted as a little-endian short) from the serial device
#         2. Read the ciphertext from the serial device
#         3. Do a frequency analysis to recover the secret key
#         3. Decrypt the ciphertext using the recovered key
#         4. Send the plaintext back to the device
#         5. Read the flag from the serial device!
# 
#     Hint: The Counter class in the collections module may come in handy!
# 
#     Resources:
# 
#     <https://docs.python.org/3/library/struct.html>
# 
#     <https://en.wikipedia.org/wiki/Caesar_cipher>
# 
#     <http://www.asciitable.com/>
#     
# 
from embsec import Serial

def caesar_hard():
    ser = Serial("/embsec/confidentiality/caesar_hard")
    # Your code goes here!

caesar_hard()
### Challenge Name: ecb_penguin (/embsec/confidentiality/ecb_penguin)
# 
# 
#         The serial device is sending you a message which includes a gzipped ciphertext 
#         encrypted with AES in ECB mode! The contents of the ciphertext is a PPM image 
#         file with dimensions 6000 (width) x 300 (length). If you fix the header of the
#         encrypted image file you should be able to look at it in an image viewer!
#         
#         The message is in the following format:
# 
#         [           0x4          ] [      variable...   ]  <-- Field Size(s) in Bytes
#         -----------------------------------------------------------------
#         | Gzipped Ciphertext Size |  Gzipped Ciphertext  | <-- Field Name
#         -----------------------------------------------------------------
# 
#         1. Read the ciphertext size (formatted as a little-endian unsigned integer) from the serial device
#         2. Read the gzipped ciphertext from the serial device
#         3. Decompress the ciphertext (note: typically compressing encrypted files have little affect on the size; 
#         however, since we compress an image file encrypted with ECB, many of the blocks are identical!)
#         4. Fix the PPM image header
#         5. Either download the PPM image to view or use Pillow to convert the image to PNG which is viewable in
#         JupyterLab
# 
#     Hint: The Counter class in the collections module may come in handy!
# 
#     Resources:
# 
#     <https://docs.python.org/3/library/struct.html>
#     
#     <https://rosettacode.org/wiki/Bitmap/Write_a_PPM_file>
#     
#      
# 
# 

def ecb_penguin_solution():
    import embsec
    import struct

    import gzip

    ser = embsec.Serial('/embsec/confidentiality/ecb_penguin')

    ct_size, = struct.unpack('<I', ser.read(4))
    ct = gzip.decompress(ser.read(ct_size))

    with open('encrypted_image.pgm', 'wb') as fp:
        fp.write(ct)

    # Your code here! Fix the header of the PPM Image
    # 
    #
    #
    
    from PIL import Image

    im = Image.open("encrypted_image_with_header_mod.pgm")

    im.save("encrypted_image_with_header_mod.png")
### Challenge Name: cbc_corrupt (/embsec/confidentiality/cbc_corrupt)
# 
# 
#     For this challenge the serial device controls a door lock! The serial device
#     will send you a command that is encrypted with AES-128 in CBC mode along with 
#     the initialization vector (IV) that was used for encryption.
#     
#     This initial message is in the following format:
# 
#     [    0x10    ] [      0x10          ]  <-- Field Size(s) in Bytes
#     -------------------------------------
#     |     IV      |  Encrypted Command  |  <-- Field Name
#     -------------------------------------
#     
#     The  encrypted command is as follows: b'DOORLOCKENABLE=1'. Note that the command is 
#     16 bytes and, therefore, fills a single AES-128 block.
#     
#     After you receive the IV and command, the serial device will accept an unlimited
#     number of messages which are composed of an IV and a single encrypted block.
#     
#     These messages should be in the following format:
# 
#     [    0x10    ] [      0x10          ]  <-- Field Size(s) in Bytes
#     -------------------------------------
#     |     IV      |  Encrypted Command  |  <-- Field Name
#     -------------------------------------
#     
#     When the serial device receive a message it will use the provided IV and the
#     original secret key to decrypted the provided encrypted command. Your goal is 
#     for the decrypted command to be b'DOORLOCKENABLE=0' so that the door unlocks!
#     
#     Hint: Look at the block diagram for decryption in CBC mode. How can you use the IV to affect
#     the decrypted plaintext? 
#         
#     Resources:
#     
#     <https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)>
#     
#     <https://en.wikipedia.org/wiki/Bitwise_operation>
#     
# 
# 

def cbc_corrupt_solution():
    import embsec

    def byte_or(ba1, ba2):
        return bytes([_a | _b for _a, _b in zip(ba1, ba2)])

    def byte_and(ba1, ba2):
        return bytes([_a & _b for _a, _b in zip(ba1, ba2)])

    def byte_xor(ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    ser = embsec.Serial('/embsec/confidentiality/cbc_corrupt')
    
    # Your code here!
