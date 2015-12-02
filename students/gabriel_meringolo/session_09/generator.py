

def intsum():
    start = 0
    step = 0
    while start < 20:
        start = (start + step)
        step += 1
        yield start
    return None


def doubler():
    start = 1
    while start < 1000000:
        yield start
        start *= 2
    return None


def fib():
    start, next = 0, 1
    while start < 100:
        yield next
        start, next = next, start + next
    return None


def prime():
    start = 2
    while start < 40:
        yield start
        pass
        pass
        pass
        #2, 3, 5, 7, 11, 13, 17, 19, 23...