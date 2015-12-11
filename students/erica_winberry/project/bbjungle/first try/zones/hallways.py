# coding=utf-8
"""
The hallways of Parsely High.
"""

from __future__ import absolute_import, print_function, division, unicode_literals
from tale.base import Item, Location, Exit, Door, Container
import athletics
import classrooms

def init(driver):
    # called when zone is first loaded
    pass


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
your_locker.add_extradesc({"lock"}, "The lock is your basic, tempered steel, 32-digit combination lock. Very hard to pick! (You've tried.)")

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

