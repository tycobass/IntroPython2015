#read file into memory, splitting on carridge returns
slist = open('students.txt','r')
y = slist.read() # now a text file
z = list(y.split('\n')) #now a list
x = []
# with list of students and languages, isolate langages (right of colon)
for i in z:
    s = i[(i.find(':')+2):].split(' ')
    x.append(s) #improved list
#now with list of strings, get single-language list and make it into set for uniqueness
myset = set(sum(x,[]))
#drop empty
myset.discard('')

