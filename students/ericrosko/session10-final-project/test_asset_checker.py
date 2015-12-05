#!/usr/bin/env python

"""
AssetChecker tests

Please note that these tests rely on the sample xcode project 'xcassetchecker'
to exist in the same folder as it uses it for the tests.  The 'assets' that
exist, like 009.jpg, were just created using 'touch 009.jpg' so they aren't
valid images in case you are wondering why you can't open them.  This keeps
the size small and assetchecker is just looking for the files and not trying
to open or validate that they are in a one valid format or another.


Requirements:
    You must have py.test installed from http://pytest.org
    python3 -m pip install pytest

Usage:
    py.test -v test-asset-checker.py

"""

import os
import asset_checker

mypath = ''
ac = None


def setup_function(function):
    """
    Runs once before each function in this file.  This is the same as
    XCUnit or CPPUnit testing.
    """
    global mypath
    mypath = os.getcwd()
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

    # note that the cd folder does not contain icon.png
    assert len(files) == len(['004.jpg', '007.jpg', '008.jpg', '009.png',
                              '001.m4a', '006.jpg', '005.jpg',
                              '002.m4a', '003.m4a', 'thumbnail.png',
                              'thumbnail@2x.png', 'thumbnail@3x.png']), \
        "Expected 9 assets in cd folder"


def test_search_tree_search_all_assets_in_xcassetchecker_project():
    files = []
    fullpath = os.path.join(mypath, 'xcassetchecker')
    ac.search_tree(fullpath, files, ['jpg', 'png', 'm4a'])
    print('test_search_tree_search_all_assets_in_xcassetchecker_project',
          files)

    print(files)
    assert len(files) == 13, "Expected 13 assets on disk Xcode project folder"
    assert set(files) == set(['007.jpg', '008.jpg', '001.m4a', '002.m4a',
                              '003.m4a', '004.jpg', '005.jpg', '006.jpg',
                              '009.png', 'icon.png', 'thumbnail.png',
                              'thumbnail@2x.png', 'thumbnail@3x.png',
                              'icon.png'])


def test_find_project_file():
    fullpath = os.path.join(mypath, 'xcassetchecker')
    files = []
    ac.find_project_file(fullpath, files)
    assert len(files) == 1
    location = files[0]
    print(location)
    name, extension = os.path.splitext(location)

    assert extension == '.xcodeproj', "Package file should end with proper" \
        " extension"


def test_find_project_file_default_directory():
    fullpath = os.getcwd()  # os.path.join(mypath, 'xcassetchecker')
    files = []
    ac.find_project_file(fullpath, files)
    assert len(files) == 1, "Expected only one project file"
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
    package_path = \
        os.path.join(mypath, 'xcassetchecker/xcassetchecker.xcodeproj')

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

    print(results)
    assert len(results) == 13, "Expected 13 files in project.pbxproj"
    assert set(results) == set(['009.png', '007.jpg',
                                'outside-of-project.png', '002.m4a',
                                '006.jpg', '005.jpg', '008.jpg', '001.m4a',
                                '003.m4a', '004.jpg', 'thumbnail.png',
                                'thumbnail@2x.png', 'thumbnail@3x.png'])


def test_perform_asset_audit():
    results = ac.perform_asset_audit()
    print(results)

    assert ac.manifest_set == {'004.jpg', '006.jpg', '005.jpg', '009.png',
                               '007.jpg', '002.m4a', '003.m4a',
                               'outside-of-project.png', '008.jpg', '001.m4a',
                               'thumbnail.png', 'thumbnail@2x.png',
                               'thumbnail@3x.png'}
    assert ac.project_set == {'004.jpg', '007.jpg', '008.jpg', '009.png',
                              'icon.png', '001.m4a', '006.jpg', '005.jpg',
                              '002.m4a', '003.m4a', 'thumbnail.png',
                              'thumbnail@2x.png', 'thumbnail@3x.png'}


def test_output_results():
    ac.perform_asset_audit()
    results = ac.output_results()
    print(results)


def test_find_files_on_disk_with_multiple_dots_in_name():
    files = []
    ac.search_tree(os.getcwd(), files, ['gif'])
    print(files)
    assert set(files) == {'filename.with.dots.gif'}


def test_find_files_in_project_file_with_multiple_dots_in_filename():

    line = "   ABF1F6C01C10F9B00018ABFA /* filename.with.dots.gif */ = " \
           "{isa = PBXFileReference; lastKnownFileType = xxx; " \
           "name = filename.with.dots.gif; path = cd/gifs/filename.with." \
           "dots.gif; sourceTree = \"<group>\"; };"

    ac.searchable_extensions = ['gif']
    regexes = ac.compiled_regexes()

    results = []
    ac.parse_line(line, regexes, results)

    # remove duplicates
    results = list(set(results))

    print(results)
    assert results == ['filename.with.dots.gif']


def test_init_with_searchable_extensions():
    a_asset_checker = asset_checker.AssetChecker(searchable_extensions=['gif'])
    assert a_asset_checker.searchable_extensions == ['gif']


def test_init_with_search_path():
    a_asset_checker = asset_checker.AssetChecker(search_path='./home/abc/def')
    assert a_asset_checker.search_path == './home/abc/def'


def test_init_with_show_all_output():
    a_asset_checker = asset_checker.AssetChecker(show_all_output=True)
    assert a_asset_checker.show_all_output is True


def test_init_with_default_values():
    a_asset_checker = asset_checker.AssetChecker()
    assert a_asset_checker.searchable_extensions == \
        ['m4a', 'jpg', 'png', 'ico']
    assert a_asset_checker.search_path == os.getcwd()
    assert a_asset_checker.show_all_output is True
