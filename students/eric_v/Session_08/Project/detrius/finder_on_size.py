#!/usr/bin/env python3

# Originally taken from:

# https://github.com/IanLee1521/utilities/blob/master/utilities/find_duplicates.py
# Original Author: Ian Lee

# Changes are
# - globalized hash directories to avoid directory joining
# - some refactoring, renaming, etc

import argparse
import os
import hashlib
import sys

REFFILE_END_MARKER = '|'
filesize_store = {}
filehash_store = {}
filestore4sort = []

refdirfind_is_over = False
verbose_msgs = False
suppress_reference_files = False

def print_if_needed(text):
    if verbose_msgs:
        print(text, end="", flush=True)


def printlf_if_needed(text):
    if verbose_msgs:
        print(text)


def find_samesize_in_folders(folders):
    for actual_folder in folders:
        find_samesize_in_a_folder(actual_folder)


def find_samesize_in_a_folder(folder):

    global filesize_store

    print_if_needed('Gathering files with same size in folder \'{}\'... '.format(folder))

    for dirname, subdirs, filelist in os.walk(folder):
        for filename in filelist:
            fullpath_filename = os.path.join(dirname, filename)
            absolutepath_filename = os.path.abspath(fullpath_filename)
            file_size = os.path.getsize(absolutepath_filename)
            if file_size in filesize_store:
                if absolutepath_filename not in filesize_store[file_size]:  # Avoid false file duplication display in case of very same files (ie. when reference dir is part of dirs)
                     filesize_store[file_size].append(absolutepath_filename)
            else:
                if not refdirfind_is_over:
                    filesize_store[file_size] = [absolutepath_filename]
    
    if 0 in filesize_store.keys():
         del (filesize_store[0])
    printlf_if_needed('Done.')


def put_reffile_end_marker(store):
    for filelist in store.values():
        filelist.append(REFFILE_END_MARKER)


def find_samehash():
    global filehash_store
    print_if_needed('Comparing same size files with md5... ')
    for samesize_file_list in filesize_store.values():
        if len(samesize_file_list) > 2 or len(samesize_file_list) > 1 and not refdirfind_is_over:
            filehash_temp_store = {}
            reffiles = True
            for filename in samesize_file_list:
                if filename != REFFILE_END_MARKER:
                    file_hash = calculate_hash(filename)
                    if file_hash in filehash_temp_store:
                        filehash_temp_store[file_hash].append(filename)
                    else:
                        if reffiles:
                            filehash_temp_store[file_hash] = [filename]
                else:
                    reffiles = False
                    put_reffile_end_marker(filehash_temp_store)
                    
            for actual_hash in filehash_temp_store.keys():
                if len(filehash_temp_store[actual_hash]) > 2 or len(filehash_temp_store[actual_hash]) > 1 and not refdirfind_is_over:
                    filehash_store[actual_hash] = filehash_temp_store[actual_hash]
    printlf_if_needed('Done.')


def calculate_hash(file, blocksize=65536):
    if os.path.isfile(file):
        with open(file, 'rb') as actual_file:
            hasher = hashlib.md5()
            buf = actual_file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = actual_file.read(blocksize)
            return hasher.hexdigest()


def find_duplicated_directories(dir):
    print('Not implemented yet.')


def sort_duplicates():
    global filestore4sort
    if filehash_store != {}:
        for files in filehash_store.values():
            filestore4sort.append(files)
        filestore4sort.sort()


def print_duplicates():
    skip_reffile_print = False
    
    if filestore4sort != []:
        printlf_if_needed('The following duplicate files were found')

        print('-' * 40)
        for samehash_file_list in filestore4sort:
            print_was_before = False
            if REFFILE_END_MARKER in samehash_file_list and suppress_reference_files:
                skip_reffile_print = True

            for filename in samehash_file_list:
                if filename != REFFILE_END_MARKER:
                    if not skip_reffile_print:
                        print_was_before = True
                        try:
                            print(filename)
                        except UnicodeEncodeError:
                            print('There is a problem with filename(s) in folder \'{}\'. Please check and fix.'.format(
                                os.path.dirname(filename)))
                else:
                    if not skip_reffile_print:
                        print(filename)
                    skip_reffile_print = False

            if print_was_before:
                print('-' * 40)
    else:
        printlf_if_needed('No duplicate files found.')


def check_if_dirs_exist(dirlist):
    for actdir in dirlist:
        if not os.path.exists(actdir):
            print('\'{}\' is not a valid path. Please verify!'.format(actdir))
            sys.exit(1)


def main():

    global verbose_msgs
    global refdirfind_is_over
    global suppress_reference_files 
    refdirfind_is_over = False

    parser = argparse.ArgumentParser(description='Find duplicate files or duplicate directories')

    parser.add_argument('-r', '--refdir', metavar='rdir', type=str, nargs=1, required=False,
                        help='Reference directory')
    parser.add_argument('-d', '--dirseek', action='store_true', help='Find duplicate directories')
    parser.add_argument('-v', '--verbose' , action='store_true', help='Print status messages')
    parser.add_argument('-s', '--suppress', action='store_true', help='Suppress file reference printout')
    parser.add_argument('dir', type=str, nargs='+', help='A directory to find for duplicates in')

    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
        parser.print_help()

    check_if_dirs_exist(args.dir)

    if args.verbose:
        verbose_msgs = True
    

    if args.refdir:
        if args.suppress:
            suppress_reference_files = True

        printlf_if_needed('Starting reference directory based duplicate find...')
        check_if_dirs_exist(args.refdir)
        find_samesize_in_a_folder(args.refdir[0])
        put_reffile_end_marker(filesize_store)
        refdirfind_is_over = True
        find_samesize_in_folders(args.dir)
    elif args.dirseek:
        printlf_if_needed('Starting duplicate directory find...')
        find_duplicated_directories(args.dir)
    else:
        printlf_if_needed('Starting normal directory based duplicate find...')
        find_samesize_in_folders(args.dir)

    find_samehash()
    sort_duplicates()
    print_duplicates()


if __name__ == '__main__':
    main()