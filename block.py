# -*- coding: utf-8 -*-
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

date: Mon Jan 19 14:10:32 2015
@author: daniel
"""

from constants import *


class Block:
    TEXT_COLORS = {'MINE': RED,
                   0: DARKGRAY,
                   1: LITEBLUE,
                   2: GREEN,
                   3: RED,
                   4: DARKBLUE,
                   5: BROWN,
                   6: CYAN,
                   7: GRAY,
                   8: ORANGE}

    # Size of the blocks, and the margin between them.
    WIDTH = 20
    HEIGHT = 20
    MARGIN = 5

    def __init__(self, row, col):
        self.flagged = False
        self.color = WHITE
        self.is_revealed = False
        self.row = row
        self.col = col

        # Position on the screen
        self.x = self.col * self.WIDTH + (self.col + 1) * self.MARGIN
        self.y = self.row * self.HEIGHT + (self.row + 1) * self.MARGIN

    def update_with_mines(self, is_mine, mine_neighbors):
        self.is_mine = is_mine
        self.mine_neighbor_count = mine_neighbors

    def cycle_flag(self):
        self.flagged = not self.flagged

    def reveal(self):
        self.is_revealed = True

        if self.is_mine:
            self.color = self.TEXT_COLORS["MINE"]
        else:
            self.color = self.TEXT_COLORS[self.mine_neighbor_count]
