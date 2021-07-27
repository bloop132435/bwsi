# FW UPDATE
## Overview
1. [Read in file](#step-1)
2. [Send in chunk](#step-2)
3. [Wait for response](#step-3)
4. [Send zero byte](#step-5)

## Step 1
Read, in lines, the "infile", which was arranged in FW Protect. Each line/chunk includes:
- Length of the chunk (format <h)
- Number corresponding to the key used to encrypt(format <h), 
- Encrypted FW
- Hash (SHA256)
- IV used

## Step 2
Send one line from the infile over serial to the bootloader.

## Step 3
Wait for an OK from the bootloader. If the response is not an OK, raise an error.

## Step 4
Send zero bytes to the bootloader
