# coding=utf-8
"""
The hallways of Parsely High.

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

from __future__ import absolute_import, print_function, division, unicode_literals
import random
import tale.lang
from story import Story
from tale.base import Location, Exit, Item, heartbeat, Door, Living
from tale.npc import NPC
from tale.errors import ActionRefused, ParseError, LocationIntegrityError
from tale.items.basic import Boxlike, Note
from tale.player import Player


def init(driver):
    # called when zone is first loaded
    pass


class GameEnd(Location):
    def init(self):
        pass

    def insert(self, obj, actor):
        # Normally you would use notify_player_arrived() to trigger an action.
        # but for the game ending, we require an immediate response.
        # So instead we hook into the direct arrival of something in this location.
        super(GameEnd, self).insert(obj, actor)
        try:
            obj.story_completed()   # player arrived! Great Success!
        except AttributeError:
            pass


south_hallway = Location("Hallway (south)", 
    """
    You stand at the south end of a long hallway, flanked by metal lockers.
    """)

north_hallway = Location("Hallway (north)", 
    """
    You are standing at the northern end of a long hallway.
    """)

nurses_office = GameEnd("Nurses's Office",
    """
    You wake up in the nurse's office with a terrible headache and blurry vision.
The school nurse decides you should go to the hospital for an MRI, just in case.
The End.
    """)


class Hazard(Door):

    def __init__(self, directions=None, target_location=None, short_description=None, long_description=None, hazard=True):
        super(Door, self).__init__(directions, target_location, short_description, long_description)
        self.hazard = hazard

    def allow_passage(self, actor):
        """Is the actor allowed to move through this door?"""
        if not self.bound:
            raise LocationIntegrityError("door not bound", None, self, None)
        if self.hazard:
            print("You slip in the puddle of sick and fall, cracking your head on a nearby locker. Everything goes black...\n\n")
            Player.move(nurses_office, actor)

    def cleaned_up(self):
        self.hazard = False
        return self.hazard

# class Hazard(Door):
#     """
#     A special exit that connects one location to another but which can be closed or even locked.
#     """
#     def __init__(self, directions, target_location, short_description, long_description=None, locked=True, opened=False):
#         self.locked = locked
#         self.opened = opened
#         self.__description_prefix = long_description or short_description
#         self.key_code = None   # you can optionally set this to any code that a key must match to unlock the door
#         super(Door, self).__init__(directions, target_location, short_description, long_description)
#         if locked and opened:
#             raise ValueError("door cannot be both locked and opened")
#         self.linked_door = None

#     @property
#     def description(self):
#         if self.opened:
#             status = "It is open "
#         else:
#             status = "It is closed "
#         if self.locked:
#             status += "and locked."
#         else:
#             status += "and unlocked."
#         return self.__description_prefix + " " + status

#     def __repr__(self):
#         target = self.target.name if self.bound else self.target
#         locked = "locked" if self.locked else "open"
#         return "<base.Door '%s'->'%s' (%s) @ 0x%x>" % (self.name, target, locked, id(self))

#     def allow_passage(self, actor):
#         """Is the actor allowed to move through this door?"""
#         if not self.bound:
#             raise LocationIntegrityError("door not bound", None, self, None)
#         if not self.opened:
#             raise ActionRefused("You can't go there; it's closed.")

#     def open(self, actor, item=None):
#         """Open the door with optional item. Notifies actor and room of this event."""
#         if self.opened:
#             raise ActionRefused("It's already open.")
#         elif self.locked:
#             raise ActionRefused("You try to open it, but it's locked.")
#         else:
#             self.opened = True
#             actor.tell("You opened it.")
#             actor.tell_others("{Title} opened the %s." % self.name)
#             if self.linked_door:
#                 self.linked_door.door.opened = True
#                 if self.linked_door.open_msg:
#                     self.target.tell(self.linked_door.open_msg)

#     def close(self, actor, item=None):
#         """Close the door with optional item. Notifies actor and room of this event."""
#         pass

#     def lock(self, actor, item=None):
#         """Lock the door with the proper key (optional)."""
#         pass

