def intsum(): 
    x = 0
    count = 0
    while x < 16:
        yield x
        count += 1
        x += count


def doubler():
    x = 1
    while x < 33:
        yield x
        x = x * 2


def fib():
    n = 1
    oldfib = 1
    yield n
    yield oldfib
    while n < 35:
        newfib = n + oldfib
        yield newfib
        n = oldfib
        oldfib = newfib


def prime():
    count = 2
    comp_list = [2, 3, 5, 7]
    while count < 24:
        if count in comp_list:
            yield count
            count += 1
        else:
            tally = 0
            for i in comp_list:
                if count % i == 0:
                    tally += 1
            if tally == 0:
                yield count
                count += 1
            else: 
                count += 1
