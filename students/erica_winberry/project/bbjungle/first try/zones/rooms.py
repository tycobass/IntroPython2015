# coding=utf-8
"""
The rooms for Blackboard Jungle.
"""

from __future__ import absolute_import, print_function, division, unicode_literals
from tale.base import Item, Location, Exit, Container
from tale.npc import NPC
# from tale.player import Player
from tale.items.basic import BoxLike


def init(driver):
    # called when zone is first loaded
    pass


# --------------------------- START Gym --------------------------------

gym = Location("Gymnasium", "The gymnasium is where the Parsely Greens have their home games. It's currently empty of sweaty athletes and cheering fans.")

# This is a temporary description, figure out how to do this:
gym.add_extradesc({"case", "glasses case", "eyeglasses case"}, "You see someone's eyeglasses case laying on the ground")

# Items

# FIGURE OUT HOW TO OPEN THIS - make an eyeglasses class, for open and closed. - look at the boxlike class

glasses_case = Boxlike("case", "eyeglasses case")
glasses_case.add_extradesc({"case", "glasses case", "eyeglasses case"}, "A simple clamshell case for eyeglasses. It rattles a bit when you shake it -- there's something inside.")
# glasses_case.add_extradesc({"case", "glasses case", "eyeglasses case"}, "An open clamshell case for eyeglasses.")

glasses = Item("glasses", "Pair of ladies' eyeglasses.")
glasses.add_extradesc({"glasses"}, "The horn-rimmed glasses aren't really your style.")

# FIGURE OUT HOW TO SAY THEY MAKE EVERYTHING BLURRY.


# ------------------------- Locker Room  -------------------------------

locker_room = Location("Locker Room", "You are in one of the Parsely High's locker rooms. A door in the west wall leads into the school gymnasium.")
locker_room.add_extradesc({"locker room", "room"}, "This is a stereotypical high school locker room, with banks of tiny lockers in long, narrow rows. It smells of dirty athletic socks and despair.")
locker_room.add_extradesc({"lockers"}, "The lockers are full of other students' nasty gym clothes.")

# FIGURE OUT HOW TO SAY "Why would you want to get into other student's gym clothes!?" when trying to open a locker.

# Items

#  DOES THE CART NEED TO BE A SUBCLASS OF CONTAINER?

cart = Container("cart", "janitor's cart")
cart.add_extradesc({"cart", "janitor's cart"}, "The janitor's cart is more of less a trash can on wheels. A bucket of pink sawdust and a broom hang from the cart.")
cart.add_extradesc({"trash", "trash can"}, "There appears to be a freshman in the trash can.")
cart.add_extradesc({"sawdust"}, "It's pink sawdust, the kind used to soak up spills and messes.")
cart.add_extradesc({"bucket"}, "You see an ordinary blue bucket.")
cart.add_extradesc({"freshman"}, "It's a freshman. They all look the same.")

# bucket = Container("")


# ------------------------- South Hallway  -----------------------------

south_hallway = Location("Hallway (south)", "You stand at the south end of a long hallway, flanked by metal lockers.")

# Items

vomit = Item("puddle", "Someone appears to have had tummy troubles; a puddle of sick lies in the middle of the corridor.")
vomit.add_extradesc({"puddle", "sick", "vomit", "puke"}, "The puddle is...kinda gross. It was Salisbury Steak Day.")

# FIGURE OUT HOW TO MAKE THE PLAYER FALL IF HE DOESN'T PUT THE SAWDUST ON THE VOMIT.


# ------------------------- North Hallway  -----------------------------

north_hallway = Location("Hallway (north)", "You are standing at the northern end of a long hallway.")

# FIGURE OUT HOW TO MAKE THIS LOCKED UNTIL YOU UNLOCK IT. locker should be a subclass of container.
your_locker = Container("locker", "your locker", "Your locker is here.")
your_locker.add_extradesc({"locker", "my locker"}, "It's your locker, you think. It's been a while since you've opened it.")
your_locker.add_extradesc({"lock"}, 
    "The lock is your basic, tempered steel, 32-digit combination lock. Very hard to pick! (You've tried.)")


# ----------------------------- Library --------------------------------

library = Location("Library", "You're in the library, where you usually spend your after-school time in detention.")

# Items

# SINCE THE BOOK NEEDS TO BE READ, DOES IT NEED TO BE A CLASS OF ITS OWN?

cubby = Item("cubby", "study cubby")
cubby.add_extradesc({"cubby", "study cubby"}, "Your typical wooden study cubby. Generations of students in detention have scratched various messages into the aging wood. ")
cubby.add_extradesc({"scratches", "messages"}, "The cubby's wooden desk has a series of numbers freshly scratched into it: 16-32-64.")

book = Item("book", "cryptography for dummies")
book.add_extradesc({"book", "cryptography for dummies"}, "The book's title is Cryptography for Dummies. You remember skimming it during detention yesterday but that was a long time ago.")


# NPCs

# DO I NEED A CUSTOM CLASS FOR INTERACTING WITH HER?
librarian = NPC("School Librarian", "f", race="human", title="School Librarian", description="Ms. Smith, the school librarian.")
librarian.add_extradesc({"librarian", "school librarian"}, "Female, elderly, hair in a bun. Could she be more stereotypical?")


# -------------------------- English Class -----------------------------

english = Location("English Class", "You step into the classroom and your teacher, Mr. Bushel, clears his throat. 'You're late, as usual. I sincerely hope you remembered your homework.' He holds out his hand expectantly.")



# -------------------------- Nurse's Office ----------------------------

nurses_office = Location("Nurse's Office", "You wake up in the nurse's office with a terrible headache and blurry vision. The school nurse decides you should go to the hospital for an MRI, just in case.")


#  Exits

gym.add_exits([
    Exit(["east", "locker room"], locker_room, "You smell a locker room to the east.", "A door in the eastern wall of the gym says 'Locker Room'."),
    Exit(["north", "hall"], south_hallway, "A door in the north wall of the gym leads to the rest of the school.")
])


locker_room.add_exits([
    Exit(["exit", "out", "west", "door"], "The gym is to the west.")
])


south_hallway.add_exits([
    Exit("south", gym, "The gym is to the south.", "A door to the south of you opens into the Parsely High gymnasium."),
    Exit("north", north_hallway, "The hallway continues to the north.", "The long, main hallway of Parsely High stretches out to the north of you.")
])


north_hallway.add_exits([
    Exit("south", south_hallway, "The hallway continues to the south.", "The long, main hallway of Parsely High stretches out to the north of you."),
    Exit(["doorway", "north"], library, "The library is north of you.", "An open doorway in the north wall leads to the school library."),
    Exit(["east", "door", "open"], english, "East is the door leading to your English class.", "To the east is the door leading to your English Class. You see Mr. Bushel giving a lecture on last night's homework. Oops.")
])


south_hallway.add_exits([
    Exit("south", gym, "The gym is to the south.", "A door to the south of you opens into the Parsely High gymnasium."),
    Exit("north", north_hallway, "The hallway continues to the north.", "The long, main hallway of Parsely High stretches out to the north of you.")
])


north_hallway.add_exits([
    Exit("south", south_hallway, "The hallway continues to the south.", "The long, main hallway of Parsely High stretches out to the north of you."),
    Exit(["doorway", "north"], library, "The library is north of you.", "An open doorway in the north wall leads to the school library."),
    Exit(["east", "door", "open"], english, "East is the door leading to your English class.", "To the east is the door leading to your English Class. You see Mr. Bushel giving a lecture on last night's homework. Oops.")
])


