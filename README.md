# micropython-aes-cmac
Run aes using the cryptolib library on micropython. Use a compatible CMAC script without external dependencies.

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
Download cmac.py and run the following command using `mpremote`
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

```

## Testing
For convenience, I've included two scripts called `cmac-cpython.py` and `aes-cpython` which use popular modern implementations of both algorithms. they are supposed to function identially to the micropython implementation, which makes them a convenient tool for running tests.

## References
The code for CMAC was taken from `https://github.com/D0ller/CMAC-AES128_for_python3/tree/master` and modified
The documentation for cryptolib is available at https://docs.micropython.org/en/latest/library/cryptolib.html

## Yapping/Rambling 🗣️🗣️🗣️
points:
- documentation was ass
- tried like 5 different things
- was solved by some guy on discord
- could find little to no online help

