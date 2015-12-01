"""
AssetChecker tests

Please note that these tests rely on the sample xcode project 'xcassetchecker'
to exist in the same folder as it uses it for the tests.
"""

import os
import asset_checker


# Module scope variables used for testing.  This helps me refactor out
# repeated values from the test methods to prevent duplication.
mypath = ''
ac = None


# def setup_module(module):
#     """
#     Runs ONCE before all tests run.  Since I'm changing a module-scope
#     variable it is necessary to bring it into this scope using
#     the global keyword.  Not really useful for testing.
#     """

#     global mypath
#     mypath = "/Users/erosko/Desktop/python/IntroPython2015/" \
#              "students/ericrosko/session10-final-project/"


# def teardown_module(module):
#     """
#     Runs ONCE after all the tests in the module run.  Not really useful
#     for testing
#     """
#     global mypath
#     mypath = 'teardown_module'


def setup_function(function):
    """
    Runs once before each function in this file.  This is the same as
    XCUnit or CPPUnit testing.
    """
    global mypath
    mypath = "/Users/erosko/Desktop/python/IntroPython2015/" \
             "students/ericrosko/session10-final-project/"
    global ac
    ac = asset_checker.AssetChecker()


def teardown_function(function):
    """
    Runs once before each function in this file.  This is the same as
    XCUnit or CPPUnit testing.
    """
    global mypath
    mypath = ""
    global ac
    ac = None


def test_get_current_directory():
    assert os.getcwd() == ac.get_current_directory()


def test_search_tree_for_images():
    files = []
    fullpath = os.path.join(mypath, 'xcassetchecker/xcassetchecker/cd/images')
    ac.search_tree(fullpath, files, ['jpg'])
    print(files)
    assert len(files) == 2, "Expected two jpg in images folder"


def test_search_tree_for_sounds_in_sounds_folder():
    files = []
    fullpath = os.path.join(mypath, 'xcassetchecker/xcassetchecker/cd/sounds')
    ac.search_tree(fullpath, files, ['jpg'])
    print(files)
    assert len(files) == 0, "Expected 0 jpg in sounds folder"


def test_search_tree_search_images_in_cd_folder():
    files = []
    fullpath = os.path.join(mypath, 'xcassetchecker/xcassetchecker/cd')
    ac.search_tree(fullpath, files, ['jpg'])
    print(files)
    assert len(files) == 5, "Expected 5 jpg in cd folder"


def test_search_tree_search_all_assets_in_cd_folder():
    files = []
    fullpath = os.path.join(mypath, 'xcassetchecker/xcassetchecker/cd')
    ac.search_tree(fullpath, files, ['jpg', 'png', 'm4a'])
    print(files)

    assert len(files) == 9, "Expected 9 assets in cd folder"


def test_search_tree_search_all_assets_in_xcassetchecker_project():
    files = []
    fullpath = os.path.join(mypath, 'xcassetchecker')
    ac.search_tree(fullpath, files, ['jpg', 'png', 'm4a'])
    print(files)

    assert len(files) == 10, "Expected 10 assets in Xcode project folder"

def test_find_project_file():
    location = ac.find_project_file(mypath)
    print(location)
    assert False
