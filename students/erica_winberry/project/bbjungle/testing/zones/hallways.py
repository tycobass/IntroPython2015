# coding=utf-8
"""
The hallways of Parsely High.

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

from __future__ import absolute_import, print_function, division, unicode_literals
import random
from tale.base import Location, Exit, Item, heartbeat, Door
from tale.npc import NPC
from tale.errors import ActionRefused, ParseError, LocationIntegrityError
import tale.lang
from tale.items.basic import Boxlike
import story
from tale.player import Player


def init(driver):
    # called when zone is first loaded
    pass

south_hallway = Location("Hallway (south)", 
    """
    You stand at the south end of a long hallway, flanked by metal lockers.
    """)

north_hallway = Location("Hallway (north)", 
    """
    You are standing at the northern end of a long hallway.
    """)


class Hazard(Door):

    def __init__(self, hazard=True):
        super(Door, self).__init__()
        self.hazard = hazard

    def allow_passage(self, actor):
        """Is the actor allowed to move through this door?"""
        if not self.hazard:
            raise LocationIntegrityError("door not bound", None, self, None)
        if self.hazard:
            story.completion_failed1()
            Player.story_completed()

    def cleaned_up(self):
        self.hazard = False
        return self.hazard


south_hallway.add_exits([
    Exit(["south", "s"], "athletics.gym", "The gymnasium is to the south.",
        "A door to the south of you opens into the Parsely High gymnasium."),
    Exit(["north", "n"], north_hallway, "The hallway continues to the north.",
        "The long, main hallway of Parsely High stretches out to the north of you.")
    ])

room112 = Door(["room 112", "door 112", "english class", "east", "e"], "classrooms.english",  
    short_description="To the east is the door leading to your English class.",
    long_description="To the east is the door leading to your English Class. You see Mr. Bushel giving a lecture on last night's homework. Oops.", 
    locked=False, 
    opened=True)


library_door = Door(["library", "library door", "north", "n"], "classrooms.library", short_description="An open door in the north wall leads to the school library.", 
    locked=False,
    opened=True)

north_hallway.add_exits([
    room112, library_door,
    Exit(["south", "s"], south_hallway,
        "The hallway continues to the south.",
        "The long, main hallway of Parsely High stretches out to the north of you."),
])


class Vomit(Item):

    def allow_item_move(self, actor, verb="move"):
        raise ActionRefused("That's disgusting! You don't want to do that!")


class Hazardous(Door):

    def __init__(self, hazard=True, locked=False, opened=True):
        super(Door, self).__init__(directions, target_location, short_description, long_description)
        self.locked = locked
        self.opened = opened
        self.hazard = hazard
        self.__description_prefix = long_description or short_description
        self.key_code = None   # you can optionally set this to any code that a key must match to unlock the door
        if locked and opened:
            raise ValueError("door cannot be both locked and opened")

    def allow_passage(self, actor):
        """Is the actor allowed to move through this door?"""
        if not self.hazard:
            raise LocationIntegrityError("door not bound", None, self, None)
        if self.hazard:
            story.completion_failed1()
            Player.story_completed()

    def cleaned_up(self):
        self.hazard = False
        return self.hazard

vomit = Vomit(name="puddle", title="puddle of sick", description="puddle of sick in the middle of the corridor; someone appears to have had tummy troubles.")
vomit.add_extradesc({"puddle", "sick", "vomit", "puke"}, 
    """
Someone appears to have had tummy troubles; a puddle of sick lies in the middle of the corridor. 
The puddle is . . . kinda gross. It was Salisbury Steak Day.
    """)

south_hallway.init_inventory([vomit])

english_paper = Item("english homework", "english paper")
english_paper.aliases = {"english paper", "paper", "homework"}
english_paper.add_extradesc({"paper", "english paper", "homework"}, "You paid good money for this!")


class Locker(Boxlike):

    def init(self, locked=True, opened=False, combo="8-16-32"):
        super(Boxlike, self).init()
        self.txt_title_closed = self._title
        self.txt_title_open_filled = self._title
        self.txt_title_open_empty = "empty " + self._title
        self.txt_descr_closed = "The locker is closed."
        self.txt_descr_open_filled = "There's something inside {}.".format(self._title)
        self.txt_descr_open_empty = "There's nothing inside {}.".format(self._title)
        self.locked = locked
        self.opened = opened
        self.combo = combo    # you can optionally set this to any code that a key must match to unlock the door
        if locked and opened:
            raise ValueError("locker cannot be both locked and opened")
        self.aliases = {"locker", "my locker", "your locker", "lock"}
        self.add_extradesc({"locker", "my locker"}, "It's your locker, you think. It's been a while since you've opened it. The lock is your basic, tempered steel, 32-digit combination lock. Very hard to pick! (You've tried.)")
        self.init_inventory([english_paper])

    def allow_item_move(self, actor, verb="move"):
        raise ActionRefused("You can't {} {}".format(verb, self.title))

    def open(self, actor, item=None):
        if self.opened:
            raise ActionRefused("It's already open.")
        elif self.locked:
            actor.tell("You can't open {}, it's locked.".format(self.name))
        else:
            self.opened = True
            actor.tell("You opened {}.".format(self.name))

    def close(self, actor, item=None):
        if not self.opened:
            raise ActionRefused("It's already closed.")
        self.opened = False
        actor.tell("You closed {}.".format(self.name))

    def handle_verb(self, parsed, actor):
        if parsed.verb == "pick":
            if self in parsed.who_info:
                actor.tell("You can't pick the lock! (You've tried.)")
                return True
            elif parsed.who_info:
                raise ActionRefused("You can't pick that.")
            else:
                raise ActionRefused("What do you want to pick?")
        elif parsed.verb == "unlock":
            if self.combo in parsed.args:
                self.locked = False
                actor.tell("That's it! Your locker is now unlocked.")
            elif "16-32-64" in parsed.args:
                raise ActionRefused("The numbers only go up to 32!")
            else:
                raise ActionRefused("If only you could remember your combination!")
            return True
        elif parsed.verb == "lock":
            if self.locked:
                raise ActionRefused("It's already locked.")
            elif self.opened:
                raise ActionRefused("You have to close it first!")
            else:
                self.locked = True
                actor.tell("With a spin of the dial, your locker is locked.")
            return True
        return False

    def insert(self, item, actor):
        if self.opened:
            super(Boxlike, self).insert(item, actor)
        else:
            raise ActionRefused("You can't put things in {}: you should open it first.".format(self.title))

    def remove(self, item, actor):
        if self.opened:
            super(Boxlike, self).remove(item, actor)
        else:
            raise ActionRefused("You can't take things from {}: you should open it first.".format(self.title))


class Readable(Item):

    def read(self, actor, contents=None):
        contents = '"The inevitability of death is a commonly recurring theme in..." blah, blah, blah, blah. Boring.'
        actor.tell(contents)

english_paper = Readable("paper", "english paper")
english_paper.aliases = {"english paper", "paper", "homework"}
english_paper.add_extradesc({"paper", "english paper", "homework"}, "You paid good money for this!")

your_locker = Locker("your locker", "locker")
your_locker.verbs = {
    # register some custom verbs. You can redefine existing verbs, so be careful.
    "pick": "Attempt to pick the lock.",
    "unlock": "Use a combination to unlock the locker.",
    "lock": "Lock the comibnation lock."
}

north_hallway.init_inventory([your_locker])
