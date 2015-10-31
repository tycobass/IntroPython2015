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

    for line in source.read().split('\n'):
        try:
            name = line[:line.index(':')] # name = student (what comes before the colon)
        except ValueError:
            print(None)
        try:
            listy = line[line.index(':')+1:].split(' ') # create list of space-delimited languages (what comes after the colon)
        except ValueError:
            print(None)
        for lang in listy:
            if lang not in languages:
                languages[lang] = []
            #print(lang)
            languages[lang] += [name]
    for lang in languages:
        count = len(languages[lang])
      #  print(count)
      #  for numb in languages.values():
      #      count = len(numb)
        print(lang, ':', count)

if __name__ == '__main__':
    print(studlang())


##fix this:
#for lang in languages:
#    print (lang , sum(len(x) for x in lang.values().itervariables()))