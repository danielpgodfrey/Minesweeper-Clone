# -*- coding: utf-8 -*-
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

date: Mon Jan 19 12:25:29 2015
@author: daniel
"""

# import pygame


class Controls:
    def __init__(self):
        self.double_click = False
        self.click_time = 0

    def get_mouse_pos(self, event):
        return event.pos

    def check_double_click(self, click_time):
        if click_time > self.click_time + 100:
            self.click_time = click_time
            return False
        else:
            return True
