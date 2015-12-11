# coding=utf-8
"""
High School Staff

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""
from __future__ import absolute_import, print_function, division, unicode_literals
import random
from tale import lang, mud_context
from tale.npc import NPC


class Librarian(NPC):
    def init(self):
        # note: this npc uses the deferred feature to yell stuff at certain moments.
        # This is the preferred way (it's efficient).
        mud_context.driver.defer(2, self.do_cry)

    def do_cry(self, ctx):
        self.tell_others("{Title} yells: welcome everyone!")
        self.location.message_nearby_locations("Someone nearby is yelling: welcome everyone!")
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
            self.tell_others("{Title} says: \"Hello there, %s.\"" % actor.title)