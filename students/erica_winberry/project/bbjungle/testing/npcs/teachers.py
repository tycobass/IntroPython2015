# coding=utf-8
"""
Creatures living in the central town.

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""
from __future__ import absolute_import, print_function, division, unicode_literals
import random
from tale import lang, mud_context
from tale.npc import NPC
from tale.errors import ActionRefused


class MrBushel(NPC):
    def init(self):
        mud_context.driver.defer(2, self.do_idle_action)
        self.aggressive = True

    def insert(self, item, actor):
        """NPC have a bit nicer refuse message when giving items to them."""
        if not self.aggressive or actor is self or actor is not None and "wizard" in actor.privileges:
            super(NPC, self).insert(item, self)
        else:
            if self.aggressive and item is not "english paper":
                raise ActionRefused("%s doesn't want %s." % (lang.capital(self.title), item.title))
            else:
                self.aggressive = False

    def do_idle_action(self, ctx):
        if random.random() < 0.5:
            self.tell_others("{Title} clears his throat impatiently." % self.possessive)
        else:
            self.tell_others("{Title} sniffs around and moves %s whiskers." % self.possessive)
        ctx.driver.defer(random.randint(5, 15), self.do_idle_action)

    def notify_action(self, parsed, actor):
        greet = False
        if parsed.verb in ("hi", "hello"):
            greet = True
        elif parsed.verb == "say":
            if "hello" in parsed.args or "hi" in parsed.args:
                greet = True
        elif parsed.verb == "greet" and self in parsed.who_info:
            greet = True
        if greet:
            self.tell_others("{Title} says: \"Hello there, %s.\"" % actor.title)


class WalkingRat(NPC):
    def init(self):
        super(WalkingRat, self).init()
        mud_context.driver.defer(2, self.do_idle_action)
        mud_context.driver.defer(4, self.do_random_move)
        self.aggressive = True

    def do_idle_action(self, ctx):
        if random.random() < 0.5:
            self.tell_others("{Title} wiggles %s tail." % self.possessive)
        else:
            self.tell_others("{Title} sniffs around and moves %s whiskers." % self.possessive)
        ctx.driver.defer(random.randint(5, 15), self.do_idle_action)

    def do_random_move(self, ctx):
        direction = self.select_random_move()
        if direction:
            self.move(direction.target, self)
        ctx.driver.defer(random.randint(10, 20), self.do_random_move)


class Librarian(NPC):
    def init(self):
        mud_context.driver.defer(2, self.do_cry)

    def do_cry(self, ctx):
        self.tell_others("{Title} mutters to herself as she putters around behind the library counter.")
        ctx.driver.defer(random.randint(20, 40), self.do_cry)

    def notify_action(self, parsed, actor):
        greet = False
        if parsed.verb in ("hi", "hello"):
            greet = True
        elif parsed.verb == "say":
            if "hello" in parsed.args or "hi" in parsed.args:
                greet = True
        elif parsed.verb == "greet" and self in parsed.who_info:
            greet = True
        if greet:
            self.tell_others("{Title} glares at you, and says, \"Shhhh!\"")