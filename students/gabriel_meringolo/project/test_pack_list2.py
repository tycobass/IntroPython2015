import pack_list2
from os.path import dirname, realpath
from os import listdir
location = dirname(realpath(__file__))


def test_create_new_list(): # need to hash out last line in func to pass test
    pack_list2.create_new_list("cat")
    assert "cat.json" in listdir(location)