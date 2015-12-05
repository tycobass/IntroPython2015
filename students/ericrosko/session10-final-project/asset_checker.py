#!/usr/bin/env python

'''
Name:       asset_checker.py
Author:     Eric Rosko
Date:       Dec 2015
Python ver. 3.4.3
Xcode ver.  7.1.1


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

    def __init__(self, search_path=None, searchable_extensions=None,
                 show_all_output=None):
        if search_path is None:
            self.search_path = os.getcwd()
        else:
            self.search_path = search_path

        if searchable_extensions is None:
            self.searchable_extensions = ['m4a', 'jpg', 'png', 'ico']
        else:
            self.searchable_extensions = searchable_extensions

        if show_all_output is None:
            self.show_all_output = True
        else:
            self.show_all_output = show_all_output

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

        for name in os.listdir(start_path):
            fullpath = os.path.join(start_path, name)

            if os.path.isdir(fullpath) and \
               name not in self.ignored_directories:
                if fullpath.endswith('xcodeproj'):
                    files.append(fullpath)
                else:
                    self.find_project_file(fullpath, files)

    def parse_project_file(self, path, results):
        assert os.path.isdir(path), "Expected Xcode package file"

        manifest = os.path.join(path, 'project.pbxproj')

        assert os.path.isfile(manifest), "Expected manifest text file"

        regexes = self.compiled_regexes()

        doParse = False

        # We only want to get data from a small section of the pbxproj
        # file.  This is because in a section below it, the terms image.png
        # and image.jpeg are used except these aren't real files in your
        # project.  To avoid accidentally including these false positives,
        # at least for now I'm just parsing the section entitled:
        # /* Begin PBXBuildFile section */
        # /* End PBXBuildFile section */
        # If this script every stops working it will probably be because
        # Apple has changed the format of the project file for this section.
        try:
            with open(manifest, 'r') as f:

                for line in f:
                    line = line.rstrip('\n')
                    if "/* End PBXBuildFile section */" == line:
                        doParse = False
                    elif "/* Begin PBXBuildFile section */" == line:
                        doParse = True

                    if doParse:
                        self.parse_line(line, regexes, results)

        except Exception:
            print("file read failure")

    def parse_line(self, line, regexes, results):
        assert isinstance(results, list)

        count = 0

        for p in regexes:
            count += 1
            found_items = p.findall(line)
            if len(found_items) > 0:
                results.extend(found_items)

    def compiled_regexes(self):
        assert len(self.searchable_extensions) >= 1, "Expected at least " \
            "one searchable extension (jpg, etc)"
        regexes = []

        for ext in self.searchable_extensions:
            # http://www.regexpal.com has a nice online checker :)
            regexes.append(re.compile("[A-Za-z0-9@\._-]+\.{}".format(ext)))

        return regexes

    def perform_asset_audit(self):
        temp = []

        self.find_project_file(self.search_path, temp)

        print("Found Xcode Project: {}".format(os.path.basename(temp[0])))
        assets_in_manifest = []

        self.parse_project_file(temp[0], assets_in_manifest)

        # remove duplicates and save as set
        self.manifest_set = set(assets_in_manifest)

        assets_in_project_folders = []
        folder_to_search = os.path.dirname(temp[0])
        self.search_tree(folder_to_search, assets_in_project_folders,
                         self.searchable_extensions)

        # remove duplicates and save as set
        self.project_set = set(assets_in_project_folders)

    def output_results(self):
        return_string = "Searching for these extensions:{}\n" \
            .format(self.searchable_extensions)

        if self.show_all_output:
            return_string += \
                "\nFiles referenced in the Xcode project manifest: {}\n\n" \
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
    print('**         AssetChecker - for Xcode projects           **')
    print('*********************************************************')
    print('**   Usage and description: ./asset_checker --help     **')
    print('*********************************************************')
    print('')

    total = len(sys.argv)

    # sys.argv is a list
    # print("total: {}".format(total))
    # print("cmdargs", cmdargs)
    # print("what type is sys.argv", type(sys.argv))

    if total == 2 and sys.argv[1] == '--help':
        print(""""
  Usage:
    ./asset_checker.py <path-to-project folder> <extensions> <output_flag>
    ./asset_checker.py /Users/username/your-project-folder
    ./asset_checker.py /Users/username/proj -b
    ./asset_checker.py --brief
    ./asset_checker.py --ext jpg png ico
    ./asset_checker.py /home/user/app --ext jpg png --brief
    ./asset_checker.py /Users/username/project -e jpg png ico

  Description:
  All parameters are optional.  If none are supplied, defaults are used.  If
  no parameters are given the program defaults to the equivalent of:
  ./asset-checker.py ./ --ext m4a jpg png ico

  You can pass the path to your project, or you can run the script from
  inside your Xcode project folder.  It will use the first .xcodeproj file
  it finds.  You can run it from a folder beneath where your Xcode project
  lives.

  You can also provide your own extensions by editing this script or adding
  them after --ext or -e.

  You can put --brief or -b at the end of the list of extensions if you do not
  want it to print out all the items it found in the project and on disk.
              """)

        sys.exit()

    searchable_extensions = None
    show_all_output = None
    search_path = None

    index_of_extension = 0

    for i in range(1, len(sys.argv)):
        if str(sys.argv[i]) == '--brief' or str(sys.argv[i]) == '-b':
            show_all_output = False
        elif i == 1 and os.path.isdir(sys.argv[i]) is True:
            search_path = str(sys.argv[i])
        elif str(sys.argv[i]) == '--ext' or str(sys.argv[i]) == '-e':
            index_of_extension = i

    if index_of_extension > 0:
        searchable_extensions = []
        for sub_index in range(index_of_extension + 1, len(sys.argv)):
            if str(sys.argv[sub_index]) == '--brief' or \
               str(sys.argv[sub_index]) == '-b':
                break
            searchable_extensions.append(str(sys.argv[sub_index]))

    # print("{}\n{}\n{}\n".format(search_path, searchable_extensions,
    #                             show_all_output))

    # sys.exit()

    ac = AssetChecker(search_path=search_path,
                      searchable_extensions=searchable_extensions,
                      show_all_output=show_all_output)

    ac.perform_asset_audit()
    results = ac.output_results()
    print(results)
