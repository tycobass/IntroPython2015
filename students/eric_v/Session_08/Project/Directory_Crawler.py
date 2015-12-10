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
        for filename in fileList:
            # Assign path to file and filename to filename_path
            filename_path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(filename_path)
            # Add or append the file path
            if file_hash in list_of_files:
                list_of_files[file_hash].append(filename_path)
            else:
                list_of_files[file_hash] = [filename_path]
    return list_of_files