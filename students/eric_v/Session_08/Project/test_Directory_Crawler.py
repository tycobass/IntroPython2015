#!/usr/bin/env python3

import Directory_Crawler as dc


def test_hash_identifier():
    assert dc.hash_identifier('c:\work_area\Python\IntroPython2015\README.rst') == '22f95f67b342722d057a72be249f98a9'

def test_file_hash_values():
    top_level_folder = 'C:\work_area\Python\IntroPython2015\students\eric_v\Session_08\Project\key_test'
    filename_listing = 'Directory_crawler_list.txt'
    log_file = 'Directory_crawler_log.txt'
    test_file = 'C:\work_area\Python\IntroPython2015\students\eric_v\Session_08\Project\key_test\key_test.txt'
    list_of_files = (dc.file_hash_values(top_level_folder, filename_listing, log_file))
    assert list_of_files['d41d8cd98f00b204e9800998ecf8427e'] ==test_file

