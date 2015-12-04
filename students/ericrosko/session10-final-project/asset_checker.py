#!/usr/bin/env python

'''
Name:       asset_checker.py
Author:     Eric Rosko
Date:       Dec 2015
Written with Python 3.4.3
Parses project file in Xcode 7.1.1

Prerequisites: Xcode 7.1.1, Python 3.4.3

Implementation Details: It is interesting to note that the Xcode framework
libc++.dylib returns false for both os.path.isfile and os.path.isdir.  This is
why in the search_tree method I first check for isfile and then for isdir,
when it seems like just one would have been enough.
'''

import os
from os.path import isfile, isdir
import re
import sys

__author__ = 'Eric Rosko'


class AssetChecker():

    # add any directory names here that you know will not need to be
    # searched for files.  The will be ignored.
    ignored_directories = ['__pycache__', '.cache', '.git']

    # the final list of results are stored in sets, which eliminates
    # any duplicates since sets cannot have the same element twice
    manifest_set = {}
    project_set = {}

    def __init__(self, *args, **kwargs):
        self.starting_search_path = os.getcwd()
        self.searchable_extensions = ['m4a', 'jpg', 'png', 'ico']
        self.show_all_output = False
        for item in args:
            if isinstance(item, str):
                if os.path.isdir(item):
                    self.starting_search_path = item
                elif item == 'all':
                    self.show_all_output = True
            elif isinstance(item, list):
                self.searchable_extensions = item
            else:
                raise Exception("Bad Parameter:{}".format(item))

    def search_tree(self, path, files, extensions):
        assert isinstance(extensions, list)

        try:
            for name in os.listdir(path):
                file_name_parts = name.split('.')
                fullpath = os.path.join(path, name)

                if isfile(fullpath):
                    if len(file_name_parts) > 1 and \
                            file_name_parts[-1] in extensions:
                        files.append(name)
                elif isdir(fullpath):
                    if name not in self.ignored_directories:
                        self.search_tree(fullpath, files, extensions)
        except NotADirectoryError as e:
            print("Not a directory: {}".format(e))
            raise e

        except Exception as e:
            raise e

    def get_current_directory(self):
        return os.getcwd()

    def find_project_file(self, start_path, files):
        '''
        Finds the first file with the .xcodeproj extension and
        returns it
        '''
        # assert os.path.isdir(start_path) == True

        for name in os.listdir(start_path):
            fullpath = os.path.join(start_path, name)
            # print("Fullpath: ", fullpath)
            if os.path.isdir(fullpath) and \
               name not in self.ignored_directories:
                if fullpath.endswith('xcodeproj'):
                    files.append(fullpath)
                else:
                    assert os.path.isdir(fullpath), "Expected Dir!"
                    # print("DIR: ", fullpath)
                    self.find_project_file(fullpath, files)

    def parse_project_file(self, path, results):
        assert os.path.isdir(path), "Expected Xcode package file"

        manifest = os.path.join(path, 'project.pbxproj')
        # print(manifest)
        assert os.path.isfile(manifest), "Expected manifest text file"

        regexes = self.compiled_regexes()

        doParse = False

        # we only want to get data from a small section of the pbxproj
        # file.  This is because in a section below it, the terms image.png
        # and image.jpeg are used except these aren't real files in your
        # project.  To avoid accidentally including these false positives,
        # at least for now I'm just parsing the section entitled
        # /* Begin PBXBuildFile section */
        # /* End PBXBuildFile section */
        try:
            with open(manifest, 'r') as f:

                for line in f:
                    line = line.rstrip('\n')
                    if "/* End PBXBuildFile section */" == line:
                        doParse = False
                    elif "/* Begin PBXBuildFile section */" == line:
                        doParse = True
                    # print(line)
                    if doParse:
                        self.parse_line(line, regexes, results)
                    # print(results)

        except Exception:
            print("file read failure")

        # remove duplicates
        # results = list(set(results))
        # print('end of method len is', len(results), results)

    def parse_line(self, line, regexes, results):
        assert isinstance(results, list)
        # p = re.compile('[A-Za-z0-9_-]+\.m4a')
        # print(type(p))
        count = 0

        for p in regexes:
            # print("loop #", count)
            count += 1
            found_items = p.findall(line)
            if len(found_items) > 0:
                # print("adding")
                results.extend(found_items)
                # print("length: ", len(results))

    def compiled_regexes(self):
        assert len(self.searchable_extensions) >= 1, "Expected at least " \
            "one searchable extension (jpg, etc)"
        regexes = []

        for ext in self.searchable_extensions:
            # special thanks to http://www.regexpal.com !
            regexes.append(re.compile("[A-Za-z0-9@\._-]+\.{}".format(ext)))

        return regexes

    def perform_asset_audit(self):
        temp = []

        self.find_project_file(self.starting_search_path, temp)

        print("\nFound Xcode Project: {}\n".format(os.path.basename(temp[0])))
        assets_in_manifest = []

        self.parse_project_file(temp[0], assets_in_manifest)

        # remove duplicates and save as set
        self.manifest_set = set(assets_in_manifest)

        assets_in_project_folders = []
        folder_to_search = os.path.dirname(temp[0])
        self.search_tree(folder_to_search, assets_in_project_folders,
                         self.searchable_extensions)

        # remove duplicates
        self.project_set = set(assets_in_project_folders)

    def output_results(self):

        return_string = ''

        if self.show_all_output:
            return_string += \
                "Files referenced in the Xcode project manifest: {}\n\n" \
                "Files found inside the project: {}\n" \
                "".format(self.manifest_set, self.project_set)

        orphan_assets_inside_folder = \
            [x for x in self.project_set if x not in self.manifest_set]

        missing_files_not_in_folder = \
            [x for x in self.manifest_set if x not in self.project_set]

        if len(orphan_assets_inside_folder) == 0 and \
           len(missing_files_not_in_folder) == 0:
            return "\nNo missing files.  Looks good!\n"

        if len(orphan_assets_inside_folder) > 0:
            return_string += \
                "\nFiles existing in the project folder not " \
                "referenced by the project:\n{}\n \
                ".format(orphan_assets_inside_folder)
        else:
            return_string += "\nNo un-included files found inside the " \
                "project's folder.\n"

        if len(missing_files_not_in_folder) > 0:
            return_string += \
                "\nFiles missing from the the project folder but " \
                "referenced in the project file:\n{}\n\n \
                ".format(missing_files_not_in_folder)
        else:
            return_string += "\nNo files missing from the project's folder.\n"

        return return_string

