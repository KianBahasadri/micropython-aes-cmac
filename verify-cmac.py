from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.backends import default_backend

def compute_cmac(key, message):
    # Create a CMAC object using AES
    c = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    c.update(message)
    return c.finalize()

def verify_cmac(key, message, expected_cmac):
    # Create a CMAC object using AES
    c = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    c.update(message)
    
    # Attempt to verify the CMAC
    try:
        c.verify(expected_cmac)
        return True
    except Exception:
        return False

# Example usage
#key = b"thisiskey1234567"  # AES key must be either 16, 24, or 32 bytes long
#message = b"Hello, World!"  # Message to authenticate
key = b"\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c"
message = b"Your message goes here"

# Compute CMAC
cmac_result = compute_cmac(key, message)
print("CMAC:", cmac_result.hex())

import binascii
cmac_result = binascii.unhexlify(input("what is the cmac?\n")) or cmac_result

# Check CMAC
is_valid = verify_cmac(key, message, cmac_result)
print("Is the CMAC valid?", is_valid)

