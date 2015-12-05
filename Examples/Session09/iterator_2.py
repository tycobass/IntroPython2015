#!/usr/bin/env python

"""
Simple iterator examples
"""


class IterateMe_2(object):
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """
    def __init__(self, start= 0, stop=5, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __getitem__(self, position):
        current = self.start + position * self.step
        if current >= self.stop:
            raise IndexError
        return current

if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_2():
        print(i)

