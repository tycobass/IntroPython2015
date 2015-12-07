#!/usr/bin/env python3

from Directory_Crawler import hashfile, file_hash_values



def test_hashfile():
    my_hash = hashfile("key_test/key_test.txt", blocksize = 65536)
    assert my_hash == 'd41d8cd98f00b204e9800998ecf8427e'

def test_file_hash_values():
    my_found_duplicates = file_hash_values('key_test')
    print (my_found_duplicates)
    'key_test/frogs.txt' == my_found_duplicates['93c84386766ee905520b0005a7a3e080']
    #assert false