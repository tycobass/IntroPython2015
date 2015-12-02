__author__ = 'Max'

"""
some simple tests for the circle.py class

designed to run with py.test or nose.
"""
from circle import Circle
import math

def test_constructor():
    c = Circle(2)

def test_radius():
    c = Circle(2)
    assert (2 == c.radius)

def test_diameter_get():
    c = Circle(2)
    assert (4 == c.diameter)

def test_diameter_set():
    c = Circle(2)
    c.diameter = 6
    assert (6 == c.diameter)
    assert (3 == c.radius)

def test_area():
    r = 2
    area = (math.pi * (r ** 2))
    c = Circle(r)
    assert (area == c.area)

def test_from_diameter():
    c = Circle(2)
    c.from_diameter(6)
    assert (3 == c.radius)
    assert (6 == c.diameter)

def test_str():
    c = Circle(2)
    assert 'Circle with radius:' in str(c)

def test_repr():
    c = Circle(2)
    assert False



