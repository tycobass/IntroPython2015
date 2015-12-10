from circle import Circle
from math import pi, isclose

def test_init():
    C = Circle(4)

def test_radius():
    c = Circle(4)
    assert c.radius == 4

def test_diam():
    c = Circle(4)
    assert c.diam == 8

def test_set_diameter():
    c = Circle(4)
    c.diameter = 2
    assert c.diameter == 8

def test_area():
    c = Circle(2)
    print(c.area)
    assert c.area == 12.56637

