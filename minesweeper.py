# -*- coding: utf-8 -*-
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

date: Mon Jan 19 14:10:32 2015
@author: daniel
"""
import pygame

# from constants import *
from grid import Grid
from screen import Screen
from controls import Controls
from gamestate import GameState
from eventhandler import EventHandler


class Game:
    """
    This class holds all the game elements. It renders the game,
    controls user input, and handles game logic.
    """

    def __init__(self):
        """
        Sets up the initial game state, and starts the game
        """
        self.initialize_pygame()

    def initialize_pygame(self):
        """
        Initializes pygame-related things.
        """
        pygame.init()
        self.clock = pygame.time.Clock()

    def restart(self, click_grid, flag_grid):
        """
        Handles what should occur on game restart. The screen should return
        to the initial state, and the click_grid should be reinitialized.
        """
        pass

    def play(self):
        """
        This is the main loop of the program. It draws to the screen
        at appropriate times and controls the events of the game.
        """

        grid = Grid()
        event_handler = EventHandler()
        game_state = GameState()
        controls = Controls()
        screen = Screen(grid)

        # This grid changes during gameplay, so I initialize it in
        # the main game loop.
        while not game_state.quit:
            for event in pygame.event.get():
                event_handler.handle_event(event, grid, game_state, controls)

            if grid.mine_clicked:
                game_state.game_over()
            elif grid.revealed_blocks == grid.non_mine_count:
                game_state.win()

            if game_state.is_game_over:
                screen.game_over(grid)
            elif game_state.is_won:
                screen.victory_screen(grid)
                print("win")
            elif game_state.click_count >= 1:
                current_time = game_state.get_current_time(
                    pygame.time.get_ticks())

                screen._display_time_counter(current_time)

            if game_state.is_restart:
                screen.initial_draw(grid)

            # Update screen.
            screen.draw_grid(grid)
            pygame.display.flip()

            self.clock.tick(60)


def main():
    game = Game()
    game.play()
    pygame.quit()

if __name__ == "__main__":
    main()
