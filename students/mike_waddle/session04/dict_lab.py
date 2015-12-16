
d = {'key1' : 'name','key2' : 'city','key3' : 'cake', 'key4' : 'Chris', 'key5' : 'Seattle','key6' : 'Chocolate'}

print(d.values())
print('Now remove cake')
del d['key3']

print(d.values())

d['fruit'] = 'Mango'

print(d.values())

print(d.keys())

print(d.values())

print('cake' in d)

print('Mango' in d.values())

for t in d:
    print(t)

    












