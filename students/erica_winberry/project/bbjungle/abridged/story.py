# coding=utf-8
"""
Blackboard Jungle

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""
from __future__ import absolute_import, print_function, division, unicode_literals
import datetime
import sys
from tale.hints import Hint
from tale.story import Storybase
from tale.main import run_story


class Story(Storybase):
    name = "Blackboard Jungle"
    author = "Jared A. Sorenson (python version by Erica Winberry)"
    author_address = "elaewin@gmail.com"
    version = "1.2"
    requires_tale = "2.6"
    supported_modes = {"if"}
    player_name = "Biff"
    player_gender = "m"
    player_race = "human"
    server_tick_method = "timer"
    server_tick_time = 1.0
    gametime_to_realtime = 5
    display_gametime = True
    epoch = datetime.datetime(2015, 12, 10, 14, 0, 0)
    startlocation_player = "athletics.gym"
    startlocation_wizard = "athletics.gym"
    license_file = "messages/license.txt"

    driver = None     # will be set by init()

    def init(self, driver):
        """Called by the game driver when it is done with its initial initialization"""
        self.driver = driver
        self.driver.load_zones(["athletics", "classrooms", "hallways"])

    def init_player(self, player):
        """
        Called by the game driver when it has created the player object.
        You can set the hint texts on the player object, or change the state object, etc.
        """
        player.hints.init([
            Hint(None, None, "Find a way to end the day without ending up in detention. (Again.)"),
        ])

    def welcome(self, player):
        """welcome text when player enters a new game"""
        player.tell("<bright>Hello, <player>{}</><bright>! Welcome to {}.</>".format(player.title.capitalize(), self.name), end=True)
        player.tell("\n")
        player.tell(self.driver.resources["messages/welcome.txt"].data)
        player.tell("\n")

    def welcome_savegame(self, player):
        """welcome text when player enters the game after loading a saved game"""
        player.tell("<bright>Hello, <player>{}</><bright>, welcome back to {}.</>".format(player.title, self.name), end=True)
        player.tell("\n")
        player.tell(self.driver.resources["messages/welcome.txt"].data)
        player.tell("\n")

    def goodbye(self, player):
        """goodbye text when player quits the game"""
        player.tell("Goodbye, {}. Please come back again soon.".format(player.title))
        player.tell("\n")

    def completion_success(self, player):
        """congratulation text / finale when player finished the game (story_complete event)"""
        self.display_text_file(player, "messages/completion_success.txt")

    def completion_failed1(self, player):
        """text / finale when player slipped in the south Hallway (story_complete event)"""
        self.display_text_file(player, "messages/completion_failed1.txt")

    def completion_failed2(self, player):
        """text / finale when player couldn't turn in the English paper (story_complete event)"""
        self.display_text_file(player, "messages/completion_failed2.txt")

if __name__ == "__main__":
    # story is invoked as a script, start it in the Tale Driver.
    run_story(sys.path[0])
