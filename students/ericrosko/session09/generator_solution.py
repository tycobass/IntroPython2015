
def intsum():
    total = 0
    for i in range(20):
        total += i
        yield total


def intsum2():
    total = 0
    for i in range(20):
        total += i
        yield total


def doubler():
    total = 1
    for i in range(1, 20):
        yield total
        total = total + total


def fib():
    curr = 1
    prev = 0
    for i in range(100):
        if i == 0:
            yield 1
        elif i == 1:
            yield 1
            curr = 1
            prev = 1
        else:
            yield curr + prev
            temp = curr + prev
            prev = curr
            curr = temp


def prime():
    for i in range(2, 100):
        isPrime = True

        for j in range(2, i):
            if i % j == 0:
                isPrime = False

        if isPrime:
            yield i
