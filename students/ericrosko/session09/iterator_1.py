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
    def __init__(self, start, stop, step):
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

    # print("Testing the iterator")
    # for i in IterateMe_1(2, 25, 1):
    #     if i > 10:
    #         print("greater than 10")
    #         break

    #     print(i)

    it = IterateMe_1(2, 25, 1)
    for i in it:
        print(i)
        if i > 10:
            break

    for i in it:
        print(i)

    r = range(18)

    for i in r:
        print(i)
        if i > 10:
            break

    for i in r:
        print(i)
