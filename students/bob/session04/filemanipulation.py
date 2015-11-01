#!/usr/bin/python

''' Week 4 Homework:  Paths & File Processing
    - Print the full path to all files in cwd, one/line
    - Write a program to copy a file to another location (don't use shutil or bash)
    -- Copy the file in parts so the program is viable for very large files '''

def fullpath():
    import os
    for (root, dirs, files) in os.walk('.'):  ## from http://www.saltycrane.com/blog/2007/03/python-oswalk-example/
        #print(os.path.abspath(root))  ## print absolute path to top
        #for dir in dirs:
        #    print(os.path.abspath(dir))
        for file in files:
            print(os.path.abspath(file))

fullpath()

#def copyfile():
#    imort os
## eh, maybe later