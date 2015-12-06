#!/usr/bin/env python3

from Directory_Crawler import hashfile, file_hash_values



def test_hashfile():
    my_hash = hashfile("c:\work_area\Python\Info\loop.py", blocksize = 65536)
    assert my_hash == '40608b9a2d1640de7366edc6db9ed69b'

def test_file_hash_values():
    my_found_duplicates = file_hash_values('c:\work_area\Python\Info\Session_03')
    print (my_found_duplicates)
    assert 'c:\\work_area\\Python\\Info\\Session_03\\maleroom.py' in my_found_duplicates['1b4ab39302d1fc30f31f22ac8e19d3fc']

def test_file_duplicate_value():
    my_found_duplicates = file_hash_values('c:\work_area\Python\Info\Session_03')
    print (my_found_duplicates['93c84386766ee905520b0005a7a3e080'])
    #assert 'c:\\work_area\\Python\\Info\\Session_03\\list_lab_dup.py' in my_found_duplicates['93c84386766ee905520b0005a7a3e080']