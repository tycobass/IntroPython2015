def counter():
    print('counter: starting counter_again')
    i = -3
    while i < 3:
        i = i + 1
        print('counter: yield', i)
        yield i
    return None

def summer(stop):
    print('summer: starting summer')
    i = 0
    sum = 0
    while i < stop:
        sum += i
        i = i + 1
        print('counter: yield', sum)
        yield sum
    return None


def doubler(stop):
    print('doubler: starting doubler')
    i = 0
    while i < stop:
        sum += i
        i = i + 1
        print('counter: yield', sum)
        yield sum
    return None
#    if __name__ == '__main__':


def sum_generator():
    i=0
    sum = 0
    
#        print ("the generator function:")
 #       print (repr(counter))
 #       print ("call generator function")

#     c = counter()
#     print "the generator:"
#     print repr(c)

#     print 'iterate'
#     for item in c:
#         print 'received:', item
