# -*- coding: utf-8 -*-
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

date: Mon Jan 19 12:32:47 2015
@author: daniel
"""


class GameState:

    def __init__(self):
        self.start_time = 0
        self.is_won = False
        self.is_game_over = False
        self.click_count = 0
        self.quit = False
        self.is_started = False
        self.is_restart = False

    def __str__(self):
        return """
        Start time   : {0}
        Is won?      : {1}
        Is game over?: {2}
        Click count  : {3}
        Time to quit?: {4}
        Started?     : {5}""".format(self.start_time, self.is_won,
                                     self.is_game_over, self.click_count,
                                     self.quit, self.is_started)

    def start(self, time):
        self.start_time = time
        self.is_started = True

    def get_current_time(self, time):
        return (time - self.start_time) // 1000

    def left_click(self):
        self.click_count += 1

    def right_click(self, time):
        pass

    def game_over(self):
        self.is_game_over = True

    def win(self):
        self.is_won = True

    def restart(self, time):
        self.start_time = time
        self.is_game_over = False
        self.is_won = False
        self.is_started = False
        self.click_count = 0
        self.is_restart = True
