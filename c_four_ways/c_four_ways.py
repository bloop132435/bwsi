# C four ways
# 
# 
# In this lab we'll be learning all the ways we will run C code in
# this class.
# 
# We'll start out by setting up the development board from TI. Next, we'll play with running
# files compiled for Arm on this x86 machine. For this, we'll use QEMU.
# 
# Remember, we have two types of emulators:
#   - a user level emulator
#   - a system level emulator
# 
# We will use both. For each of these challenges, you will work in a linux terminal to run pre-compiled c
# code. If you run the file correctly, you will get string - send the string you find to the grader, but
# add a newline! If you got the correct string, you will get a flag.
# 
# To run user-level emulation, use the command:
#     `run-arm-user myfile.bin`
# 
# To run system-level emulation, use the command:
#     `run-arm-system myfile.bin`
# 
# To run system-level emulation in a debugger:
#     (1) run `debug-arm-system myfile.bin`
#     (2) in another terminal, run `gdb-remote myfile.axf`
# 
# 
# ### Challenge Name: ti_board (/embsec/c_four_ways/ti_board)
# 
# 
# Follow the instructions from TI to set up your board!
# 
# If you are having difficulty getting your board recognized, try manually installing
# the drivers, from here: https://www.ti.com/lit/zip/slac632
# 
# 
from embsec import Serial

def ti_board():
    ser = Serial("/embsec/c_four_ways/ti_board")
    # Your code goes here!

ti_board()
### Challenge Name: user_level (/embsec/c_four_ways/user_level)
# 
# 
# Run the binary 'user_level.bin', and send it's output to the grader!
# 
# 
from embsec import Serial

def user_level():
    ser = Serial("/embsec/c_four_ways/user_level")
    # Your code goes here!

user_level()
### Challenge Name: system_level (/embsec/c_four_ways/system_level)
# 
# 
# Run the binary 'system_level.bin', and send it's output to the grader!
# 
# hint: Look at UART ...
# 
# 
from embsec import Serial

def system_level():
    ser = Serial("/embsec/c_four_ways/system_level")
    # Your code goes here!

system_level()
### Challenge Name: system_level_debug (/embsec/c_four_ways/system_level_debug)
# 
# 
# Run the binary 'system_level_debug.bin', and send it's output to the grader!
# Hint: you will need to use the debugger...
# 
# 
from embsec import Serial

def system_level_debug():
    ser = Serial("/embsec/c_four_ways/system_level_debug")
    # Your code goes here!

system_level_debug()
