chmod +x dict_lab.py

#dict
d = {'name':'Chris','city':'Seattle','cake':'Chocolate'}
print(d)
del d['cake']
print(d)
d['fruit']= 'Mango'
d.keys()
d.values()
'cake' in d
'Mango' in d
d2 = d.copy()
for i in d2:
    d[i] = i.count('t')


#sets
s2 = set()
for i in range (1,21):
    if i%2 == 0:
        s1.add(i)

s3 = set()
for i in range (1,21):
    if i%3 == 0:
        s3.add(i)

s4 = set()
for i in range (1,21):
    if i%4 == 0:
        s4.add(i)
s2.issubset(s3)
s2.issubset(s4)

#with string
s1 = set()
for i in 'python':
        s1.add(i)

s2 = set()
for i in 'marathon':
        s2.add(i)
s3 = frozenset(s2)

#text parsing

f = open('students.txt','r')
x = f.read()
x.split(":")
x.split("\n")
for l in x:
    c = l[(l.index(":")):]
    q = set()
    q.add(c)
f.close()


