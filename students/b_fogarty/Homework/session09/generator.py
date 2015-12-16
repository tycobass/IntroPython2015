def counter():
    print('counter: starting counter')
    i = -3
    while i < 3:
        i = i + 1
        print('counter: yield', i)
        yield i
    return None

def summ(start,stop):
    i = start
    while i < stop:
        yield i
        i += 1

def get_double(start,end=100):
    while start<=end:
        yield start
        start+=start

for z in get_double(3,600):
    print(z)

def add_ints(start,end=100):
    i = 0
    while start<=end:
        yield start
        i +=1
        start +=i
for z in add_ints(3,60):
    print(z)




def get_odds(start,end=100):
    while True:
        if start%2 != 0 and start < end:
            yield start
        start += 1


for z in get_odds(3,10):
    print(z)


# if __name__ == '__main__':
#     print "the generator function:"
#     print repr(counter)
#     print "call generator function"

#     c = counter()
#     print "the generator:"
#     print repr(c)

#     print 'iterate'
#     for item in c:
#         print 'received:', item