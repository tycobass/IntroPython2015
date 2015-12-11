# coding=utf-8
"""
The hallways of Parsely High.
"""

from __future__ import absolute_import, print_function, division, unicode_literals
from tale.base import Item, Location, Exit, Door, Container
from tale.npc import NPC
import hallways


def init(driver):
    # called when zone is first loaded
    pass

# ----------------------------- Library --------------------------------

library = Location("Library", "You're in the library, where you usually spend your after-school time in detention.")

# Items

# SINCE THE BOOK NEEDS TO BE READ, DOES IT NEED TO BE A CLASS OF ITS OWN?

cubby = Item("cubby", "study cubby", "There is a study cubby here.")
cubby.add_extradesc({"cubby", "study cubby"}, "A typical wooden study cubby. Generations of students in detention have scratched various messages into the aging wood. ")
cubby.add_extradesc({"scratches", "messages"}, "The cubby's wooden desk has a series of numbers freshly scratched into it: 16-32-64.")

book = Item("book", "cryptography for dummies", "There is a book here.")
book.add_extradesc({"book", "cryptography for dummies"}, "The book's title is Cryptography for Dummies. You remember skimming it during detention yesterday but that was a long time ago.")


# NPCs

# DO I NEED A CUSTOM CLASS FOR INTERACTING WITH HER?
librarian = NPC("School Librarian", f, race="human", title="The School Librarian")
librarian.add_extradesc({"librarian", "school librarian"})


# -------------------------- English Class -----------------------------

north_hallway = Location("Hallway (north)", "You are standing at the northern end of a long hallway.")

# FIGURE OUT HOW TO MAKE THIS LOCKED UNTIL YOU UNLOCK IT. locker should be a subclass of container.
your_locker = Container("locker", "your locker", "Your locker is here.")
your_locker.add_extradesc({"locker", "my locker"}, "It's your locker, you think. It's been a while since you've opened it.")
your_locker.add_extradesc({"lock"}, "The lock is your basic, tempered steel, 32-digit combination lock. Very hard to pick! (You've tried.)")


# -------------------------- Nurse's Office ----------------------------

#  Exits

south_hallway.add_exits([
    Exit("south", athletics.gym, "The gym is to the south.", "A door to the south of you opens into the Parsely High gymnasium."),
    Exit("north", north_hallway, "The hallway continues to the north.", "The long, main hallway of Parsely High stretches out to the north of you.")
])


north_hallway.add_exits([
    Exit("south", south_hallway, "The hallway continues to the south.", "The long, main hallway of Parsely High stretches out to the north of you."),
    Exit(["doorway", "north"], classrooms.library, "The library is north of you.", "An open doorway in the north wall leads to the school library."),
    Exit(["east", "door", "open"], classrooms.english, "East is the door leading to your English class.", "To the east is the door leading to your English Class. You see Mr. Bushel giving a lecture on last night's homework. Oops.")
])

