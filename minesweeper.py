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
        Gets the position of the mouse from pygame.
        """
        pos = pygame.mouse.get_pos()
        return pos

    def find_row_and_column_clicked(self, mouse_pos):
        """
        Returns row and column from mouse click position.
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

    def check_victory(self, click_grid):
        """
        Draws the victory screen when as many blocks are clicked as there are
        non-mines. Assumes that the game over state immediately occurs
        when the user clicks a mine.
        """
        if click_grid.count_trues() == NON_MINES:
            return True

        else:
            return False

    def check_game_over(self, row, column, mine_grid, flag_grid):
        """
        Checks if the user has lost, and draws to the screen
        appropriately.
        """
        if mine_grid.get_value(row, column) and not flag_grid.get_value(row, column):
            return True
        else:
            return False

    def reveal_block(self, row_clicked,
        column_clicked, click_grid, flag_grid, mine_grid, mine_neighbor_grid):
        """
        Handles what occurs when a row and column are clicked.
        Updates the click_grid.
        """
        if flag_grid.get_value(row_clicked, column_clicked):
            return

        click_grid.set_value(row_clicked, column_clicked, True)

        # If the block is mine-neighborless, reveal the neighbors of the
        # clicked block.
        if mine_neighbor_grid.get_value(row_clicked, column_clicked) == 0:
            self._reveal_neighbors(
                row_clicked, column_clicked,
                click_grid, mine_neighbor_grid, flag_grid, mine_grid)

    def _reveal_neighbors(self, row, column, click_grid, mine_neighbor_grid, flag_grid, mine_grid):
        """
        Reveals all blocks next to a input block if the block has no
        mine-neighbors. If the block has no mine-neighbors, and one of its
        neighbors has no mine-neighbors, call this function on those neighbors.
        If the block is currently flagged, it does not reveal that block.
        """
        if mine_grid.get_value(row, column):
            return
        
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
            self._reveal_call(row, column - 1, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if not on_right_border:
            self._reveal_call(row, column + 1, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if not on_top_border:
            self._reveal_call(row - 1, column, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if not on_bottom_border:
            self._reveal_call(row + 1, column, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        # Reveal diagonals
        if not on_left_border and not on_top_border:
            self._reveal_call(row - 1, column - 1, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if not on_left_border and not on_bottom_border:
            self._reveal_call(row + 1, column - 1, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if not on_right_border and not on_top_border:
            self._reveal_call(row - 1, column + 1, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if not on_right_border and not on_bottom_border:
            self._reveal_call(row + 1, column + 1, click_grid, mine_neighbor_grid, flag_grid, mine_grid)

        if flag_grid.get_value(row, column):
            click_grid.set_value(row, column, False)

    def _reveal_call(self, row, column, click_grid, mine_neighbor_grid, flag_grid, mine_grid):
        to_reveal = self._check_to_reveal(row, column,
            click_grid, flag_grid)

        if to_reveal:
            click_grid.set_value(row, column, True)
            neighborless = mine_neighbor_grid.get_value(row, column) == 0
            if neighborless:
                self._reveal_neighbors(
                    row, column,
                    click_grid, mine_neighbor_grid, flag_grid, mine_grid)

    def _check_to_reveal(self, row, column, click_grid, flag_grid):
            clicked = click_grid.get_value(row, column)
            flagged = flag_grid.get_value(row, column)

            if not clicked and not flagged:
                return True
            else:
                return False

    def restart(self, click_grid, flag_grid):
        """
        Handles what should occur on game restart. The screen should return
        to the initial state, and the click_grid should be reinitialized.
        """
        self.game_screen.initial_draw()
        click_grid.initialize()
        flag_grid.initialize()

    def is_double_click(self, last_click_time):
        """
        Returns if the current time and the last time the user clicked
        exceeds the constant CLICK_WAIT time.
        """
        return pygame.time.get_ticks() - last_click_time < CLICK_WAIT

    def play(self):
        """
        This is the main loop of the program. It draws to the screen
        at appropriate times and controls the events of the game.
        """
        done = False
        game_over = False
        win_state = False
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
                    # Generate everything on first click

                    # Wait added to prevent accidental double clicks
                    if not self.is_double_click(last_click_time):
                        if not game_over and not win_state:
                            if click_count == 0:
                                mine_grid.generate_grid(
                                    row_clicked, column_clicked)
                                
                                mine_neighbor_grid.generate_grid(mine_grid.grid)
                                color_grid.generate_grid(
                                    mine_grid.grid, mine_neighbor_grid.grid)
                                
                                start_time = pygame.time.get_ticks()
                                                        
                            last_click_time = pygame.time.get_ticks()
                            
                            self.reveal_block(
                                row_clicked, column_clicked,
                                click_grid, flag_grid,
                                mine_grid, mine_neighbor_grid)

                            self.game_screen.update_grid(
                                click_grid, color_grid, mine_neighbor_grid)
                                
                            game_over = self.check_game_over(
                                row_clicked, column_clicked,
                                mine_grid, flag_grid)
                                
                            win_state = self.check_victory(click_grid)

                            click_count += 1

                        else:
                            self.restart(click_grid, flag_grid)
                            win_state, game_over = False, False
                            click_count = 0


                # Right click event
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if win_state or game_over:
                        done = True

                    if not self.is_double_click(last_click_time):
                        last_click_time = pygame.time.get_ticks()

                        # Alternate between flagged and unflagged state.
                        flag_grid.set_flag(row_clicked, column_clicked, click_grid)
                        self.game_screen.draw_flags(
                            row_clicked, column_clicked, click_grid, flag_grid)

            if game_over:
                self.game_screen.game_over_screen(mine_grid, click_grid, flag_grid)
            elif win_state:
                self.game_screen.victory_screen(mine_grid)

            if click_count > 0 and not game_over and not win_state:
                current_time = pygame.time.get_ticks() - start_time
                self.game_screen._display_time_counter(current_time // 1000)
                
            # Update screen.
            pygame.display.flip()

            self.clock.tick(60)

def main():
    game = Game()
    game.play()
    pygame.quit()

if __name__ == "__main__":
    main()
