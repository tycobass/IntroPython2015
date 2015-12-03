import json
from measurement.measures import volume


#def menu():
#    menu_choice = input("Pack List V 0.01\n"
#          "----------------\n"
#          ""°
#          "1) Set Pars\n"
#          "2) Update Pars\n"
#          "3) View Current Inventory\n"
#          "4) View Pack List\n"
#          "5) Quit\n\n>>> ")
#    if menu_choice == "1":
#        set_pars()
#    elif menu_choice == "2":
#        update_pars()
#    elif menu_choice == "3":
#        view_inv()
#    elif menu_choice == "4":
#        view_packlist()
#    elif menu_choice == "5":
#        quit_pl()
#    else:
#        print("Not a valid selection, please select 1, 2, 3, 4, or 5 to quit.")
#
#
#def set_pars():
#    pass
#
#
#def update_pars():
#    pass
#
#
#def view_inv():
#    pass
#
#
#def view_packlist():
#    pass
#
#
#def quit_pl():
#    quit()


def main_menu():
    menu_choice = input("Pack List V0.02\n"
                        "---------------\n"
                        "1. Use Existing List\n"
                        "2. Create New List\n"
                        "3. Exit\n\n>>> ")
    if menu_choice == "1":
        pass
    elif menu_choice == "2":
        pass
    elif menu_choice == "3":
        exit_pl()
    else:
        print("Not a valid selection, please enter 1, 2, or 3\n\n ")
        main_menu()


def exit_pl():
    print("Exiting program\n")
    quit()


main_menu()