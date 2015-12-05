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
    def __init__(self, start=0, stop=10, step=1):
        # self.current = start - step  NOTE: Removed along with iter and next.
        self.start = start
        self.stop = stop
        self.step = step

    def __getitem__(self, position=0):
        # Makes this like range
        current = self.start + position * self.step
        if current > self.stop:
            raise IndexError
        return current

    #These two methods make it an iterable:

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     self.current += self.step
    #     if self.current < self.stop:
    #         return self.current
    #     else:
    #         raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_2(2, 20, 2):
        if i > 10:
            break
        print(i)
