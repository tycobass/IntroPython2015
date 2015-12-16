# coding=utf-8
"""
Rooms inside Parsely High

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""

from tale.base import Item, Location, Door, Living
from npcs.teachers import Librarian, MrBushel
from tale.items.basic import Note
from zones.hallways import english_paper


def init(driver):
    # called when zone is first loaded
    pass


class ForDummies(Note):

    def init(self):
        super(Note, self).init()
        self._text = '''
        "Divide by 2" is scrawled in the margin of the book in your handwriting.
        '''

    def read(self, actor):
        actor.tell(self.text)

hallway_door = Door(["hallway", "hallway door", "south", "s", "out"], "hallways.north_hallway", short_description="An open door to the south leads back into the hallway.", 
    locked=False,
    opened=True)

cubby = Item("cubby", "study cubby")
cubby.add_extradesc({"cubby", "study cubby"}, "Your typical wooden study cubby. Generations of students in detention have scratched various messages into the aging wood. ")
cubby.add_extradesc({"scratches", "messages"}, "The cubby's wooden desk has a series of numbers freshly scratched into it: 16-32-64.")

book = ForDummies("book", "dog-eared book")
book.add_extradesc({"book"}, "The book's title is Cryptography for Dummies. You remember skimming it during detention yesterday but that was a long time ago.")
book.aliases = {"library book", "cryptography book", "cryptography for dummies", "dog-eared book"}

librarian = Librarian("School Librarian", "f", race="human", title="Ms. Smith, the School Librarian", description="Ms. Smith, the school librarian.")
librarian.aliases = {"librarian", "school librarian", "mrs. smith"}
librarian.add_extradesc({"librarian", "school librarian"}, "Female, elderly, hair in a bun. Could she be more stereotypical?")

mr_bushel = MrBushel("Mr. Bushel", "m", race="human", title="Mr. Bushel", description="Mr. Bushel, your English teacher")
mr_bushel.aliases = {"mr bushel", "bushel", "teacher", "english teacher"}
mr_bushel.add_extradesc({"Mr. Bushel"}, "Mr. Bushel is your English teacher and the Parsely High football coach. His face is growing redder with irritation as he waits for you to hand in your paper.")


class Library(Location):
    """
    Parsely High's Library
    """
    def __init__(self, name, description=None, visits=0):
        super(Location, self).__init__(name, description=description)
        self.name = name      # make sure we preserve the case; base object stores it lowercase
        self.livings = set()  # set of livings in this location
        self.items = set()    # set of all items in the room
        self.exits = {}       # dictionary of all exits: exit_direction -> Exit object with target & descr
        self.visits = visits
        self.init_inventory([cubby, book, librarian])
        self.add_exits([hallway_door])

    def __contains__(self, obj):
        return obj in self.livings or obj in self.items

    def insert(self, obj, actor):
        """Add obj to the contents of the location (either a Living or an Item)"""
        if isinstance(obj, Living):
            self.livings.add(obj)
        elif isinstance(obj, Item):
            self.items.add(obj)
        else:
            raise TypeError("can only add Living or Item")
        obj.location = self

    def notify_action(self, parsed, actor):
        """Notify the room, its livings and items of an action performed by someone."""
        # Notice that this notification event is invoked by the driver after all
        # actions concerning player input have been handled, so we don't have to
        # queue the delegated calls.
        for living in self.livings:
            living._notify_action_base(parsed, actor)
        for item in self.items:
            item.notify_action(parsed, actor)
        for exit in set(self.exits.values()):
            exit.notify_action(parsed, actor)

    def notify_player_arrived(self, player, previous_location):
        """a player has arrived in this location."""
        if self.visits == 0:
            player.tell('Ms. Smith peers myopically at you and says, "You should be in class, young man!"')
            self.visits += 1
        else:
            player.tell("Ms. Smith peers at you suspiciously.")


class EnglishRoom(Location):
    """
    Your English classroom.
    """
    def __init__(self, name, description=None):
        super(Location, self).__init__(name, description=description)
        self.name = name      # make sure we preserve the case; base object stores it lowercase
        self.livings = set()  # set of livings in this location
        self.items = set()    # set of all items in the room
        self.exits = {}       # dictionary of all exits: exit_direction -> Exit object with target & descr
        self.init_inventory([mr_bushel])

    def __contains__(self, obj):
        return obj in self.livings or obj in self.items

    def insert(self, obj, actor):
        """Add obj to the contents of the location (either a Living or an Item)"""
        if isinstance(obj, Living):
            self.livings.add(obj)
        elif isinstance(obj, Item):
            self.items.add(obj)
        else:
            raise TypeError("can only add Living or Item")
        obj.location = self

    def notify_action(self, parsed, actor):
        """Notify the room, its livings and items of an action performed by someone."""
        # Notice that this notification event is invoked by the driver after all
        # actions concerning player input have been handled, so we don't have to
        # queue the delegated calls.
        for living in self.livings:
            living._notify_action_base(parsed, actor)
        for item in self.items:
            item.notify_action(parsed, actor)
        for exit in set(self.exits.values()):
            exit.notify_action(parsed, actor)

    def notify_player_arrived(self, player, previous_location):
        """a player has arrived in this location."""
        player.tell('''
        As you step into the classroom your teacher, Mr. Bushel, clears his throat. "You're late, as usual. I sincerely hope you remembered your homework." He holds out his hand expectantly.
        ''')
        if english_paper in player.inventory:
            pass
        else:
            player.tell_later("After a few minutes of prevaricating, you're forced to admit that you don't have your homework. Mr. Bushel growls and sends you off to the library, where you spend the next four hours staring at the wall. The End.")
            player.story_completed()

english = EnglishRoom("English Class", "You're in your English classroom, where you've spent many long, boring hours trying not to fall asleep.")

library = Library("Library", "You're in the library, where you usually spend your after-school time in detention.")
