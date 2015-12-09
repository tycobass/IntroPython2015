from math import pi

from circle import Circle


def test_init():
    Circle(4)


def test_radius():
    c = Circle(4)
    assert c.radius == 4


def test_diameter():
    c = Circle(4)
    assert c.diameter == 8


def test_diameter2():
    c = Circle(2)
    assert c.diameter == 4


def test_set_diameter():
    c = Circle(4)
    c.diameter = 2
    assert c.diameter == 2
    assert c.radius == 1


def test_area():
    c = Circle(2)
    assert c.area == pi * 4


def test_alt_constructor():
    c = Circle.from_diameter(8)
    assert c.diameter == 8
    assert c.radius == 4


def test_str_method():
    c = Circle(8)
    assert c.__str__() == 'Circle with a radius: 8'


def test_repr_method():
    c = Circle(8)
    assert c.__repr__() == 'Circle(8)'


def test_add_two_circles():
    c1 = Circle(2)
    c2 = Circle(4)
    c3 = c1 + c2
    assert c3.radius == 6


def test_multiply_circle():
    c = Circle(2)
    c2 = c * 4
    c3 = 4 * c
    assert c2.radius == 8
    assert c3.radius == 8


def test_cmp():
    c = Circle(1)
    c2 = Circle(2)
    c3 = Circle(3)
    c4 = Circle(2)
    assert c2 == c4
    assert c != c2
    assert c2 > c
    assert c < c3
    assert c2 < c3
    assert c3 > c


def test_sort():
    c1 = Circle(1)
    c2 = Circle(2)
    c5 = Circle(5)
    c8 = Circle(8)
    circles = [c8, c5, c2, c1]
    circles.sort()
    assert circles == [c1, c2, c5, c8]


