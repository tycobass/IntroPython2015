import json
from measurement.measures import volume
from os.path import dirname, realpath
from os import listdir


def main_menu(): # main menu
    menu_choice = input("\nPack List V0.02\n"
                        "---------------\n"
                        "1. Use Existing List\n"
                        "2. Create New List\n"
                        "3. Exit\n\n>>> ")
    if menu_choice == "1":
        use_existing()
    elif menu_choice == "2":
        create_new()
    elif menu_choice == "3":
        exit_pl()
    else:
        print("Not a valid selection, please enter 1, 2, or 3\n\n ")
        main_menu()


def current_lists(): # displays all . josn files in current dir
        print("\nCurrent Lists:\n"
              "--------------")
        for files in listdir(dirname(realpath(__file__))):
            if files.endswith(".json"):
                print(files.strip(".json"))


def use_existing():
    current_lists()
    list_name = input("\nEnter list name: ")
    if list_name + ".json" in listdir(dirname(realpath(__file__))):
        sub_menu(list_name)
    else:
        make_choice = input("\n\aList does not exist, create new list? Y/N ")
        if make_choice.lower() == "y":
            create_new(list_name)
        elif make_choice.lower() == "n":
            main_menu()
        else:
            print("Not a valid selection, returning to main menu.")
            main_menu()


def sub_menu(invlist):
    print("\n" + invlist)
    sub_choice = input("-"*len(invlist)+"\n"
                       "1. View List\n"
                       "2. Edit List\n"
                       "3. Generate Pack List\n"
                       "4. Return To Main Menu\n"
                       "5. Exit Program\n\n>>> ")
    if sub_choice == "1":
        pass
    elif sub_choice == "2":
        pass
    elif sub_choice == "3":
        pack_list()
    elif sub_choice == "4":
        main_menu()
    elif sub_choice == "5":
        exit_pl()
    else:
        pass


def create_new(list_name=None):
    new_list = {}
    if list_name is None:
        list_name = input("\nEnter new list name\n\n>>> ")
    #print("\nType 'Quit' anytime to return main menu.")
    new_item = input("\nEnter item: ")
    new_par = input("\nEnter par: ")
    new_list[new_item] = new_par
    quit_continue = input("\n'Q' to quit and save or 'ENTER' to add item.")
    if quit_continue.lower() == "q":
        main_menu()
    elif quit_continue.lower() != "q":
        create_new(list_name)
    print(list_name,"!!!!")
    #pass


def exit_pl(): # exits program
    print("Exiting Program\n")
    quit()


def pack_list():
    pass


main_menu()

