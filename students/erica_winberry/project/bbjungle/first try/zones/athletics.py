# coding=utf-8
"""
The gym, where it begins, and the locker room.
"""

from __future__ import absolute_import, print_function, division, unicode_literals
from tale.base import Item, Location, Exit, Container
from tale.npc import NPC
from tale.player import Player
import hallways


def init(driver):
    # called when zone is first loaded
    pass


# --------------------------- START Gym --------------------------------

gym = Location("Gymnasium", "The gymnasium is where the Parsely Greens have their home games. It's currently empty of sweaty athletes and cheering fans.")

# This is a temporary description, figure out how to do this:
gym.add_extradesc({"case", "glasses case", "eyeglasses case"}, "You see someone's eyeglasses case laying on the ground")


# Items

# FIGURE OUT HOW TO OPEN THIS - make an eyeglasses class, for open and closed. - look at the boxlike class
glasses_case = Container("case", "eyeglasses case", "A simple clamshell case for eyeglasses.")
glasses_case.add_extradesc({"case", "glasses case", "eyeglasses case"}, "It rattles a bit when you shake it -- there's something inside.")
glasses_case.add_extradesc({"case", "glasses case", "eyeglasses case"}, "An open clamshell case for eyeglasses.")

glasses = Item("glasses", "A pair of ladies' eyeglasses.")
glasses.add_extradesc({"glasses"}, "The horn-rimmed glasses aren't really your style.")

# FIGURE OUT HOW TO SAY THEY MAKE EVERYTHING BLURRY.


# ------------------------- Locker Room  -------------------------------

locker_room = Location("Locker Room", """
        You are in one of the Parsely High's locker rooms.
        A door in the west wall leads into the school gymnasium.
    """)
locker_room.add_extradesc({"locker room", "room"}, "This is a stereotypical high school locker room, with banks of tiny lockers in long, narrow rows. It smells of dirty athletic socks and despair.")
locker_room.add_extradesc({"lockers"}, "The lockers are full of other students' nasty gym clothes.")

# FIGURE OUT HOW TO SAY "Why would you want to get into other student's gym clothes!?" when trying to open a locker.

# Items

#  DOES THE CART NEED TO BE A SUBCLASS OF CONTAINER?

cart = Container("cart", "janitor's cart", "There is a janitor's cart here.")
cart.add_extradesc({"cart", "janitor's cart"}, "The janitor's cart is more of less a trash can on wheels. A bucket of pink sawdust and a broom hang from the cart.")
cart.add_extradesc({"trash", "trash can"}, "There appears to be a freshman in the trash can.")
cart.add_extradesc({"sawdust"}, "It's pink sawdust, the kind used to soak up spills and messes.")
cart.add_extradesc({"bucket"}, "You see an ordinary blue bucket.")
cart.add_extradesc({"freshman"}, "It's a freshman. They all look the same.")

# bucket = Container("")

""
# Exits

gym.add_exits([Exit(["east", "locker room"], locker_room, "You smell a locker room to the east.", "A door in the eastern wall of the gym says 'Locker Room'.")])

gym.add_exits([Exit(["north", "hall"], hallways.south_hallway, "A door in the north wall of the gym leads to the rest of the school.")])

locker_room.add_exits(["exit", "out", "west", "door"], "The gym is to the west.")

