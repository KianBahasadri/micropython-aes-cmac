# micropython-aes-cmac
Run AES using the cryptolib library on micropython. Use a compatible CMAC script without external dependencies.

## Prerequisites
- `NUCLEO_L476RG` Development Board

## Setup
First, make sure the dependencies for Micropython are available on your system.
```
sudo apt-get install build-essential libffi-dev git pkg-config
sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi
pip3 install mpremote # As per usual, its a good idea to use some kind of virtual environment
# For Arch Linux (I use arch btw), the package name for the ARM toolkit is arm-none-eabi-gcc
```

### AES
To run AES, follow the basic steps to set up the Micropython development environment
```
git clone https://github.com/micropython/micropython
cd micropython/mpy-cross
make
cd ../ports/stm32
```

At this point we will add two lines to the file located at `./boards/NUCLEO_L476RG/mpconfigboard.mk`, You can easily do this by running this command:
```
echo -e "MICROPY_PY_SSL = 1\nMICROPY_SSL_MBEDTLS = 1" >> ./boards/NUCLEO_L476RG/mpconfigboard.mk
```

Then continue with the rest of the standard installation procedure.
```
make submodules BOARD=NUCLEO_L476RG
make BOARD=NUCLEO_L476RG
make deploy-stlink BOARD=NUCLEO_L476RG
```

You can now access the AES class in the cryptolib library, here is a demonstration:
```
$ mpremote
Connected to MicroPython at /dev/ttyACM0
Use Ctrl-] or Ctrl-x to exit this shell
MicroPython v1.24.0-preview.47.g88513d122.dirty on 2024-06-20; NUCLEO-L476RG with STM32L476RG
Type "help()" for more information.
>>> import cryptolib
>>> key          = bytes.fromhex("7fb7b598d7e50457438099994907a2f0")
>>> iv           = bytes.fromhex("00000000000000000000000000000000")
>>> encrypted    = bytes.fromhex("03322788ae6db98c963e12c6df1f4019")
>>> cipher       = cryptolib.aes(key, 2, iv)
>>> decrypted    = cipher.decrypt(encrypted)
>>> expected_out = "b4ffeaa4b4293b6d2077a172e095c819"
>>> f"Decryption successful: {decrypted.hex() == expected_out}"
Decryption successful: True
```

### AES-CMAC
After performing the steps to run AES, download cmac.py and run the following command using `mpremote`
```
mpremote cp cmac.py :
```

You can now access the CMAC class in the cmac library, here is a demonstration:
```
$ mpremote
Connected to MicroPython at /dev/ttyACM0
Use Ctrl-] or Ctrl-x to exit this shell
MicroPython v1.24.0-preview.47.g88513d122.dirty on 2024-06-20; NUCLEO-L476RG with STM32L476RG
Type "help()" for more information.
>>> import cmac
>>> key          = bytes.fromhex("7fb7b598d7e50457438099994907a2f0")
>>> message      = bytes.fromhex("b4ffeaa4b4293b6d2077a172e095c819")
>>> cmac         = cmac.CMAC()
>>> mac          = cmac.aes_cmac(key, message)
>>> expected_out = "a53a717d302670eb4970e485c67787be"
>>> f"CMAC valid: {mac.hex() == expected_out}"
CMAC valid: True
```

## Testing
For convenience, I've included two scripts called `cmac-cpython.py` and `aes-cpython.py` which use popular modern implementations of both algorithms. You will have to install the cryptography package with `pip3 install cryptography`. The scripts provide a quick way to compute and test aes and cmac values, which makes them a very convenient tool for running quick tests. Just run them and they will guide you on how to use them.

## References
The code for CMAC was taken from https://github.com/D0ller/CMAC-AES128_for_python3/tree/master and modified.  
The documentation for cryptolib is available at https://docs.micropython.org/en/latest/library/cryptolib.html

## Yapping/Rambling 🗣️🗣️🗣️
1. The documentation for working with Micropython is sorely tangled up, as it so often happens with big and old open source projects. Even the 'Getting Started' page is not obviously shown to you when you go through the documentation, first you go through a bunch of pages about its libraries and details about unimportant information like 'Inline assembler for Thumb2 architectures'. Bro i dont care, get to the point.
2. Secondly, when trying to do as simple as 'implement x algorithm on a development board' i could not find an obvious way to solve the issue. I found like 5 totally different ways of solving the problem and there was not a single clue as to which I should go with. First I tried copying an AES implementation in C and have it compiled and made available in MicroPython. This was a terrible headache which I seriously hope I never have to go through again. Then, I tried compiling it into a .mpy file and getting that to execute on the board which I gave up on probably in less than an hour. On top of all that, I decided to use AES written in pure Micropython and I couldn't even find a SINGLE implementation which didnt have 800 dependencies. WTF!!! I tried a bunch of things and generally had no idea what I was doing the entire time. Micropython project really is an absolute headache for beginners to work with.
3. After I had given up on everything I could think of, I went looking for online help. Personally I've needed to get online help with a lot of computer stuff in the past and I'd say that I know how to find the right people and ask the right questions. Well with Micropython, I quickly found that most embedded hardware engineers have a great disdain for it (I can see why tbh), and don't even have more than preliminary knowledge about it. This was the most frusturating part of all, because it took me maybe 3-4 days to actually get a hold of someone who knew what he was doing, and even then he couldn't figure out what the issue was for a while. In the end he actually managed to figure out how to run the cryptolib library so I really owe the solution of this project to him.

