#!/usr/bin/env python3

# Directory_Crawler.py
# Author: Eric Vegors
# for Intro to Python class

# Adapted from original and adapted works by:

# http://pythoncentral.io/finding-duplicate-files-with-python/
#Tutorial author: Andres Torres

# https://github.com/IanLee1521/utilities/blob/master/utilities/find_duplicates.py
# Author: Ian Lee

# https://github.com/issteiner/dupliSeek/blob/3ced12da855da28fa35520548f7dfdf602646c89/dupliSeek.py
# Author: issteiner

# http://stackoverflow.com/questions/12565500/finding-duplicate-files-with-python
# Author: mgilson

# Switch commands
# http://www.tutorialspoint.com/python/python_command_line_arguments.htm



import os, sys
import hashlib
import getopt

def hash_identifier(file_path, blocksize = 65536):
    """
    file_path is the path to the specific file which will be hashed
    blocksize is set to a large value to facilitate loading of the file contents
    the contents of the file at the file_path location are hashed and the
        hexidecimal representation of the hash value is returned to
        the calling program.
    """

    file_of_interest = open(file_path, 'rb')
    hash_calculate = hashlib.md5()
    buffer = file_of_interest.read(blocksize)
    while len(buffer) > 0:
        hash_calculate.update(buffer)
        buffer = file_of_interest.read(blocksize)
    file_of_interest.close()
    return hash_calculate.hexdigest()


def file_hash_values(top_level_folder, filename_listing, log_file):
    """
    Use the os.walk method to traverse the top_level_folder provided by user from
        top to bottom evaluating every file.
    Build a full filename path for each file
    Build a md5 hash value for each file
    Add the filename information to a dictionary associated with the top level directory
        being evaluted.  The hash value will of each file will serve as the key and the filename path
        will be the value information.
    The dictionary key is then compared to a running list of keys.  If the key is already contained in the list
        then this file is a duplicate and the filename path will be added to the dictionary value for that key.  If
        the key is not found in the list then the key value pair will be added to the dictionary.  That dictionary,
        called list_of_files is returned from the function.
    There are two exception handlers.
        - Handles case where corrupted file cannot be hashed
        - Handles the case where the filename contains illegal windows filename characters
    """

    list_of_files = {}
    counter = 0
    filename_listing = arguments[0]
    log_file = arguments[1]

    f_listing = open(filename_listing,'w')
    f_log = open(log_file,'w')


    for dirName, subdirs, fileList in os.walk(top_level_folder):
        print('\n', 'Scanning the top level directory %s...' % dirName)
        if (subdirs):
            print ('\n', 'list of sub directories being scanned - ', subdirs, '\n\n')

        for filename in fileList:
            counter += 1

            # Generate the full path to filename that will be hashed,
            # exception handler addresses the case where filename contains illegal Windows filename characters
            file_path = os.path.join(dirName, filename)
            try:
                print (counter, ' - pathname to be hashed - ', file_path, file=f_listing)
            except UnicodeEncodeError:
                print ('pathname unprintable', file=f_log)
                pass

            # Calls the hash calculation
            # Exception handler addresses the case where a corrupted file cannot be hashed
            try:
                file_hash = hash_identifier(file_path)
                print (counter, ' - file_hash', file_hash, '\n', file=f_listing)
            except PermissionError:
                file_hash = 1234
                print('File cannot be hashed, possible corruption - ', file_path, '\n', file=f_log)
                pass

            # Add or append the file path
            if file_hash in list_of_files:
                list_of_files[file_hash].append(file_path)
            else:
                list_of_files[file_hash] = [file_path]

    f_log.close()
    f_listing.close()
    return list_of_files


def joinDictionaries(dictionary1, dictionary2):
    """
    Joins together the results contained in two dictionaries by stepping through the keys.
    """

    for key in dictionary2.keys():
        if key in dictionary1:
            dictionary1[key] = dictionary1[key] + dictionary2[key]
        else:
            dictionary1[key] = dictionary2[key]


def printResults(dictionary1, filename_listing, log_file):
    """
    Use a lambda function to go through the dictionary looking for key/value pairs where the value has two or more
        filename paths strings.
        The duplicate search results are printed.
    """

    results = list(filter(lambda x: len(x) > 1, dictionary1.values()))
    f_listing = open(filename_listing,'w')
    f_log = open(log_file,'w')
    if len(results) > 0:
        print('Potential duplicates found:', file=f_log)
        print('Although the names may differ, the contents are identical', file=f_log)
        print('========================', file=f_log)
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult, file=f_log)
            print('======================', file=f_log)
    else:
        print('No duplicate files found.', file=f_log)
    f_log.close()
    f_listing.close()


def parse_commandline_arguments ():
    """
    Use getopt to parse the command line arguments.
    Expected usage: Directory_Crawler.py -f <filename_listing> -l <log_file> directory1 <directory2> <directory3>
    """

    filename_listing = 'Directory_crawler_listing.txt'
    log_file = 'Directory_crawler_log.txt'


    options, directories = getopt.getopt(sys.argv[1:], 'f:l:', ['filename_listing=',
                                                                                    'log_file=',
                                                                                    ])

    for opt, arg in options:
        if opt in ('-f', '--filename_listing'):
            filename_listing = arg
        elif opt in ('-l', '--log_file'):
            log_file = arg

    return (filename_listing, log_file, directories)


# Main program
# Check for sufficient arguments and assure paths provided can be found
# Initialize list of files
# Iterate through the files append duplicates into the list of files
#
# begin processing

if __name__ == '__main__':

    arguments = parse_commandline_arguments ()
    filename_listing = arguments[0]
    log_file = arguments[1]
    folders = arguments[2]

    if len(folders) >= 1:
        list_of_files = {}
        #folders = directories[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDictionaries(list_of_files, file_hash_values(i, filename_listing, log_file))
            else:
                print('\n', '!!!! Error !!!!')
                print(' %s could not be found, please verify path and try again' % i)
                print('\n', 'Exiting program, good-bye')
                sys.exit()
        printResults(list_of_files, filename_listing, log_file)
    else:
        print('\n', 'Expected usage: python Directory_Crawler.py folder (where folder can be up to three folders)')
        print (' Please try again - Good-bye')