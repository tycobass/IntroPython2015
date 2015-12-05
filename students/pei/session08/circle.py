from math import pi


class Circle:
    def __init__(self, radius):
        self.radius = float(radius)

    @property
    def diameter(self):
        return self.radius*2

    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2.0

    @property
    def area(self):
        return pi*self.radius**2
# step 5
    @classmethod
    def from_diameter (cls, alt_diameter):
        self = cls(alt_diameter / 2)
        return self
# step 6
    def __str__(self):
        return "Circle with radius: " + str(self.radius)

    def __repr__(self):
        return "Circle({})".format(int(self.radius))
# step 7
    def __add__(self, c):
        #assert len(self) == len(c)
        return Circle(self.radius + c.radius)

    def __mul__(self, n):
        return Circle(int(self.radius) * n)

# step 8
    def __gt__(self, c):
        return self.radius > c.radius

    def __eq__(self, c):
        return self.radius == c.radius

# step 9
    #doesn't seem to need to do anything 

        #sorted(self.radius)



