if __name__ == '__main__':
    print('\n')
    print('*********************************************************')
    print('*         AssetChecker - for Xcode projects!            *')
    print('*********************************************************')
    print('* Help   : ./asset_checker help                         *')
    print('* Example: ./asset-checker.py all                       *')
    print('* Example: ./asset-checker.py                           *')
    print('*********************************************************')

    total = len(sys.argv)
    cmdargs = str(sys.argv)
    print("total: {}".format(total))
    # print("cmdargs", cmdargs)
    # print(type(list(sys.argv[1])))
    show_all_files = False
    ac = AssetChecker()

    if total == 2 and sys.argv[1] == 'help':
        print("Usage:")
        print("./asset_checker.py /Users/username/your-project-folder")
        print("./asset_checker.py all")
        print("./asset_checker.py ./")
        print("./asset_checker.py --ext jpg png ico")
        print("./asset_checker.py --ext jpg all")
        print("""
  Description:
  You can pass the path to your project.  This will default to only
  showing the problems it finds.  If you pass 'all' as a
  parameter you will also see all files it finds followed by
  any problems listed at the bottom.

  You can also provide your own extension by editing the script or adding them
  after an --ext argument.  You can put 'all' at the end of the list of
  extensions if you want to print out all the items it finds, not just
  the missing or orphaned files.

  I recommended sticking with the usage examples.  If you try to mix and
  match in any possible way it will not work.
              """)
        sys.exit()

    extensions = []

    if total == 2 and str(sys.argv[1]) == 'all':
        show_all_files = True
    elif total == 2 and os.path.isdir(sys.argv[1]):
        ac = AssetChecker(str(sys.argv[1]))
    elif total == 3 and str(sys.argv[1]) == '--ext' \
            and str(sys.argv[2]) == 'all':
        sys.exit("Bad parameter sequence.  " +
                 "Try \'./asset-checker.py help\' to see examples.")
    elif total >= 3 and str(sys.argv[1]) == '--ext':

        for i in range(2, len(sys.argv)):
            if str(sys.argv[i]) == 'all':
                show_all_files = True
            else:
                extensions.append(sys.argv[i])
        ac = AssetChecker(extensions)

    ac.show_all_output = show_all_files
    ac.perform_asset_audit()
    results = ac.output_results()
    print(results)
