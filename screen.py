import pygame

from constants import *

class Screen:

    """
    This class is responsible for drawing to the screen.
    """

    def __init__(self):
        # Screen elements
        self.screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
        pygame.display.set_caption("Minesweeper Alpha")
        self.word_font = pygame.font.SysFont('Arial', 16, True, False)
        self.number_font = pygame.font.SysFont('Courier', 14, True, False)
        self.flag_image = pygame.image.load(FLAG_LOCATION)
        self.initial_draw()

    def initial_draw(self):
        """
        Draw initial game board. All blocks should initially be
        white
        """
        self.screen.fill(BLACK)
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                pygame.draw.rect(self.screen, GRAY,
                                (column * GRID_WIDTH + (column + 1) * MARGIN,
                                 row * GRID_HEIGHT + (row + 1) * MARGIN,
                                 GRID_WIDTH,
                                 GRID_HEIGHT))

    def update_grid(self, click_grid, color_grid, mine_neighbor_grid):
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                # Only draw to the screen if the block is marked
                # as to-draw
                if click_grid.get_value(row, column):
                    pygame.draw.rect(self.screen, 
                        # color_grid.get_value(row, column),
                        DARKGRAY,
                        (column * GRID_WIDTH + (column + 1) * MARGIN,
                         row * GRID_HEIGHT + (row + 1) * MARGIN,
                         GRID_WIDTH,
                         GRID_HEIGHT))
                            
                    # Draw the mine-neighbor number if it is greater than 0
                    if mine_neighbor_grid.get_value(row, column) > 0:
                        text = self.number_font.render(
                                str(mine_neighbor_grid.get_value(row, column)), 
                                True, color_grid.get_value(row, column))
                            
                        self.screen.blit(text, 
                            [column * GRID_WIDTH + (column + 1) * MARGIN + 7,
                            row * GRID_HEIGHT + (row + 1) * MARGIN + 3])
                                     
    def draw_flags(self, row, column, click_grid, flag_grid):
        if click_grid.get_value(row, column):
            return
            
        elif flag_grid.get_value(row, column):
            self.screen.blit(self.flag_image,
                            (column * GRID_WIDTH + (column + 1) * MARGIN,
                             row * GRID_HEIGHT + (row + 1) * MARGIN,
                             GRID_WIDTH,
                             GRID_HEIGHT))
                             
        elif not flag_grid.get_value(row, column):
            pygame.draw.rect(self.screen, GRAY,
                (column * GRID_WIDTH + (column + 1) * MARGIN,
                 row * GRID_HEIGHT + (row + 1) * MARGIN,
                 GRID_WIDTH,
                 GRID_HEIGHT))

    def victory_screen(self):
        """
        This controls what happens when the user clicks on a mine.
        """
        self.screen.fill(BLACK)

        text = self.word_font.render("You won!", True, PURPLE)
        self.screen.blit(text, self._get_centered_text(text, 20))

        text = self.word_font.render("Left click to restart.", True, WHITE)
        self.screen.blit(text, self._get_centered_text(text, 100))
                
        text = self.word_font.render("Right click to quit.", True, WHITE)
        self.screen.blit(text, self._get_centered_text(text, 150))
        
    def game_over_screen(self):
        """
        This controls what happens when the user clicks on a mine.
        """
        self.screen.fill(BLACK)

        text = self.word_font.render("You lost!", True, PURPLE)
        self.screen.blit(text, self._get_centered_text(text, 20))

        text = self.word_font.render("Left click to restart.", True, WHITE)
        self.screen.blit(text, self._get_centered_text(text, 100))
                
        text = self.word_font.render("Right click to quit.", True, WHITE)
        self.screen.blit(text, self._get_centered_text(text, 150))
        
    def _get_centered_text(self, text, y):
        textpos = text.get_rect()
        textpos.centerx = SCREEN_WIDTH // 2
        textpos.centery = y
        return textpos
