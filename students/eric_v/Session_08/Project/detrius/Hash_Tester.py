# Hash_Tester.py
import os, sys
import hashlib

def hashfile(phrase, blocksize = 65536):

    hasher = hashlib.md5()
    hasher.update(phrase)
    return hasher.hexdigest()

m = 'Roses are red'
print ('My hashed value is - ', hashfile(m))