import pygame

from constants import *

class Screen:

    """
    This class is responsible for drawing to the screen.
    """

    def __init__(self):
        # Screen elements
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper Alpha")
        
        self.word_font = pygame.font.SysFont('Arial', 16, True, False)
        self.number_font = pygame.font.SysFont('Courier', 14, True, False)
        
        self.flag_image = pygame.image.load(FLAG_LOCATION)
        self.mine_image = pygame.image.load(MINE_LOCATION)
        self.red_x_image = pygame.image.load(RED_X_LOCATION)
        self.initial_draw()

    def initial_draw(self):
        """
        Draw initial game board. All blocks should initially be
        white
        """
        self.screen.fill(BLACK)
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                self._draw_block(GRAY, row, column)
                
        self._display_flag_counter(0)
        self._display_mine_counter(MINES)
        self._display_time_counter(0)

    def update_grid(self, click_grid, color_grid, mine_neighbor_grid):
        for row in range(0, ROWS):
            for column in range(0, COLUMNS):
                # Only draw to the screen if the block is marked
                # as to-draw
                if click_grid.get_value(row, column):
                    self._draw_block(DARKGRAY, row, column)
                            
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
            self._draw_image(self.flag_image, row, column)
                             
        elif not flag_grid.get_value(row, column):
            self._draw_block(GRAY, row, column)
            
        self._display_flag_counter(flag_grid.flag_count)

    def victory_screen(self, mine_grid):
        """
        This controls what happens when the user clicks on a mine.
        """
        for row in range(ROWS):
            for column in range(COLUMNS):
                if mine_grid.get_value(row, column):
                    self._draw_image(self.flag_image, row, column)

        self._display_text("You win!", 20)
        self._display_text("Left click to restart.", 40)
        self._display_text("Right click to quit.", 60)        
        
    def game_over_screen(self, mine_grid, click_grid, flag_grid):
        """
        This controls what happens when the user clicks on a mine.
        """
        for row in range(ROWS):
            for column in range(COLUMNS):
                if mine_grid.get_value(row, column) and click_grid.get_value(row, column):
                    self._draw_block(RED, row, column)
                    self._draw_image(self.mine_image, row, column)
                    
                elif mine_grid.get_value(row, column) and not flag_grid.get_value(row, column):
                    self._draw_block(DARKGRAY, row, column)
                    self._draw_image(self.mine_image, row, column)
                    
                elif not mine_grid.get_value(row, column) and flag_grid.get_value(row, column):
                    self._draw_block(DARKGRAY, row, column)
                    self._draw_image(self.mine_image, row, column)
                    self._draw_image(self.red_x_image, row, column)
                             
        self._display_text("You lose!", 10)
        self._display_text("Left click to restart.", 30)
        self._display_text("Right click to quit.", 50)
        
    def _display_flag_counter(self, flag_count):
        y_offset = 0
        self._display_counter("FLAGS: ", flag_count, y_offset)
    
    def _display_mine_counter(self, mine_count):
        y_offset = 20
        self._display_counter("MINES: ", mine_count, y_offset)
    
    def _display_time_counter(self, time):
        y_offset = 40
        self._display_counter("TIME:  ", time, y_offset)
    
    def _display_counter(self, prestring, count, y_offset):
        x0 = 0
        y0 = SCREEN_HEIGHT - INFO_HEIGHT + y_offset
        string = prestring + str(count)
        
        text = self.word_font.render(string, True, WHITE)
        text_size = self.word_font.size(string)
        
        pygame.draw.rect(self.screen, BLACK, (x0, y0, text_size[0], text_size[1]))
        self.screen.blit(text, [x0, y0, text_size[0], text_size[1]])

    def _display_text(self, string, y_offset):
        y0 = SCREEN_HEIGHT - INFO_HEIGHT + y_offset
        text = self.word_font.render(string, True, WHITE)
        text_size = self.word_font.size(string)
        text_loc = self._get_centered_text(string, y0)
        
        pygame.draw.rect(self.screen, BLACK, text_loc)
        self.screen.blit(text, text_loc)
    
    def _draw_image(self, image, row, column):
        self.screen.blit(image,
            (column * GRID_WIDTH + (column + 1) * MARGIN,
             row * GRID_HEIGHT + (row + 1) * MARGIN,
             GRID_WIDTH,
             GRID_HEIGHT))
             
    def _draw_block(self, color, row, column):
         pygame.draw.rect(self.screen, color,
            (column * GRID_WIDTH + (column + 1) * MARGIN,
             row * GRID_HEIGHT + (row + 1) * MARGIN,
             GRID_WIDTH,
             GRID_HEIGHT))
             
    def _get_centered_text(self, string, y):
        text = self.word_font.render(string, True, WHITE)
        textpos = text.get_rect()
        textpos.centerx = SCREEN_WIDTH // 2
        textpos.centery = y
        return textpos
