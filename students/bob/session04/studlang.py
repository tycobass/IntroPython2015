#!/usr/bin/python

## Files Lab


'''
open text file, assign to source
dict = dict()
not needed:  manipulate string:  replace ' ' with ',', replace ',,' with ','
stringy = read line from ':' to end; use source.index(':')
listy = stringy.split(' ')
human = read line from 0:source.index(':')
if word in listy isn't in dict, create it.
if word in dict, += dict[name]
for totals, count the names in the values in dict
'''

def studlang():
    '''Read languages from a text file, create a dictionary with
       languages as keys and students as the associated values. 
       Return the list of languages and the number of learners.'''

    #source = open('../../../Examples/students.txt') # we're in 'IntroPython2015/students/bob/session04'
    source = open('./students-clean.txt') # GIGO

    languages = {}

    for line in source.read().split('\n'): ## source.readline() here was only grabbing a single character?
        try:
            name = line[:line.index(':')] # name = student (what comes before the colon)
        except ValueError:
            print('no ":" in your line: ', line)
        try:
            listy = line[line.index(':')+1:].split(' ') # create list of space-delimited languages (what comes after the colon)
        except ValueError:
            print('no ":" in your line: ', line)
        for lang in listy:
            if lang not in languages: # if the language isn't already keyed
                languages[lang] = []  # create it
            languages[lang] += [name] # then add the student (name) to the item
    for lang in languages:
        count = len(languages[lang]) # count number of item's in a lang's value list
        print(count, 'studied', lang)

if __name__ == '__main__':
    print(studlang())