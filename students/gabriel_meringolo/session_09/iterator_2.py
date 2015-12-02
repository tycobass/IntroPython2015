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
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    #def __iter__(self):
    #    return self

    def __getitem__(self, position):
        current = self.start + position * self.step
        if current > self.stop:
            return IndexError
        return current


    #def __next__(self):
    #    self.current += self.step
    #    if self.current < self.stop:
    #        return self.current
    #    else:
    #        raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    it = IterateMe_1(1, 20)
    for i in it:
        if i > 10:
            break
        print(i)
    for i in it:
        print(i)
