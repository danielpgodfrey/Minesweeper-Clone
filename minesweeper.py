import pygame
import random

from constants import *
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
        self.mine_grid = self.generate_mine_grid()
        self.mine_neighbor_grid = self.get_mine_neighbor_grid(self.mine_grid)
        self.color_grid = self.get_color_grid(
            self.mine_grid,
            self.mine_neighbor_grid)

        self.initialize_pygame()
        self.clock = pygame.time.Clock()
        self.game_screen = Screen()
        self.main_loop()

    def initialize_pygame(self):
        """
        Initializes pygame-related things.
        """
        pygame.init()

    def generate_mine_grid(self):
        """
        Creates a randomly generated grid of mines.
        Ideally, this should happen after the first click by the user.
        """
        mine_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        laid_mines = 0
        assert(MINES < ROWS * COLUMNS)

        # Generate mines randomly.
        while laid_mines < MINES:
            row = random.randrange(0, ROWS)
            column = random.randrange(0, COLUMNS)
            if mine_grid[row][column] == 0:
                mine_grid[row][column] = 1
                laid_mines += 1

        return mine_grid

    def get_mine_neighbor_grid(self, mine_grid):
        """
        Creates the grid that holds how many mine-neighbors each space
        has. In the original, this is the number that is displayed on
        the block after they have been clicked.
        """
        mine_neighbor_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        for row in range(ROWS):
            for column in range(COLUMNS):
                mine_neighbor_grid[row][column] = self.__count_mine_neighbors(
                    row, column, mine_grid)

        return mine_neighbor_grid

    def __count_mine_neighbors(self, row, column, mine_grid):
        mine_neighbor_count = 0

        # Check whether the block is on an edge.
        left = row >= 1
        right = row < ROWS - 1
        up = column >= 1
        down = column < COLUMNS - 1

        # Check left, up-left, and down-left for mines.
        if left:
            if mine_grid[row - 1][column] == 1:
                mine_neighbor_count += 1
            if up and mine_grid[row - 1][column - 1] == 1:
                mine_neighbor_count += 1
            if down and mine_grid[row - 1][column + 1] == 1:
                mine_neighbor_count += 1

        # Check right, up-right, and down-right for mines.
        if right:
            if mine_grid[row + 1][column] == 1:
                mine_neighbor_count += 1
            if up and mine_grid[row + 1][column - 1] == 1:
                mine_neighbor_count += 1
            if down and mine_grid[row + 1][column + 1] == 1:
                mine_neighbor_count += 1

        # Check up and down for mines.
        if up and mine_grid[row][column - 1] == 1:
            mine_neighbor_count += 1
        if down and mine_grid[row][column + 1] == 1:
            mine_neighbor_count += 1

        return mine_neighbor_count

    def get_color_grid(self, mine_grid, mine_neighbor_grid):
        """
        Creates a ROWS by COLUMNS grid that holds what color each
        block should be. This is based on the amount of mine-neighbors
        each block has.
        """
        color_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        for row in range(ROWS):
            for column in range(COLUMNS):
                if mine_grid[row][column] == 1:
                    color_grid[row][column] = RED
                elif mine_neighbor_grid[row][column] == 0:
                    color_grid[row][column] = BLUE
                elif mine_neighbor_grid[row][column] == 1:
                    color_grid[row][column] = CYAN
                elif mine_neighbor_grid[row][column] == 2:
                    color_grid[row][column] = DARKGREEN
                elif mine_neighbor_grid[row][column] == 3:
                    color_grid[row][column] = GREEN
                elif mine_neighbor_grid[row][column] == 4:
                    color_grid[row][column] = LITEGREEN
                elif mine_neighbor_grid[row][column] == 5:
                    color_grid[row][column] = PURPLE
                elif mine_neighbor_grid[row][column] == 6:
                    color_grid[row][column] = PINK
                elif mine_neighbor_grid[row][column] == 7:
                    color_grid[row][column] = YELLOW
                elif mine_neighbor_grid[row][column] == 8:
                    color_grid[row][column] = ORANGE

        return color_grid

    def mouse_down(self):
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

    def click_block_event(self, row_clicked, column_clicked, click_grid):
        """
        Handles what occurs when a row and column are clicked.
        Returns the updated click_grid and the game_over variable.
        """
        # Initialize game over variable
        game_over = False

        click_grid[row_clicked][column_clicked] = 1

        # End the game if the user has clicked on a mine
        if self.mine_grid[row_clicked][column_clicked] == 1:
            game_over = True

        # Reveal the neighbors of the clicked block
        elif self.mine_neighbor_grid[row_clicked][column_clicked] == 0:
            self.__reveal_neighbors(
                row_clicked,
                column_clicked,
                click_grid,
                self.mine_neighbor_grid)

        return click_grid, game_over

    def __reveal_neighbors(self, row, column, click_grid, mine_neighbor_grid):
        """
        Reveals all blocks next to a input block if the block has no
        mine-neighbors. If the block has no mine-neighbors, and one of its
        neighbors has no mine-neighbors, call this function on those neighbors
        """
        assert mine_neighbor_grid[row][column] == 0

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
            neighborless_left = mine_neighbor_grid[row][column - 1] == 0
            clicked_left = click_grid[row][column - 1] == 1
            click_grid[row][column - 1] = 1

        if not on_right_border:
            neighborless_right = mine_neighbor_grid[row][column + 1] == 0
            clicked_right = click_grid[row][column + 1] == 1
            click_grid[row][column + 1] = 1

        if not on_top_border:
            neighborless_up = mine_neighbor_grid[row - 1][column] == 0
            clicked_up = click_grid[row - 1][column] == 1
            click_grid[row - 1][column] = 1

        if not on_bottom_border:
            neighborless_down = mine_neighbor_grid[row + 1][column] == 0
            clicked_down = click_grid[row + 1][column] == 1
            click_grid[row + 1][column] = 1

        # Call the function on the neighbors that have no mine-neighbors
        if not on_left_border and neighborless_left and not clicked_left:
            self.__reveal_neighbors(
                row, column - 1,
                click_grid, mine_neighbor_grid)
        if not on_right_border and neighborless_right and not clicked_right:
            self.__reveal_neighbors(
                row, column + 1,
                click_grid, mine_neighbor_grid)
        if not on_top_border and neighborless_up and not clicked_up:
            self.__reveal_neighbors(
                row - 1, column,
                click_grid, mine_neighbor_grid)
        if not on_bottom_border and neighborless_down and not clicked_down:
            self.__reveal_neighbors(
                row + 1, column,
                click_grid, mine_neighbor_grid)

        # Reveal diagonals. Important that this comes last as to not
        # interfere with the recursion.
        if not on_left_border and not on_top_border:
            neighborless = mine_neighbor_grid[row - 1][column - 1] == 0
            clicked = click_grid[row - 1][column - 1] == 1
            click_grid[row - 1][column - 1] = 1
            
            if neighborless and not clicked:
                self.__reveal_neighbors(row - 1, column - 1, click_grid, mine_neighbor_grid)
        
        if not on_left_border and not on_bottom_border:
            neighborless = mine_neighbor_grid[row + 1][column - 1] == 0
            clicked = click_grid[row + 1][column - 1] == 1
            click_grid[row + 1][column - 1] = 1
            
            if neighborless and not clicked:
                self.__reveal_neighbors(row + 1, column - 1, click_grid, mine_neighbor_grid)
        
        if not on_right_border and not on_top_border:
            neighborless = mine_neighbor_grid[row - 1][column + 1] == 0
            clicked = click_grid[row - 1][column + 1] == 1
            click_grid[row - 1][column + 1] = 1
            
            if neighborless and not clicked:
                self.__reveal_neighbors(row - 1, column + 1, click_grid, mine_neighbor_grid)
                
        if not on_right_border and not on_bottom_border:
            neighborless = mine_neighbor_grid[row + 1][column + 1] == 0
            clicked = click_grid[row + 1][column + 1] == 1
            click_grid[row + 1][column + 1] = 1
            
            if neighborless and not clicked:
                self.__reveal_neighbors(row + 1, column + 1, click_grid, mine_neighbor_grid)

        return click_grid

    def restart(self):
        self.mine_grid = self.generate_mine_grid()
        self.mine_neighbor_grid = self.get_mine_neighbor_grid(self.mine_grid)
        self.color_grid = self.get_color_grid(
            self.mine_grid,
            self.mine_neighbor_grid)

        self.game_screen.initial_draw()

    def main_loop(self):
        """
        This is the main loop of the program. It draws to the screen
        at appropriate times and controls the events of the game.
        """
        done = False

        # Variable to be used to check whether the game needs to be
        # re-drawn.
        new_click = False
        game_over = False
        restart = False
        click_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

        # This grid changes during gameplay, so I initialize it in
        # the main game loop.
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    mouse_pos = self.mouse_down()
                    new_click = True
                if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                    restart = True

            # If the user has clicked since the last iteration, handle
            # the event, check the game over status, and
            # redraw the screen.
            if new_click:
                # Get the row and column of the block clicked.
                row_clicked, column_clicked = self.find_row_and_column_clicked(
                    mouse_pos)
                click_grid, game_over = self.click_block_event(
                    row_clicked, column_clicked, click_grid)
                self.game_screen.update_grid(click_grid, self.color_grid)
                new_click = False

            elif game_over:
                self.game_screen.game_over_screen()

            total_clicked_blocks = len([x for y in click_grid for x in y if x==1])

            if total_clicked_blocks == NON_MINES:
                game_over = True
                self.game_screen.victory_screen()

            # Update the screen with what is drawn.
            pygame.display.flip()

            self.clock.tick(60)

            if restart:
                click_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
                self.restart()
                game_over = False
                restart = False

def main():
    game = Game()
    pygame.quit()

if __name__ == "__main__":
    main()
