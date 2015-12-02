__author__ = 'Max'

import math

class Circle:
    def __init__(self, the_radius):
        self.radius = the_radius

    @property
    def diameter(self):
        return (2*self.radius)

    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2

    @property
    def area(self):
        return (math.pi * (self.radius ** 2))

    @classmethod
    def from_diameter(cls, diameter):
        return Circle(diameter/2)

    def __str__(self):
        return "Circle with radius: {}".format(self.radius)

    def __repr__(self):
        return "Circle({})".format(self.radius)

    def __add__(self, other):
        return Circle(self.radius + other.radius)

    def __mul__(self, mul):
        return Circle(self.radius * mul)

    __rmul__ = __mul__

    def __eq__(self, other):
        return (self.radius == other.radius)

    def __gt__(self, other):
        return (self.radius > other.radius)

    def __lt__(self, other):
        return (self.radius < other.radius)




