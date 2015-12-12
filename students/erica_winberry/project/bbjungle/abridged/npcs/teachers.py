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
from story import Story
from zones.hallways import english_paper


class MrBushel(NPC):
    def init(self):
        mud_context.driver.defer(2, self.do_idle_action)
        self.aggressive = True

    def insert(self, item, actor):
        """NPC have a bit nicer refuse message when giving items to them."""
        if item is english_paper:
            super(NPC, self).insert(item, self)
            actor.story_completed()
            actor.tell_later("""
Mr. Bushel takes your English paper with a look of surprise. "Well, better late than never, I suppose."
You take your seat. For the first time in weeks, you won't be in detention all afternoon.""")
        else:
            raise ActionRefused("{} doesn't want {}.".format(lang.capital(self.title), item.title))

    def do_idle_action(self, ctx):
        if random.random() < 0.5:
            self.tell_others("{} clears his throat impatiently.".format(self.title))
        else:
            self.tell_others("{} snorts in irritation.".format(self.title))
        ctx.driver.defer(random.randint(20, 50), self.do_idle_action)

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
            self.tell_others("{} says: \"Mr. Tannen, stop stalling and turn in your homework, please.\"".format(self.title))


class Librarian(NPC):
    def init(self):
        mud_context.driver.defer(2, self.do_cry)
        self.aggressive = True

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