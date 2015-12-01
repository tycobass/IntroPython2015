
import os
from os.path import isfile


class AssetChecker():

    searchable_extension = ['jpg']
    ignored_directories = ['__pycache__', '.cache']
    # def __init__(self, *args, **kwargs):
    #     self.starting_search_path = ''

    #     if args is None:
    #         self.starting_search_path = os.getcwd()
    #     else:
    #         self.starting_search_path = args[0]

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

    def find_project_file(self, path):
        '''
        Finds the first file with the .xcodeproj extension and
        returns it
        '''
        project_file_location = ''
        for name in os.listdir(path):
            fullpath = os.path.join(path, name)
            if isfile(fullpath):
                if name.split('.')[1] == 'png':
                    print("hello world")
                    project_file_location = fullpath
            else:
                if name not in self.ignored_directories:
                    return self.find_project_file(fullpath)

        return project_file_location


    def list_files(self, path):
        # returns a list of names (with extension, without full path) of all
        # filesin folder path
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
        return files
