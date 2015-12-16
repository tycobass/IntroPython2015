# coding=utf-8
"""
The central town, which is the place where mud players start/log in

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

from __future__ import absolute_import, print_function, division, unicode_literals
from tale.base import Location, Exit, Item, Container, Living, Key
from tale.npc import NPC
from tale.player import Player
from tale.errors import ActionRefused
from tale.items.basic import Boxlike, Wearable
from tale import pubsub
from tale import lang

pending_actions = pubsub.topic("driver-pending-actions")

def init(driver):
    # called when zone is first loaded
    # board.load()
    pass

gym = Location("Gymnasium",
    """
    The gymnasium is where the Parsely Greens have their home games.
    It's currently empty of sweaty athletes and cheering fans.
    """)

locker_room = Location("Locker Room",
    """
    You are in a stereotypical high school locker room.
    It smells of dirty athletic socks and despair.
    """)

gym.add_exits([
    Exit(["east", "locker room", "e"],
        locker_room,
        "You smell a locker room to the east.",
        "A door in the eastern wall of the gym says 'Locker Room'."),
    Exit(["north", "hall", "n"], 
        "hallways.south_hallway",
        "Parsely High is to the north",
        "A door in the north wall of the gym leads to the rest of the school.")
])

locker_room.add_exits([
    Exit(["exit", "out", "west", "door", "w"],
        gym,
        "The gym is to the west.",
        "To the west you can see Parsely High's gymnasium.")
])


class GlassesCase(Boxlike):
    def init(self):
        super(Boxlike, self).init()
        self.opened = False
        self.txt_title_closed = self._title
        self.txt_title_open_filled = self._title
        self.txt_title_open_empty = "empty " + self._title
        self.txt_descr_closed = "The {} is shut.".format(self.name)
        self.txt_descr_open_filled = "It is an open."
        self.txt_descr_open_empty = "It is an open."

    def allow_item_move(self, actor, verb="move"):
        pass


class UntakableContainer(Container):
    def allow_item_move(self, actor, verb="move"):
        raise ActionRefused("You can't {} {}.".format(verb, self.title))

    # def insert(self, item, actor):
    #     if self.opened and item is "glasses":
    #         super(Boxlike, self).insert(item, actor)
    #     else:
    #         raise ActionRefused("No matter how hard you try, you can't fit {} in the box.".format(item.title))

class Glasses(Wearable):
        
    def init(self, wearing=False):
        super(Glasses, self).init()
        self.wearing = wearing

    def wearing_glasses(self):
        while self.wearing:
            pass

    def vision_problems(self):
        pass


glasses = Item("glasses", "glasses", "pair of ladies eyeglasses.")
glasses.aliases = {"glasses"}
glasses.add_extradesc({"glasses"}, "The horn-rimmed glasses aren't really your style.")

glasses_case = GlassesCase("case", "clamshell case for eyeglasses")
glasses_case.aliases = {"case", "clamshell case", "eyeglasses case"}
glasses_case.init_inventory([glasses])

gym.init_inventory([glasses_case])

class MovableObject(Boxlike):

    def allow_item_move(self, actor, verb="take"):
        raise ActionRefused("You can't {} {}.".format(verb, self.title))

    def move(self, target, actor=None, silent=False, is_player=False, verb="move"):
        """
        Leave the current location, enter the new location (transactional).
        """
        actor = actor or self
        original_location = None
        if self.location:
            original_location = self.location
            self.location.remove(self, actor)
            try:
                target.insert(self, actor)
            except:
                # insert in target failed, put back in original location
                original_location.insert(self, actor)
                raise
           # # queue event
           #  if is_player:
           #      pending_actions.send(lambda who=self, where=target: original_location.notify_player_left(who, where))
           #  else:
           #      pending_actions.send(lambda who=self, where=target: original_location.notify_npc_left(who, where))
        else:
            target.insert(self, actor)
        # queue event
        # if is_player:
        #     pending_actions.send(lambda who=self, where=original_location: target.notify_player_arrived(who, where))
        # else:
        #     pending_actions.send(lambda who=self, where=original_location: target.notify_npc_arrived(who, where))

    def handle_verb(self, parsed, actor):
        if parsed.verb in ("move", "push"):
            xt = parsed.args[-1]
            for d, e in self.location.exits.items():
                if e.target.exits:
                    print(e.target)
                    if xt in d:
                        print("match found!")
                        try:
                            self.move(str(e.target))
                        except:
                            print("Not it.")
                #     try:
                #     actor.tell("You {} the janitor's cart along ahead of you.".format(parsed.verb))
                #     self.move(target=xt)
                #     Player.move(target=xt)
                #             xt.allow_passage(self)
                #         except ActionRefused:
                #             continue
                #     else:
                #         return xt
                # return None
                #         actor.tell("You {} the janitor's cart along ahead of you.".format(parsed.verb))
                #         self.move(target=v.target.title)
                #         Player.move(target=v.target.title)
                else:
                    raise ActionRefused("You can't {} it that way!".format(parsed.verb))
            return True
        else:
            raise ActionRefused("What do you want to {}?".format(parsed.verb))
        return False


    def move_item(self):
            """
            Select a random accessible exit to move to.
            Avoids exits to a room that have no exits (traps).
            If no suitable exit is found in a few random attempts, return None.
            """
            directions_with_exits = [d for d, e in self.location.exits.items() if e.target.exits]
            for direction in directions_with_exits:
                if direction in parsed.args:
                    xt = self.location.exits[direction]
                    try:
                        xt.allow_passage(self)
                    except ActionRefused:
                        continue
                    else:
                        return xt
            return None

    # def handle_verb(self, parsed, actor):
    #     if parsed.verb in ("move", "push"):
    #         for k, v in self.location.exits.items():
    #             if k in parsed.args:
    #                 # print(k,v)
    #                 actor.tell("You {} the janitor's cart along ahead of you.".format(parsed.verb))
    #                 self.move(target=v.target.title)
    #                 Player.move(target=v.target.title)
    #             else:
    #                 raise ActionRefused("You can't {} it that way!".format(parsed.verb))
    #         return True
    #     else:
    #         raise ActionRefused("What do you want to {}?".format(parsed.verb))
    #     return False


    # def move_item(self):
    #         """
    #         Select a random accessible exit to move to.
    #         Avoids exits to a room that have no exits (traps).
    #         If no suitable exit is found in a few random attempts, return None.
    #         """
    #         directions_with_exits = [d for d, e in self.location.exits.items() if e.target.exits]
    #         for direction in directions_with_exits:
    #             if direction in parsed.args:
    #                 xt = self.location.exits[direction]
    #                 try:
    #                     xt.allow_passage(self)
    #                 except ActionRefused:
    #                     continue
    #                 else:
    #                     return xt
    #         return None

    # def handle_verb(self, parsed, actor):
    #     if parsed.verb == "hack":
    #         if self in parsed.who_info:
    #             actor.tell("It doesn't need to be hacked, you can just type commands on it.")
    #             return True
    #         elif parsed.who_info:
    #             raise ActionRefused("You can't hack that.")
    #         else:
    #             raise ActionRefused("What do you want to hack?")
    #     if parsed.verb in ("type", "enter"):
    #         if parsed.who_info and self not in parsed.who_info:
    #             raise ActionRefused("You need to type it on the computer.")
    #         if parsed.message:
    #             # type "bla bla" on computer (message between quotes)
    #             action, _, door = parsed.message.partition(" ")
    #             self.process_typed_command(action, door, actor)
    #             return True
    #         args = list(parsed.args)
    #         if self.name in args:
    #             args.remove(self.name)
    #         for name in self.aliases:
    #             if name in args:
    #                 args.remove(name)
    #         if args:
    #             args.append("")
    #             self.process_typed_command(args[0], args[1], actor)
    #             return True
    #     return False

    def search_item(self, name, include_inventory=True, include_location=True, include_containers_in_inventory=True):
        """The same as locate_item except it only returns the item, or None."""
        item, container = self.locate_item(name, include_inventory, include_location, include_containers_in_inventory)
        return item  # skip the container

