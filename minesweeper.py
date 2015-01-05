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
        self.initialize_pygame()
        self.clock = pygame.time.Clock()
        self.game_screen = Screen()

    def initialize_pygame(self):
        """
        Initializes pygame-related things.
        """
        pygame.init()

    def generate_mine_grid(self, row_clicked, column_clicked):
        """
        Creates a randomly generated grid of mines.
        Ideally, this should happen after the first click by the user.
        """
        mine_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

        # Generate mines randomly. COLUMNS * ROWS gives us the total amount
        # of blocks on the playing ground. We then create a mine in the randomly
        # selected spaces. We create one more than we need in case 
        mines = random.sample(range(COLUMNS*ROWS), MINES + 1)
        for mine in mines[:-1]:
            # Unpack the row and column from the integer "mine"
            mine_row = mine // COLUMNS
            mine_column = mine % COLUMNS
            
            # If a mine is generated where the user clicked, use the extra mine
            # we generated in its place.
            if row_clicked == mine_row and mine_column == mine_row:
                mine_row = mines[MINES] // COLUMNS
                mine_column = mines[MINES] % COLUMNS
            
            mine_grid[mine_row][mine_column] = 1
            
        if mine_grid[row_clicked][column_clicked] == 1:
            mine_grid[row_clicked][column_clicked] = 0
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
                mine_neighbor_grid[row][column] = self._count_mine_neighbors(
                    row, column, mine_grid)

        return mine_neighbor_grid

    def _count_mine_neighbors(self, row, column, mine_grid):
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

    def click_block_event(self, row_clicked, column_clicked, click_grid, flag_grid, mine_grid, mine_neighbor_grid):
        """
        Handles what occurs when a row and column are clicked.
        Returns the updated click_grid and the game_over variable.
        """
        # Initialize game over variable
        game_over = False

        click_grid[row_clicked][column_clicked] = 1

        # If the user has a flag on that space, don't do anything when they
        # left click it.
        if flag_grid[row_clicked][column_clicked] == 1:
            click_grid[row_clicked][column_clicked] = 0


        # End the game if the user has clicked on a mine
        elif mine_grid[row_clicked][column_clicked] == 1:
            game_over = True

        # If the block is mine-neighborless, reveal the neighbors of the 
        # clicked block.
        elif mine_neighbor_grid[row_clicked][column_clicked] == 0:
            self._reveal_neighbors(
                row_clicked,
                column_clicked,
                click_grid,
                mine_neighbor_grid)

        return click_grid, game_over

    def _reveal_neighbors(self, row, column, click_grid, mine_neighbor_grid):
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
            self._reveal_neighbors(
                row, column - 1,
                click_grid, mine_neighbor_grid)
        if not on_right_border and neighborless_right and not clicked_right:
            self._reveal_neighbors(
                row, column + 1,
                click_grid, mine_neighbor_grid)
        if not on_top_border and neighborless_up and not clicked_up:
            self._reveal_neighbors(
                row - 1, column,
                click_grid, mine_neighbor_grid)
        if not on_bottom_border and neighborless_down and not clicked_down:
            self._reveal_neighbors(
                row + 1, column,
                click_grid, mine_neighbor_grid)

        # Reveal diagonals. Important that this comes last as to not
        # interfere with the recursion.
        if not on_left_border and not on_top_border:
            neighborless = mine_neighbor_grid[row - 1][column - 1] == 0
            clicked = click_grid[row - 1][column - 1] == 1
            click_grid[row - 1][column - 1] = 1
            
            if neighborless and not clicked:
                self._reveal_neighbors(row - 1, column - 1, click_grid, mine_neighbor_grid)
        
        if not on_left_border and not on_bottom_border:
            neighborless = mine_neighbor_grid[row + 1][column - 1] == 0
            clicked = click_grid[row + 1][column - 1] == 1
            click_grid[row + 1][column - 1] = 1
            
            if neighborless and not clicked:
                self._reveal_neighbors(row + 1, column - 1, click_grid, mine_neighbor_grid)
        
        if not on_right_border and not on_top_border:
            neighborless = mine_neighbor_grid[row - 1][column + 1] == 0
            clicked = click_grid[row - 1][column + 1] == 1
            click_grid[row - 1][column + 1] = 1
            
            if neighborless and not clicked:
                self._reveal_neighbors(row - 1, column + 1, click_grid, mine_neighbor_grid)
                
        if not on_right_border and not on_bottom_border:
            neighborless = mine_neighbor_grid[row + 1][column + 1] == 0
            clicked = click_grid[row + 1][column + 1] == 1
            click_grid[row + 1][column + 1] = 1
            
            if neighborless and not clicked:
                self._reveal_neighbors(row + 1, column + 1, click_grid, mine_neighbor_grid)

        return click_grid

    def restart(self):
        #self.mine_grid = self.generate_mine_grid()
        #self.mine_neighbor_grid = self.get_mine_neighbor_grid(self.mine_grid)
        #self.color_grid = self.get_color_grid(
            #self.mine_grid,
            #self.mine_neighbor_grid)

        self.game_screen.initial_draw()

    def play(self):
        """
        This is the main loop of the program. It draws to the screen
        at appropriate times and controls the events of the game.
        """
        done = False

        # Variable to be used to check whether the game needs to be
        # re-drawn.
        left_click = False
        right_click = False
        game_over = False
        restart = False
        first_click = False
        clicks = 0
        
        time_clicked = pygame.time.get_ticks()
        
        click_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        flag_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

        # This grid changes during gameplay, so I initialize it in
        # the main game loop.
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # Left click event
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = self.mouse_down()

                    # Wait added to prevent accidental double clicks
                    if pygame.time.get_ticks() - time_clicked > CLICK_WAIT:
                        left_click = True
                        time_clicked = pygame.time.get_ticks()
                        
                        if clicks == 0:
                            clicks += 1
                            first_click = True
                
                # Right click event
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    mouse_pos = self.mouse_down()

                    if pygame.time.get_ticks() - time_clicked > CLICK_WAIT:
                        time_clicked = pygame.time.get_ticks()
                        right_click = True
            
            if first_click:
                row_clicked, column_clicked = self.find_row_and_column_clicked(
                    mouse_pos)
                mine_grid = self.generate_mine_grid(row_clicked, column_clicked)
                mine_neighbor_grid = self.get_mine_neighbor_grid(mine_grid)
                color_grid = self.get_color_grid(mine_grid, mine_neighbor_grid)
                first_click = False

            
            # If the user has left clicked since the last iteration, 
            # handle the event, check the game over status, and
            # redraw the screen.
            if left_click and not game_over:
                # Get the row and column of the block clicked.
                row_clicked, column_clicked = self.find_row_and_column_clicked(
                    mouse_pos)
                click_grid, game_over = self.click_block_event(
                    row_clicked, column_clicked, click_grid, flag_grid, mine_grid, mine_neighbor_grid)
                self.game_screen.update_grid(
                    click_grid, color_grid, mine_neighbor_grid)
                
                # Since the event has been handled on this iteration, do not
                # handle it on the next iteration unless they click again.
                left_click = False
                
            elif right_click and not game_over:
                row_clicked, column_clicked = self.find_row_and_column_clicked(
                    mouse_pos)
                
                # Alternate between flagged and unflagged state.
                flag_grid[row_clicked][column_clicked] += 1
                flag_grid[row_clicked][column_clicked] %= 2
                
                self.game_screen.draw_flags(
                    row_clicked, column_clicked, click_grid, flag_grid)
                
                right_click = False

            # Game over condition
            elif game_over:
                self.game_screen.game_over_screen()
                if left_click:
                    restart = True
                elif right_click:
                    done = True

            # Victory condition
            total_clicked_blocks = len([x for y in click_grid 
                                        for x in y if x==1])

            if total_clicked_blocks == NON_MINES:
                game_over = True
                self.game_screen.victory_screen()

            # Update screen.
            pygame.display.flip()

            self.clock.tick(60)

            if restart:
                click_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
                self.restart()
                left_click = False
                right_click = False
                game_over = False
                restart = False
                first_click = True
                time_clicked = pygame.time.get_ticks()

def main():
    game = Game()
    game.play()
    pygame.quit()

if __name__ == "__main__":
    main()
