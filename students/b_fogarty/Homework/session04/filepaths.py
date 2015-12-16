#printing paths
import os
for i in os.listdir():
    print(os.path.abspath(i))

#early scratchwork
f = open('sherlock_sm.txt')
story = f.read()
x = []
for i in story:
    x.append(i)
print(x)
f.close()


#splitting infile into list, irrespective of length
t = open('sherlock_sm.txt','rb')
outfile = open('sherlock.txt','wb')
chunk = 300
x =[]
while True:
    f = t.read(chunk)
    if len(f) == 0:
        break
    outfile.write(f)
t.close()
outfile.close()



