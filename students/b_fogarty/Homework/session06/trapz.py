#trapz

# this works, strictly speaking, but is limited greatly in its precision
f = lambda x : x*2
def trapz(f,a,b):
    shards = [f(i)*(i-(i-1)) for i in range(a,b)]
    area = sum(shards)
    print(area)



'''
def iter(a,b):
    p = []
    while a < b:
        a += 0.1
        p.append(a)
        print(p[len(p)-2])




'''
m = [((q * 0.1) + q) for q in range(2,200)]

def trapz(f,a,b):
#define range with small increments
    m = [(q * 0.1) for q in range(a,b)]
    part1 = ((b-a)/len(m))
    part2= sum([f(i) for i in m[1:-1]]) + (f(a)+(f(b))/2)
    area = part1 * part2
    print(area)