#     def unlock(self, actor, item=None):
#         """Unlock the door with the proper key (optional)."""
#         if not self.locked:
#             raise ActionRefused("It's not locked.")
#         if item:
#             if self.check_key(item):
#                 key = item
#             else:
#                 raise ActionRefused("You can't use that to unlock it.")
#         else:
#             key = self.search_key(actor)
#             if key:
#                 actor.tell("<dim>(You use your %s; %s matches the lock.)</>" % (key.title, key.subjective))
#             else:
#                 raise ActionRefused("You don't seem to have the means to unlock it.")
#         self.locked = False
#         actor.tell("Your %s fits, it is now unlocked." % key.title)
#         actor.tell_others("{Title} unlocked the %s with %s." % (self.name, lang.a(key.title)))
#         if self.linked_door:
#             self.linked_door.door.locked = False

#     def check_key(self, item):
#         """Check if the item is a proper key for this door (based on key_code)"""
#         key_code = getattr(item, "key_code", None)
#         if self.linked_door:
#             # if this door has a linked door, it could be that the key_code was set on the other door.
#             # in that case, copy the key code from the other door.
#             other_code = self.linked_door.door.key_code
#             if self.key_code is None:
#                 self.key_code = other_code
#             else:
#                 assert self.key_code == other_code, "door key codes must match"
#         return key_code and key_code == self.key_code

#     def search_key(self, actor):
#         """Does the actor have a proper key? Return the item if so, otherwise return None."""
#         for item in actor.inventory:
#             if self.check_key(item):
#                 return item
#         return None

#     def insert(self, item, actor):
#         """used when the player tries to put a key into the door, for instance."""
#         if self.check_key(item):
#             if self.locked:
#                 raise ActionRefused("You could try to unlock the door with it instead.")
#             else:
#                 raise ActionRefused("You could try to lock the door with it instead.")
#         raise ActionRefused("The %s doesn't fit." % item.title)




go_north = Hazard(directions=["north", "n"], target_location=north_hallway, 
    short_description="The hallway continues to the north.")

south_hallway.add_exits([
    go_north,
    Exit(["south", "s"], "athletics.gym", "The gymnasium is to the south.",
        "A door to the south of you opens into the Parsely High gymnasium."),
    Exit(["east", "e"], nurses_office, "The school nurse's office is to the east.")
    ])

room112 = Door(["room 112", "door 112", "english class", "east", "e"], "classrooms.english",  
    short_description="To the east is the door leading to your English class.",
    long_description="To the east is the door leading to your English Class. You see Mr. Bushel giving a lecture on last night's homework. Oops.", 
    locked=False, 
    opened=True)


library_door = Door(["library", "library door", "north", "n"], "classrooms.library", 
    short_description="An open door in the north wall leads to the school library.", 
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

    def search_item(self, actor, item=None):
        """Does the actor have a proper key? Return the item if so, otherwise return None."""
        if item in actor.inventory:
            print("got it!")
            return True
        return None

    def handle_verb(self, parsed, actor):
        if parsed.verb == "clean":
            print(parsed.args)
            if "sawdust" in parsed.args:
                print("recognizes sawdust")
                # for item in actor.inventory:
                if "sawdust" in actor.inventory:
                    print("sawdust in inventory!")
                    actor.tell("You gingerly spread the pink sawdust over the puddle of vomit.")
                    self.remove("sawdust", actor)
                    Hazard.cleaned_up()
                    return True
                else:
                    raise ActionRefused("You don't have any sawdust!")
            elif len(parsed.args) < 2:
                raise ActionRefused("What do you want to clean it up with?")
            else:
                raise ActionRefused("That won't help here.")
        elif parsed.verb == "cover":
            if "sawdust" in parsed.message:
                if self.search_item(actor):
                    actor.tell("You gingerly spread the pink sawdust over the puddle of vomit.")
                    self.remove("sawdust", actor)
                    Hazard.cleaned_up()
                    return True
            else:
                raise ActionRefused("What do you want to cover it with?")
        return False

vomit = Vomit(name="puddle", title="puddle of sick", description="puddle of sick in the middle of the corridor; someone appears to have had tummy troubles.")
vomit.verbs = {
    # register some custom verbs. You can redefine existing verbs, so be careful.
    "clean": "Clean up the puke.",
    "cover": "Clean up the puke."
    # "put": "Put something on something else.",
}
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


class EnglishPaper(Note):

    def init(self):
        super(Note, self).init()
        self._text = '''
        "The inevitability of death is a commonly recurring theme in..." blah, blah, blah, blah. Boring! You stop reading.
        '''

    def read(self, actor):
        actor.tell("The {} reads:".format(self.title), end=True)
        actor.tell(self.text)

english_paper = EnglishPaper("paper", "english paper")
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
