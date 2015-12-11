import json
from collections import OrderedDict
from fractions import Fraction
#def create_new(list_name):
#    new_file = open("{}.json".format(list_name), "w")
#    new_file.close()
#    print("New inventory file '{}' created.".format(list_name))
#
#print(create_new("canyy"))
#
#
#def edit_list(list_name):
#    new_list = {}
#    if list_name is None:
#        list_name = input("\nEnter new list name\n\n>>> ")
#    new_item = input("\nEnter item: ")
#    new_par = input("\nEnter par: ")
#    new_list[new_item] = new_par
#    quit_continue = input("\n'Q' to quit and save or 'ENTER' to add item.")
#    if quit_continue.lower() == "q":
#        main_menu()
#    elif quit_continue.lower() != "q":
#        create_new(list_name)

#import json
#a = json.dumps({"a": 1, "b": 2})
#print(a)
#print(json.loads(a))



#def edit_list(list_name):
#    while True:
#        item = input("Enter new item: ")
#        par = input("Set par: ")
#        update_json_file(list_name, item, par)
#        if input("'ENTER' to input another item,\n 'Q' to return to main menu\n>>> ").lower() == "q"
#            main_menu()

with open("AAG.json", "r") as f:
    aag_inv = json.load(f,object_pairs_hook=OrderedDict)
#print(" Item                      Par\n"
#      "-------------------------------")
par_check = OrderedDict()
for i in aag_inv:
    current_amt = input("Current amount of {}: ".format(i))
    if "/" in current_amt:
        current_amt = str(round(float(Fraction(current_amt)),2))
    par_check[i] = current_amt
print("\n")
for i in par_check:
    if float(par_check[i]) >= float(aag_inv[i]):
        print(i, "good")
    elif float(par_check[i]) < float(aag_inv[i]):
        print(i, float(aag_inv[i]) - float(par_check[i]))  ### need to print 'good' if over, want to use different measures


### use generator expresions for this!?
### use *args for the par ammount? it will be set in a tuple and can use teh volume later?