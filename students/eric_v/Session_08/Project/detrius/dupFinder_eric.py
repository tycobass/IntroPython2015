# dupFinder.py
import os, sys
import hashlib
 
def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    counter = 0
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('\n', 'Scanning %s...' % dirName)
        if (subdirs):
            print ('\n', 'subdir being scanned - ', subdirs, '\n\n')
        for filename in fileList:
            counter = counter + 1
            # Get the path to the file

            path = os.path.join(dirName, filename)
            try:
                print (counter, ' - pathname under consideration - ', path)
            except UnicodeEncodeError:
                print ('pathname unprintable')
                pass

                # Calculate hash
            try:
                file_hash = hashfile(path)
                print (counter, ' - file_hash', file_hash, '\n')
            except PermissionError:
                file_hash = 1234
                print('File cannot be hashed, possible corruption - ', path, '\n')
                pass

                # Add or append the file path
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
    return dups
 
 
# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
 
def hashfile(path, blocksize = 65536):
    #afile = open(path,"r",encoding='utf-8')
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
 
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('___________________')
 
    else:
        print('No duplicate files found.')
 
 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        printResults(dups)
    else:
        print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')