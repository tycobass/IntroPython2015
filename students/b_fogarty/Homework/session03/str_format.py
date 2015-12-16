x = (2,123.4567, 10000)

y = 'file_{:0>3d} : {:.2f}, {:.1e}'.format(*x)
print(y)

#pt. 2
t = (1,3,4)
"the first 3 numbers are {:d},{:d},{:d}".format(*t)