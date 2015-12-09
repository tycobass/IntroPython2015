
from circle import Circle
from math import pi, isclose

def test_init():
	c = Circle()

def test_radius():
	c = Circle(4)
	assert c.radius == 4

def test_diameter():
	c = Circle(3)
	c.radius=2
	assert c.diamter==4

def test_area():
	c = Circle(2)
	assert isclose()
	assert c.area = pi*4
