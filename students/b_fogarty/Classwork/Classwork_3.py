i = [4,5,'a',5,'z',12,99]
w = ['q',4,'hh','a',5,'z',12,'coffee']

def trans1(x):
    if len(x) >= 3:
        return x[1:len(x)-1]
trans1(i)

def trans2(x):
    y = []
    if len(x) > 2:
        middle = x[1:-1]
        beginning = x[:1]
        end = x[-1:]
        print(end+middle+beginning)
    #print(y)

trans2(w)

# every other
def oth(x):
    x[::2]

assert oth('word') == 'wr'

# reverse
def rev(x):
for item in x:

def thirds(seq):
        f = len(seq)//3
        if i%3:
            return seq[i*2:i]


#listlab
#do it at home
