x = 'Zntargvp sebz bhgfvqr arne pbeare'
def rot13(x):
For s in x:
    print chr(ord(s) + 13)

A = 65
Z = 90
a = 97
z = 122
z = []
y=list(x)
for i in y:
    z.append(ord(i) + 13))
    if i > 64 and 



z = []
y=list(x)
for i in y:
    if ord(i) > 64 and ord(i) <75:
        z.append(chr(i + 13))
    elif ord(i) > 64 and ord(i) > 74:
        z.append(chr(i - 10))
    print(z)

