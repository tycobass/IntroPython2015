x = (2,123.4567, 10000)

y = 'file_{:0>3d} : {:.2f}, {:.1e}'.format(*x)
print(y)






#pt. 2
t = (1,3,6,7,8,4)
x = "{:d}, "
("the first " + str(len(t)) + " numbers are " + (x*len(t))).format(*t)

x.join("the first")
f=[]
for  i in t:
    i =+ 2 + i
    f.append(i)

print("the first %i numbers are")