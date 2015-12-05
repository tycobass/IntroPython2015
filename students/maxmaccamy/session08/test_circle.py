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
    c = Circle(r)
    assert (areaOfCircle(r) == c.area)

def test_from_diameter():
    c = Circle.from_diameter(6)
    assert (3 == c.radius)
    assert (6 == c.diameter)

def test_str():
    c = Circle(2)
    assert 'Circle with radius:' in str(c)

def test_repr():
    c = Circle(2)
    assert 'Circle(2)' == eval(repr(c))

def test_add():
    c1 = Circle(2)
    c2 = Circle(4)
    newCircle = c1 + c2
    assert (6 == newCircle.radius)
    assert (12 == newCircle.diameter)

def test_mul():
    c = Circle(2)
    c *= 2
    assert (4 == c.radius)
    c = 2 * c
    assert (8 == c.radius)
    assert(areaOfCircle(c.radius) == c.area)

def test_eq():
    c1 = Circle(1)
    c2 = Circle(1)
    c3 = Circle(2)
    assert (c1 == c2)
    assert not (c1 == c3)

def test_gt():
    c1 = Circle(1)
    c2 = Circle(1)
    c3 = Circle(2)
    assert not (c1 > c2)
    assert (c3 > c1)

def areaOfCircle(r):
    return (math.pi * (r ** 2))




