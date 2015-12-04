#!/usr/bin/env python3

"""
circle class 
"""

from math import pi
from math import isclose

# you can also do this
#from math import pi, isclose

class circle(object):
	"""docstring for ClassName"""
	def __init__(self, radius):
		self.radius = radius


	@property
	def diameter(self):
	    return self.radius*2

	@diameter.setter(self,value):
		self.radius = value / 2.0

	@property
	def area(self):
	    return pi * self.raidus  ** 2

TODO  @classmethod lets you make another ctor and pass in a diameter
