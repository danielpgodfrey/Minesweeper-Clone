# -*- coding: utf-8 -*-
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

date: Mon Jan 19 14:10:32 2015
@author: daniel
"""

import pygame


class EventHandler:
    def handle_event(self, event, grid, game_state, controls):
        time = pygame.time.get_ticks()

        if event.type == pygame.QUIT:
            game_state.quit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = controls.get_mouse_pos(event)

            # Left click event
            if event.button == 1 and not controls.check_double_click(time):
                if not game_state.is_game_over and not game_state.is_won:
                    print('LC')
                    self._left_click(grid, game_state, time, mouse_pos)
                else:
                    game_state.restart(time)

            # Right click event
            elif event.button == 3 and not controls.check_double_click(time):
                if not game_state.is_game_over and not game_state.is_won:
                    self._right_click(grid, game_state, time, mouse_pos)
                else:
                    game_state.quit = True

    def _left_click(self, grid, game_state, time, mouse_pos):

        if game_state.click_count == 0:
            grid.initialize_grid(mouse_pos)
            game_state.start(pygame.time.get_ticks())

        game_state.left_click()
        grid.click_grid(mouse_pos, "left")

    def _right_click(self, grid, game_state, time, mouse_pos):
        game_state.right_click(time)
        grid.click_grid(mouse_pos, "right")
