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
        self.word_font = pygame.font.SysFont('Arial', 24, True, False)
        self.number_font = pygame.font.SysFont('Arial', 14, True, False)
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
                pygame.draw.rect(self.screen, WHITE,
                                (column * GRID_WIDTH + (column + 1) * MARGIN,
                                 row * GRID_HEIGHT + (row + 1) * MARGIN,
                                 GRID_WIDTH,
                                 GRID_HEIGHT))

    def update_grid(self, click_grid, color_grid, mine_neighbor_grid):
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
                    if mine_neighbor_grid[row][column] != 0:
                        text = self.number_font.render(
                                str(mine_neighbor_grid[row][column]), 
                                True, WHITE)
                            
                        self.screen.blit(text, 
                            [column * GRID_WIDTH + (column + 1) * MARGIN + 7,
                            row * GRID_HEIGHT + (row + 1) * MARGIN + 2])
                                     
    def draw_flags(self, row, column, click_grid, flag_grid):
        if click_grid[row][column] == 1:
            pass
        elif flag_grid[row][column] == 1:
            self.screen.blit(self.flag_image,
                            (column * GRID_WIDTH + (column + 1) * MARGIN,
                             row * GRID_HEIGHT + (row + 1) * MARGIN,
                             GRID_WIDTH,
                             GRID_HEIGHT))
        elif flag_grid[row][column] == 0:
            pygame.draw.rect(self.screen, WHITE,
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
        self.screen.blit(text, [SCREEN_WIDTH // 7, 5])

        text = self.word_font.render("Left click to restart.", True, WHITE)
        self.screen.blit(text, [20, 100])
        
        text = self.word_font.render("Right click to quit.", True, WHITE)
        self.screen.blit(text, [20, 150])
        
    def game_over_screen(self):
        """
        This controls what happens when the user clicks on a mine.
        """
        self.screen.fill(BLACK)

        text = self.word_font.render("You lost!", True, PURPLE)
        self.screen.blit(text, [SCREEN_WIDTH // 7, 5])

        text = self.word_font.render("Left click to restart.", True, WHITE)
        self.screen.blit(text, [0, 100])
        
        text = self.word_font.render("Right click to quit.", True, WHITE)
        self.screen.blit(text, [0, 150])

