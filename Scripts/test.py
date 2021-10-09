from hash1 import hash1, hash2
from os import path 

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "..",
                                  "../static", "uploads", "charmander.jpg"))
print(filepath)
f = open(filepath, "r")

a = hash1(filepath)
print("something")
print(a)
