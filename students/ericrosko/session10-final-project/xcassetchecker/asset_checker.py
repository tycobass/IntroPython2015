#!/usr/bin/env python

import os
from os.path import isfile
import re
import sys

__author__ = 'Eric Rosko'


class AssetChecker():

    ignored_directories = ['__pycache__', '.cache']
    manifest_set = {}
    project_set = {}

    def __init__(self, *args, **kwargs):
        self.starting_search_path = os.getcwd()
        self.searchable_extensions = ['m4a', 'jpg', 'png']

        for item in args:
            if isinstance(item, str):
                self.starting_search_path = item
            elif isinstance(item, list):
                self.searchable_extensions = item
            else:
                raise Exception("Bad Parameter:{}".format(item))

    def search_tree(self, path, files, extensions):
        assert isinstance(extensions, list)

        for name in os.listdir(path):
            fullpath = os.path.join(path, name)

            if isfile(fullpath):
                if name.split('.')[1] in extensions:
                    files.append(name)
            else:
                if name not in self.ignored_directories:
                    self.search_tree(fullpath, files, extensions)

    def get_current_directory(self):
        return os.getcwd()

    def search_project_file_for_assets(self, path, files, extensions):
        pass

    def find_project_file(self, start_path, files):
        '''
        Finds the first file with the .xcodeproj extension and
        returns it
        '''
        # assert os.path.isdir(start_path) == True

        for name in os.listdir(start_path):
            fullpath = os.path.join(start_path, name)

            if not isfile(fullpath) and name not in self.ignored_directories:
                if fullpath.endswith('xcodeproj'):
                    files.append(fullpath)
                else:
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
            regexes.append(re.compile("[A-Za-z0-9_-]+.{}".format(ext)))

        return regexes

    def perform_asset_audit(self):
        temp = []
        self.find_project_file(self.starting_search_path, temp)

        return_string = "\nFound Xcode Project: {}\n".format(
            os.path.basename(temp[0]))
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

        return return_string

    def output_results(self, all=False):

        return_string = ''

        if all:
            return_string += \
            "In Manifest: {}\n\nIn Project Folder: {}\n" \
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
                "actually included in the project:\n{}\n \
                ".format(orphan_assets_inside_folder)

        if len(missing_files_not_in_folder) > 0:
            return_string += \
                "\nFiles outside of the project folder " \
                "referenced in the project file:\n{}\n\n \
                ".format(missing_files_not_in_folder)

        return return_string

if __name__ == '__main__':
    print('\n')
    print('*********************************************************')
    print('*         AssetChecker - for Xcode projects!            *')
    print('*********************************************************')
    print('* Add \'all\' to show all files: ./asset_checker.py all   *')
    print('* Example: ./asset-checker.py all                       *')
    print('*********************************************************')

    total = len(sys.argv)
    cmdargs = str(sys.argv)

    show_all_files = False
    if total == 2 and str(sys.argv[1]) == 'all':
        show_all_files = True
    elif total == 2:
        sys.exit("\nUnknown paramter:{}".format(cmdargs))

    elif total > 2:
        sys.exit("Unknown paramters:{}".format(cmdargs))

    ac = AssetChecker()
    ac.perform_asset_audit()
    results = ac.output_results(show_all_files)
    print(results)
