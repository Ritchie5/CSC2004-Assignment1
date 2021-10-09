# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
def hash1(filename): 
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash

