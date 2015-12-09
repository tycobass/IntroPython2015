from math import pi


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __str__(self):
        return 'Circle with a radius: {}'.format(self.radius)

    def __repr__(self):
        return 'Circle({})'.format(self.radius)

    def __add__(self, other):
        return Circle(self.radius + other.radius)

    def __mul__(self, other):
        return Circle(self.radius * other)

    # reverse multiplaction returns the same value as __mul__()
    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.radius == other.radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    # only store radius, so attributes don't get out of sync
    # never store computed values

    @property
    def diameter(self):
        return self.radius*2

    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2

    @property
    def area(self):
        return pi * self.radius**2

    # class method as alternate constructor
    @classmethod
    def from_diameter(cls, diameter):
        self = cls(diameter/2)
        return self
