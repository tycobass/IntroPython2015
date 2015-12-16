#list exercise part 1
a = ['Apples','Pears','Oranges','Peaches']
print(a)
r = input('Please type in a new fruit--maybe a tropical one? >')
a.append(r)
print(a)

r2 = input('Pick a number between 1 and 5 >')
if int(r2) > 5:
    r2 = 5
r2 = int(r2) -1
print(a[r2])

"""
['Blueberries'] + a
a.insert(0,'Grapes')

for each in a:
    if each[:1] == 'P':
        print(each)

#continuing pt.2
print(a)
del a[len(a)-1]
print(a)
r3 = input('Which fruit should we drop? >')
a.remove(str(r3))
"""
#pt. 3
r4 = input('Do you like Apples? >')
for f in a:
    r5 = input('Do you like ' + str(f) +'? >')
    while r5.lower() =="no" or r5.lower() =="yes":
        if r5 == "no":
            a.remove(str(f))
        elif r5.lower() == "yes":
            break
    input('Could you make the a "yes" or "no?"')
print(a)

#pt. 4
c = a[:]
c.reverse()
del c[len(c)-1]



