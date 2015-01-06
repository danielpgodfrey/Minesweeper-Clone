import pygame
import random

from constants import *
import grid
from screen import Screen

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
        self.clock = pygame.time.Clock()
        self.game_screen = Screen()

    def initialize_pygame(self):
        """
        Initializes pygame-related things.
        """
        pygame.init()

    def get_mouse_pos(self):
        """
        Update the click_grid list when the user clicks a grid.
        """
        pos = pygame.mouse.get_pos()
        return pos

    def find_row_and_column_clicked(self, mouse_pos):
        """
        Returns row and column from mouse click position
        """

        # Find the row and column the user clicked on.
        column_clicked = mouse_pos[0] // (GRID_WIDTH + MARGIN)
        row_clicked = mouse_pos[1] // (GRID_HEIGHT + MARGIN)

        # If the user clicks below the final row, count it as the final row.
        if row_clicked >= ROWS:
            row_clicked = ROWS - 1
        if column_clicked >= COLUMNS:
            column_clicked = COLUMNS - 1

        return row_clicked, column_clicked

    def victory_check(self, click_grid):
        # If the amount of blocks clicked equals the amount of non_mines, user
        # has won. Assumes that the game over state immediately occurs
        # when the user clicks a mine.
        if click_grid.count_trues() == NON_MINES:
            self.game_screen.victory_screen()
            return True

        else:
            return False
            
    def game_over_check(self, row_clicked, column_clicked, mine_grid):
        if mine_grid.get_value(row_clicked, column_clicked):
            return True
        else:
            return False

    def click_block_event(self, row_clicked, 
        column_clicked, click_grid, flag_grid, mine_grid, mine_neighbor_grid):
        """
        Handles what occurs when a row and column are clicked.
        Returns the updated click_grid and the game_over variable.
        """
        click_grid.set_value(row_clicked, column_clicked, True)

        # If the block is mine-neighborless, reveal the neighbors of the
        # clicked block.
        if mine_neighbor_grid.get_value(row_clicked, column_clicked) == 0:
            self._reveal_neighbors(
                row_clicked, column_clicked,
                click_grid, mine_neighbor_grid, flag_grid)
                
        # If the user has a flag on that space, don't do anything when they
        # left click it.
        if flag_grid.get_value(row_clicked, column_clicked):
            click_grid.set_value(row_clicked, column_clicked, False)

        game_over = self.game_over_check(row_clicked, column_clicked, mine_grid)
        
        win_state = False
        
        if not game_over:
            win_state = self.victory_check(click_grid)
            
        return game_over, win_state

    def _reveal_neighbors(self, row, column, click_grid, mine_neighbor_grid, flag_grid):
        """
        Reveals all blocks next to a input block if the block has no
        mine-neighbors. If the block has no mine-neighbors, and one of its
        neighbors has no mine-neighbors, call this function on those neighbors.
        If the block is currently flagged, do not reveal
        """

        # Check to see if the block is on a border
        on_left_border = column == 0
        on_right_border = column == COLUMNS - 1
        on_top_border = row == 0
        on_bottom_border = row == ROWS - 1

        # Reveal the neighbors, if they exist. Check to see if the
        # neighbors themselves have mine-neighbors. Also, check to see
        # if the neighbors are already clicked.
        # If statements are necessary to prevent an out of range error.            
        if not on_left_border:
            neighborless = mine_neighbor_grid.get_value(row, column - 1) == 0
            clicked = click_grid.get_value(row, column - 1)
            click_grid.set_value(row, column - 1, True)

            if neighborless and not clicked:
                self._reveal_neighbors(
                    row, column - 1,
                    click_grid, mine_neighbor_grid, flag_grid)

        if not on_right_border:
            neighborless = mine_neighbor_grid.get_value(row, column + 1) == 0
            clicked = click_grid.get_value(row, column + 1)
            click_grid.set_value(row, column + 1, True)

            if neighborless and not clicked:
                self._reveal_neighbors(
                    row, column + 1,
                    click_grid, mine_neighbor_grid, flag_grid)

        if not on_top_border:
            neighborless = mine_neighbor_grid.get_value(row - 1, column) == 0
            clicked = click_grid.get_value(row - 1, column)
            click_grid.set_value(row - 1, column, True)

            if neighborless and not clicked:
                self._reveal_neighbors(
                    row - 1, column,
                    click_grid, mine_neighbor_grid, flag_grid)

        if not on_bottom_border:
            neighborless = mine_neighbor_grid.get_value(row + 1, column) == 0
            clicked = click_grid.get_value(row + 1, column)
            click_grid.set_value(row + 1, column, True)

            if neighborless and not clicked:
                self._reveal_neighbors(
                    row + 1, column,
                    click_grid, mine_neighbor_grid, flag_grid)

        # Reveal diagonals. Important that this comes last as to not
        # interfere with the recursion.
        if not on_left_border and not on_top_border:
            neighborless = mine_neighbor_grid.get_value(row - 1, column - 1) == 0
            clicked = click_grid.get_value(row - 1, column - 1)
            click_grid.set_value(row - 1, column - 1, True)

            if neighborless and not clicked:
                self._reveal_neighbors(row - 1, column - 1, 
                    click_grid, mine_neighbor_grid, flag_grid)

        if not on_left_border and not on_bottom_border:
            neighborless = mine_neighbor_grid.get_value(row + 1, column - 1) == 0
            clicked = click_grid.get_value(row + 1, column - 1)
            click_grid.set_value(row + 1, column - 1, True)

            if neighborless and not clicked:
                self._reveal_neighbors(row + 1, column - 1, 
                    click_grid, mine_neighbor_grid, flag_grid)

        if not on_right_border and not on_top_border:
            neighborless = mine_neighbor_grid.get_value(row - 1, column + 1) == 0
            clicked = click_grid.get_value(row - 1, column + 1)
            click_grid.set_value(row - 1, column + 1, True)

            if neighborless and not clicked:
                self._reveal_neighbors(row - 1, column + 1, 
                    click_grid, mine_neighbor_grid, flag_grid)

        if not on_right_border and not on_bottom_border:
            neighborless = mine_neighbor_grid.get_value(row + 1, column + 1) == 0
            clicked = click_grid.get_value(row + 1, column + 1)
            click_grid.set_value(row + 1, column + 1, True)

            if neighborless and not clicked:
                self._reveal_neighbors(row + 1, column + 1, 
                    click_grid, mine_neighbor_grid, flag_grid)
                    
        
        if flag_grid.get_value(row, column):
            click_grid.set_value(row, column, False)

    def restart(self, click_grid):
        self.game_screen.initial_draw()
        click_grid.reinitialize()

    def double_click_check(self, last_click_time):
        return pygame.time.get_ticks() - last_click_time > CLICK_WAIT

    def play(self):
        """
        This is the main loop of the program. It draws to the screen
        at appropriate times and controls the events of the game.
        """
        done = False
        game_over = False
        win_state = False

        # Variable to be used to check whether the game needs to be
        # re-drawn.
        click_count = 0

        last_click_time = pygame.time.get_ticks()

        click_grid = grid.Grid()
        mine_grid = grid.MineGrid()
        flag_grid = grid.FlagGrid()
        color_grid = grid.ColorGrid()
        mine_neighbor_grid = grid.MineNeighborGrid()

        # This grid changes during gameplay, so I initialize it in
        # the main game loop.
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = self.get_mouse_pos()
                    row_clicked, column_clicked = self.find_row_and_column_clicked(
                            mouse_pos)

                # Left click event
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if win_state or game_over:
                        self.restart(click_grid)
                        click_count = 0
                        win_state, game_over = False, False
                    
                    # Generate everything on first click
                    if click_count == 0:
                        mine_grid.generate_grid(row_clicked, column_clicked)
                        mine_neighbor_grid.generate_grid(mine_grid.grid)
                        color_grid.generate_grid(mine_grid.grid, mine_neighbor_grid.grid)
                        last_click_time = pygame.time.get_ticks()
                        click_count += 1

                    # Wait added to prevent accidental double clicks
                    if self.double_click_check(last_click_time):
                        last_click_time = pygame.time.get_ticks()
                        
                        game_over, win_state = self.click_block_event(
                            row_clicked, column_clicked, 
                            click_grid, flag_grid, 
                            mine_grid, mine_neighbor_grid)
                            
                        self.game_screen.update_grid(
                            click_grid, color_grid, mine_neighbor_grid)

                        # Display game over screen as soon as it occurs
                        if game_over:
                            self.game_screen.game_over_screen()

                    click_count += 1

                # Right click event
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if self.double_click_check(last_click_time):
                        last_click_time = pygame.time.get_ticks()

                        # Alternate between flagged and unflagged state.
                        flag_grid.set_flag(row_clicked, column_clicked)
                        self.game_screen.draw_flags(
                            row_clicked, column_clicked, click_grid, flag_grid)

            # Victory condition
            win_state = self.victory_check(click_grid)

            # Update screen.
            pygame.display.flip()

            self.clock.tick(60)

def main():
    game = Game()
    game.play()
    pygame.quit()

if __name__ == "__main__":
    main()
