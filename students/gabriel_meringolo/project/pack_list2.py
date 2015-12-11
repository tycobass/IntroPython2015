import json
from os.path import dirname, realpath, join
from os import listdir
from collections import OrderedDict
from fractions import Fraction
location = dirname(realpath(__file__))


def main_menu():  # main menu
    print(location)
    menu_choice = input("\nPack List V1.0\n---------------\n"
                        "1. Use Existing List\n"  # works
                        "2. Create New List\n"  # works just creates the .json file with name and empty json data
                        "3. Exit\n\n>>> ")  # works
    if menu_choice == "1":
        use_existing()
    elif menu_choice == "2":
        create_new_list(input("\nEnter new list name: "))
    elif menu_choice == "3":
        exit_pl()
    else:
        print("Not a valid selection, please enter 1, 2, or 3\n\n ")
        main_menu()


def current_lists():  # displays all . json files in current dir
        print("\nCurrent Lists:\n--------------")
        for files in listdir(location):
            if files.endswith(".json"):  # searches out .json files
                print(files[:-5])  # removes the .json for ease of reading


def use_existing():
    current_lists()
    list_name = input("\nEnter list name: ")
    if list_name + ".json" in listdir(location):  #adds the .json to the name
        sub_menu(list_name)
    else:
        make_choice = input("\n\aList does not exist, create new list? Y/N ")
        if make_choice.lower() == "y":
            create_new_list(list_name)
        elif make_choice.lower() == "n":
            main_menu()
        else:
            print("Not a valid selection, returning to main menu.")
            main_menu()


def sub_menu(list_name):
    print("\n" + list_name)
    sub_choice = input("-"*len(list_name)+"\n"
                       "1. View List\n"  # works
                       "2. Edit List\n"  # works?
                       "3. Generate Pack List\n"
                       "4. Return To Main Menu\n"  # works
                       "5. Exit Program\n\n>>> ")  # works
    if sub_choice == "1":
        view_list(list_name)
    elif sub_choice == "2":
        edit_list(list_name)
    elif sub_choice == "3":
        pack_list(list_name)
    elif sub_choice == "4":
        main_menu()
    elif sub_choice == "5":
        exit_pl()
    else:
        pass


def view_list(list_name):
    data = read_json(list_name)
    print("\n Item                      Par\n-------------------------------")
    for i in data:
        print("{:<25} {}".format(i + ":", data[i]))
    input("\nHit 'Enter' to continue.\n")
    sub_menu(list_name)


def create_new_list(list_name):
    with open(join(location, "{}.json".format(list_name)), "w") as f:
        json.dump({}, f)  # creates emtpy json file with '{}' in it
    print("\nNew inventory file '{}' created.".format(list_name))
    edit_list(list_name)


def exit_pl(): # exits program
    print("Exiting Program\n")
    quit()


def pack_list(list_name):
    data = read_json(list_name)
    par_check = OrderedDict()
    print("\n")
    for i in data:
        current_amt = input("Current amount of {}: ".format(i))
        if "/" in current_amt:
            current_amt = str(round(float(Fraction(current_amt)), 2))
        par_check[i] = current_amt
    print("\n Pack list for: {}\n".format(list_name) +
          "-----------------" + "-" * len(list_name))
    for i in par_check:
        if float(par_check[i]) >= float(data[i]):
            print("{}: good".format(i))
        elif float(par_check[i]) < float(data[i]):
            print(i + ":", round(float(float(data[i]) - float(par_check[i])), 2))


def edit_list(list_name):
    while True:
        item = input("Enter new item: ")
        par = input("Set par: ")
        if "/" in par:
            par = str(round(float(Fraction(par)),2))
        update_json_file(list_name, item, par)
        if input("\nHit 'ENTER' to input another item,\nor type 'Q' to return to menu.\n>>> ").lower() == "q":
            sub_menu(list_name)


def update_json_file(list_name, item, par):
    data = read_json(list_name)
    data[item] = par
    with open(join(location, "{}.json".format(list_name)), "w") as f:
        json.dump(data, f, indent=4)


def read_json(list_name):
    with open(join(location, "{}.json".format(list_name)), "r") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


if __name__ == "__main__":
    main_menu()

