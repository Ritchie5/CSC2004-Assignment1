# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
def hash1(filename): 
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash

print(hash1("D:/GitHub/CSC2004-Assignment1/Scripts/static/encode_output/0_copy.png"))
print(hash1("D:/GitHub/CSC2004-Assignment1/output/random/0.png"))
print(hash1("D:/GitHub/CSC2004-Assignment1/output/random2/0.png"))
# print(hash1("D:\GitHub\CSC2004-Assignment1\Image\smol.png"))
# print(hash1("D:\GitHub\CSC2004-Assignment1\Image\smol2.png"))
