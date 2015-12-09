__author__ = 'Max'

"""
some simple tests for the trapz function

designed to run with py.test or nose.
"""

from trapz import trapz
# uncomment to test second version
# from lambda_keyword import function_builder2 as function_builder


def test_line():
    """
    the function should return a list of the length input
    """
    assert trapz(line(5), 0, 10) == 50

    assert trapz(line(6), 0, 10) == 60

    assert trapz(line(10), 0, 10) == 100

def line(x):
    return 5


