#!/usr/bin/env python3

from Directory_Crawler import hashfile, findDup



def test_hashfile():
    my_hash = hashfile("c:\work_area\Python\Info\loop.py", blocksize = 65536)
    assert my_hash == '40608b9a2d1640de7366edc6db9ed69b'

def test_findDup():
    my_found_duplicates = findDup('c:\work_area\Python\Info\Session_03')
    print (my_found_duplicates, '\n')
    assert false