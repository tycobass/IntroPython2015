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


