from math import sqrt, ceil


def sum_of_integers():
    total = 0
    x = 1
    while True:
        yield total
        total = total + x
        x += 1


def doubler():
    value = 1
    while True:
        yield value
        doubled = value * 2
        value = doubled


def fibonacci():
    total = 1
    a = 0
    while True:
        yield total
        b = a
        a = total
        total = a + b


def prime_numbers():
    # 2 is the first and only even prime number
    yield 2
    next_number = 3
    prime = True
    while prime:
        # check if next number is divisible by every number between 1
        # and it's own square route.
        for n in range(2, ceil(sqrt(next_number))+1):
            if next_number % n == 0:
                prime = False
        if prime:
            yield next_number
        # only check odd numbers
        next_number += 2
        # restart the loop by setting prime to True
        prime = True



