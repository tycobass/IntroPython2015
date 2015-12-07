#!/usr/bin/env python

"""
Simple iterator examples
"""


class IterateMe_1(object):
    """
    About as simple an iterator as you can get:
    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """
    def __init__(self, start, stop=5, step=1):
        self.current = start - step
        self.stop = stop
        self.step = step
    def __iter__(self):
        return self
    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)