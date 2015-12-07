import os
import sys
import hashlib

def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def file_hash_values(parentFolder):
    #list_of_file has the format {file hash:[filename with path]}
    list_of_files = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('\n','Scanning - %s...' % dirName, '\n')
        print('\n','Rabbits and cream cheese', '\n')
        for filename in fileList:
            print('file under consideration', filename)
            # Assign path to file and filename to filename_path
            filename_path = os.path.join(dirName, filename)
            print('path of filename under consideration', filename_path)
            # Calculate hash
            file_hash = hashfile(filename_path)
            # Add or append the file path
            if file_hash in list_of_files:
                list_of_files[file_hash].append(filename_path)
            else:
                list_of_files[file_hash] = [filename_path]
    return list_of_files

    # Joins together dictionaries from individual evaluations
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        list_of_files = {}
        folders = sys.argv[1:]
        print('folder considered - ', folders)
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the list_of_files
                joinDicts(list_of_files, file_hash_values(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        printResults(list_of_files)
    else:
        print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')
