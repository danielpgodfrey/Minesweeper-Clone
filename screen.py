import pygame

from constants import *

class Screen:

    """
    This class is responsible for drawing to the screen.
    """

    def __init__(self):
        # Screen elements
        self.screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
        pygame.display.set_caption("Minesweeper Pre-Alpha")
        self.font = pygame.font.SysFont('Ubuntu', 24, True, False)
        self.initial_draw()

    def initial_draw(self):
        """
        Draw initial game board. All blocks should initially be
        white
        """
        self.screen.fill(BLACK)
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                pygame.draw.rect(self.screen, WHITE,
                                (column * GRID_WIDTH + (column + 1) * MARGIN,
                                 row * GRID_HEIGHT + (row + 1) * MARGIN,
                                 GRID_WIDTH,
                                 GRID_HEIGHT))

    def update_grid(self, click_grid, color_grid):
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                # Only draw to the screen if the block is marked
                # as to-draw
                if click_grid[row][column] == 1:
                    pygame.draw.rect(self.screen, color_grid[row][column],
                                    (column * GRID_WIDTH + (column + 1) * MARGIN,
                                     row * GRID_HEIGHT + (row + 1) * MARGIN,
                                     GRID_WIDTH,
                                     GRID_HEIGHT))

    def victory_screen(self):
        """
        This controls what happens when the user clicks on a mine.
        """
        self.screen.fill(BLACK)

        font = pygame.font.SysFont('Ubuntu', 24, True, False)
        text = self.font.render("Congraturaisins!", True, PURPLE)
        self.screen.blit(text, [SCREEN_WIDTH // 7, 5])

        text = self.font.render("You win!", True, WHITE)
        self.screen.blit(text, [SCREEN_WIDTH // 3, 100])

    def game_over_screen(self):
        """
        This controls what happens when the user clicks on a mine.
        """
        self.screen.fill(BLACK)

        text = self.font.render("Congraturaisins!", True, PURPLE)
        self.screen.blit(text, [SCREEN_WIDTH // 7, 5])

        text = self.font.render("You lose!", True, WHITE)
        self.screen.blit(text, [SCREEN_WIDTH // 3, 100])

