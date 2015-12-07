#!/usr/bin/env python3

from simple_iterator import IterateMe_1

def test_step():
    #IterateMe_1(self, start=-1, stop=5, step=1)
    it = IterateMe_1(2)
    for i in it:
        if i > 10:  break
    print(i)
    assert false