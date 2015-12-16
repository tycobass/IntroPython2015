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
    def __init__(self, stop=5):
        self.current = -1
        self.stop = stop
    def __iter__(self):
        return self
    def __next__(self):
        self.current += 1
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)
#####

class IterateMe_2(object):
    def __init__(self,start=1,stop=6,step=2):
        self.start = start
        self.stop = stop
        self.step = step
    def __next__(self,position):
        current = self.start + position *self.step
        if current > self.stop:
            raise IndexError
        print(current)


#
        current += self.step
        if self.current < self.stop:
            print(self.current)
        else:
            raise StopIteration

i = IterateMe_2()
for u in i:
    print(u)

