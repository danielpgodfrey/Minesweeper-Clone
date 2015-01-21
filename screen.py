# -*- coding: utf-8 -*-
"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

date: Mon Jan 19 14:52:04 2015
@author: daniel
"""

import pygame
from block import Block
from constants import *


class Screen:
    FLAG_LOCATION = "img/flag.png"
    MINE_LOCATION = "img/mine.png"
    RED_X_LOCATION = "img/red_x.png"

    BLOCK_COLOR = GRAY
    CLICKED_BLOCK_COLOR = DARKGRAY
    BACKGROUND_COLOR = BLACK
    MINE_COLOR = RED
    # Bottom portion of screen to display counters, time, etc.
    INFO_HEIGHT = 75

    def __init__(self, grid):
        # Screen elements
        self.screen_size = self._get_screen_size(grid)
        self.screen = pygame.display.set_mode(self.screen_size)
        #TODO: Grid class's/block classes initialization change
        self.block_font_size = int(0.7 * Block.WIDTH)
        self.display_font_size = int(grid.row_count * 1.2 - grid.col_count*.2)
        pygame.display.set_caption("Minesweeper Alpha")

        self.word_font = pygame.font.SysFont('Arial',
                                             self.display_font_size,
                                             True, False)

        self.block_font = pygame.font.SysFont('Courier',
                                              self.block_font_size,
                                              True, False)

        self.flag_image = pygame.image.load(self.FLAG_LOCATION)
        self.mine_image = pygame.image.load(self.MINE_LOCATION)
        self.red_x_image = pygame.image.load(self.RED_X_LOCATION)
        self.initial_draw(grid)

    def initial_draw(self, grid):
        self.screen.fill(self.BACKGROUND_COLOR)
        for row in range(grid.row_count):
            for col in range(grid.col_count):
                self._draw_empty_block(row, col, self.BLOCK_COLOR)

        self._display_flag_counter(0)
        self._display_mine_counter(grid.mine_count)
        self._display_time_counter(0)

    def draw_grid(self, grid):
        for row in grid.blocks:
            for block in row:
                self._draw_block(block)

    def game_over(self, grid):
        self._draw_empty_block(grid.last_clicked_block.row,
                               grid.last_clicked_block.col, self.MINE_COLOR)

        grid.reveal_mines_and_flags()
        self.draw_grid(grid)

        self._display_text("You lose!", 10)
        self._display_text("Left click to restart.", 30)
        self._display_text("Right click to quit.", 50)

    def victory_screen(self, grid):
        grid.reveal_mines_and_flags()
        self.draw_grid(grid)

        self._display_text("You win!", 10)
        self._display_text("Left click to restart.", 30)
        self._display_text("Right click to quit.", 50)

    def _get_screen_size(self, grid):
        screen_height = grid.row_count * (Block.HEIGHT + Block.MARGIN) + \
            Block.MARGIN + self.INFO_HEIGHT
        screen_width = grid.col_count * (Block.WIDTH + Block.MARGIN) + \
            Block.MARGIN

        return (screen_width, screen_height)

    def _draw_empty_block(self, row, col, color):
        # TODO: Fix this. Since the blocks aren't generated until after
        # the user clicks, we have to do it like this for now. Perhaps
        # we can find a different way to initialize blocks.
        pygame.draw.rect(self.screen, color,
                         (col * Block.WIDTH + (col + 1) *
                          Block.MARGIN,
                          row * Block.HEIGHT + (row + 1) *
                          Block.MARGIN, Block.WIDTH, Block.HEIGHT))

    def _draw_block(self, block):
        if block.is_revealed:
            if not block.is_mine and not block.flagged:
                self._draw_empty_block(block.row, block.col,
                                       self.CLICKED_BLOCK_COLOR)

                if block.mine_neighbor_count > 0:
                    self._draw_block_number(block)

            elif block.is_mine and not block.flagged:
                self._draw_mine(block)

            elif block.flagged and not block.is_mine:
                self._draw_mine(block)
                self._draw_image(self.red_x_image, block)

        else:
            if block.flagged:
                self._draw_image(self.flag_image, block)

            elif not block.flagged:
                self._draw_empty_block(block.row, block.col, self.BLOCK_COLOR)

    def _draw_block_number(self, block):
        text = self.block_font.render(str(block.mine_neighbor_count),
                                      True, block.color)

        self.screen.blit(text, [block.x + 7, block.y + 3])

    def _draw_mine(self, block):
        self._draw_image(self.mine_image, block)

    def _draw_image(self, image, block):
        self.screen.blit(image, (block.x, block.y, block.WIDTH, block.HEIGHT))

    def _display_text(self, string, y_offset):
        y0 = self.screen_size[1] - self.INFO_HEIGHT + y_offset
        text = self.word_font.render(string, True, WHITE)
        text_loc = self._get_centered_text(string, y0)

        pygame.draw.rect(self.screen, BLACK, text_loc)
        self.screen.blit(text, text_loc)

    def _get_centered_text(self, string, y):
        text = self.word_font.render(string, True, WHITE)
        textpos = text.get_rect()
        textpos.centerx = self.screen_size[0] // 2
        textpos.centery = y
        return textpos

    def _display_time_counter(self, time):
        y_offset = 40
        self._display_counter("TIME:  ", time, y_offset)

    def _display_mine_counter(self, mine_count):
        y_offset = 20
        self._display_counter("MINES: ", mine_count, y_offset)

    def _display_flag_counter(self, flag_count):
        y_offset = 0
        self._display_counter("FLAGS: ", flag_count, y_offset)

    def _display_counter(self, prestring, count, y_offset):
        x0 = 0
        y0 = self.screen_size[1] - self.INFO_HEIGHT + y_offset
        string = prestring + str(count)

        text = self.word_font.render(string, True, WHITE)
        text_size = self.word_font.size(string)

        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (x0, y0, text_size[0], text_size[1]))
        self.screen.blit(text, [x0, y0, text_size[0], text_size[1]])
