# coding=utf-8
"""
The central town, which is the place where mud players start/log in

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

from __future__ import absolute_import, print_function, division, unicode_literals
from tale.base import Location, Exit, Item, Container
from tale.npc import NPC
from tale.player import Player
from tale.errors import ActionRefused
from tale.items.basic import Boxlike

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

glasses = Item("glasses", "glasses", "pair of ladies eyeglasses.")
glasses.aliases = {"glasses"}
glasses.add_extradesc({"glasses"}, "The horn-rimmed glasses aren't really your style.")

glasses_case = GlassesCase("case", "clamshell case for eyeglasses")
glasses_case.aliases = {"case", "clamshell case", "eyeglasses case"}
glasses_case.init_inventory([glasses])

gym.init_inventory([glasses_case])

class MovableObject(Container):
    pass

janitors_cart = UntakableContainer("janitor's cart", "janitor's cart")
janitors_cart.aliases = {"cart", "janitor's cart", "janitor cart", "janitors cart"}
janitors_cart.add_extradesc({"cart", "janitor's cart"}, "The janitor's cart is more or less a trash can on wheels. A bucket of pink sawdust and a broom hang from the cart.")

bucket = Container("bucket", "bucket")
bucket.add_extradesc({"bucket"}, "You see an ordinary blue plastic bucket.")

sawdust = Item("sawdust", "pink sawdust")
sawdust.add_extradesc({"sawdust", "pink sawdust"}, "It's pink sawdust, the kind used to soak up spills and messes.")

trash_can = Container("trash can", "large grey trash can")
trash_can.aliases = {"trash can", "trashcan", "trash"}

freshman = NPC("freshman", "m", title="freshman", description="It's a freshman. They all look the same.")

broom = Item("broom", "broom")
broom.add_extradesc({"broom", "pushbroom"}, "You see a large push-broom for sweeping up messes.")

locker_room.init_inventory([janitors_cart])

janitors_cart.init_inventory([trash_can, bucket, broom])

trash_can.init_inventory([freshman])

bucket.init_inventory([sawdust])
