"""
docstrings, because I have to
"""
from math import pi

class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.diam = 2 * radius

    @property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):

    @property
    def area(self):
        return math.pi * radius * 2.0