freshman = NPC("freshman", "m", title="freshman", description="It's a freshman. They all look the same.")

class Sawdust(Key):
    def init(self):
        super(Sawdust, self).init()
        self.key_code = 111

sawdust = Sawdust("sawdust", "sawdust")
sawdust.add_extradesc({"sawdust", "pink sawdust"}, "It's pink sawdust, the kind used to soak up spills and messes.")

bucket = Container("bucket", "bucket")
bucket.add_extradesc({"bucket"}, "You see an ordinary blue plastic bucket.")
bucket.init_inventory([sawdust])

trash_can = Container("trash can", "large grey trash can")
trash_can.aliases = {"trash can", "trashcan", "trash"}
trash_can.init_inventory([freshman])

broom = Item("broom", "broom")
broom.add_extradesc({"broom", "pushbroom"}, "You see a large push-broom for sweeping up messes.")

janitors_cart = MovableObject("janitor's cart", "janitor's cart")
janitors_cart.aliases = {"cart", "janitor's cart", "janitor cart", "janitors cart"}
janitors_cart.add_extradesc({"cart", "janitor's cart"}, "The janitor's cart is more or less a trash can on wheels. A bucket of pink sawdust and a broom hang from the cart.")
janitors_cart.init_inventory([trash_can, bucket, broom])
janitors_cart.verbs = {
    # register some custom verbs. You can redefine existing verbs, so be careful.
    "move": "Move the cart to a new location.",
    "push": "Move the cart to a new location.",
}

locker_room.init_inventory([janitors_cart])
