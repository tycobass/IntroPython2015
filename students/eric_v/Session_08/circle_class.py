

"""
A nifty Circle class 

"""

class Circle:

    def __init__(self, radius = None):
     self.radius = radius

    @property
    def diameter(self):
         return (self.radius*2.0)
