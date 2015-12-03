#!/usr/bin/env python

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
    assert set(files) == set(['007.jpg', '008.jpg', '001.m4a', '002.m4a',
                              '003.m4a', '004.jpg', '005.jpg', '006.jpg',
                              '009.png', 'icon.png'])


def test_find_project_file():
    fullpath = os.path.join(mypath, 'xcassetchecker')
    files = []
    ac.find_project_file(fullpath, files)
    assert(len(files) == 1, "Expected only one project file")
    location = files[0]
    print(location)
    name, extension = os.path.splitext(location)

    assert extension == '.xcodeproj', "Package file should end with proper" \
        " extension"


def test_find_project_file_default_directory():
    fullpath = os.getcwd()  # os.path.join(mypath, 'xcassetchecker')
    files = []
    ac.find_project_file(fullpath, files)
    assert(len(files) == 1, "Expected only one project file")
    location = files[0]
    print(location)

    name, extension = os.path.splitext(location)

    assert extension == '.xcodeproj', "Package file should end with proper" \
        " extension"
    # assert False


def test_compiled_regexes():
    ac.searchable_extensions = ['jpg']
    regexes = ac.compiled_regexes()
    assert len(regexes) == 1, "Expected one compiled regex"


def test_compiled_regexes_three_args():
    ac.searchable_extensions = ['jpg', 'm4a', 'bmp']
    regexes = ac.compiled_regexes()
    assert len(regexes) == 3, "Expected three compiled regexes"


def test_parse_line():
    ac.searchable_extensions = ['m4a', 'jpg']
    regexes = ac.compiled_regexes()

    line = '        ABF8A2A41C0BD91A0049B539 /* 001.m4a in Resources */ ' \
        '= {isa = PBXBuildFile; fileRef = ABF8A2A11C0BD91A0049B539 ' \
        '/* 001.m4a */; };'

    results = []
    ac.parse_line(line, regexes, results)

    # remove duplicates
    results = list(set(results))

    print(results)
    assert results[0] == '001.m4a'


def test_parse_project_file():
    ac.searchable_extensions = ['m4a']

    results = []
    package_path = "/Users/erosko/Desktop/python/IntroPython2015/students" \
        "/ericrosko/session10-final-project/xcassetchecker/" \
        "xcassetchecker.xcodeproj"

    ac.parse_project_file(package_path, results)

    results = list(set(results))

    assert len(results) == 3
    assert set(results) == set(['002.m4a', '001.m4a', '003.m4a'])
    print("results: ", results)


def test_parse_project_file_for_all_extensions():
    ac.searchable_extensions = ['m4a', 'jpg', 'png']

    results = []
    package_path = os.path.join(os.getcwd(),
                                "xcassetchecker/xcassetchecker.xcodeproj")

    ac.parse_project_file(package_path, results)

    results = list(set(results))

    assert len(results) == 10
    print("results: ", results)
    assert set(results) == set(['009.png', '007.jpg',
                                'outside-of-project.png', '002.m4a',
                                '006.jpg', '005.jpg', '008.jpg', '001.m4a',
                                '003.m4a', '004.jpg'])


def test_perform_asset_audit():
    results = ac.perform_asset_audit()
    print(results)

    assert ac.manifest_set == {'004.jpg', '006.jpg', '005.jpg', '009.png',
                               '007.jpg', '002.m4a', '003.m4a',
                               'outside-of-project.png', '008.jpg', '001.m4a'}
    assert ac.project_set == {'004.jpg', '007.jpg', '008.jpg', '009.png',
                              'icon.png', '001.m4a', '006.jpg', '005.jpg',
                              '002.m4a', '003.m4a'}


def test_output_results():
    ac.perform_asset_audit()
    results = ac.output_results()
    print(results)
    assert False
