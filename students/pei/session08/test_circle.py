from circle import Circle

from math import pi

# from math import isclose, pi

def test_init ():
    C = Circle(4)

def test_attrutes():
    c = Circle(4)
    assert c.radius == 4

def test_diameter():
    c = Circle(4)
    assert c.diameter == 8

def test_diameter2():
    c = Circle(4)
    c.radius = 2
    assert c.diameter == 4

def test_set_diameter():
    c = Circle(4)
    c.diameter = 2
    assert c.diameter == 2
    assert c.radius == 1

def test_area():
    c = Circle(2)
    print(c.area)
    # assert isclose(c.area, 12.56637061, rel_tol = le-6)
    assert c.area ==pi*4

def test_diameterConstructor():
    c = Circle.from_diameter(8)
    assert c.diameter == 8
    assert c.radius == 4

def test_str_repr():
    c = Circle(4)
    assert str(c) == "Circle with radius: 4.0"
    assert repr(c) == "Circle(4)"
    # Question for Chris
    d = eval(repr(c))
    assert d.radius == c.radius
    #assert False

def test_add_circles():
    c1 = Circle(2)
    c2 = Circle(4)
    c3 = c1 + c2
    assert c3.radius == 6.0

def test_mul_circles():
    c1 = Circle(2)
    c2 = c1 * 3
    assert c2.radius == 6.0

def test_compare():
    c1 = Circle(2)
    c2 = Circle(4)
    assert c1 < c2 
    # Question for Chris
    assert not (c1 > c2)

def test_equal():
    c1 = Circle(2)
    c2 = Circle(2)
    assert c1 == c2
    c3 = Circle(3)
    assert not c2 == c3
    assert c2 != c3
    # assert c2 <> c3
def test_sort():
    c = [Circle(6), Circle(7), Circle(0)]
    # question for Chirs
    c.sort()
    assert c == [Circle(0), Circle(6), Circle(7)]
    #pass
