from constants import *
import random

class Grid:
    def __init__(self):
        self.grid = [[False for x in range(COLUMNS)] for y in range(ROWS)]
        
    def set_value(self, row, column, value):
        """This class adds value to a specific block of the grid."""
        self.grid[row][column] = value
        
    def get_value(self, row, column):
        return self.grid[row][column]
        
    def initialize(self):
        self.grid = [[False for x in range(COLUMNS)] for y in range(ROWS)]
        
    def count_trues(self):
        return len([x for y in self.grid for x in y if x])
        
class MineGrid(Grid):
    def __init__(self):
        self.grid = [[False for x in range(ROWS)] for y in range(COLUMNS)]
        
    def generate_grid(self, row_clicked, column_clicked):
        """
        Creates a randomly generated grid of mines.
        Ideally, this should happen after the first click by the user.
        """
        # Generate mines randomly. COLUMNS * ROWS gives us the total amount
        # of blocks on the playing ground. We then create a mine in the randomly
        # selected spaces. We create one more than we need in case 
        self.grid = [[False for x in range(COLUMNS)] for y in range(ROWS)]

        mines = random.sample(range(COLUMNS*ROWS), MINES + 1)
        
        # Loop over all but the last one (since we generate one more than we need 
        for mine in mines[:-1]:
            # Unpack the row and column from the integer "mine"
            mine_row = mine // COLUMNS
            mine_column = mine % COLUMNS
            
            # If a mine is generated where the user clicked, use the extra mine
            # we generated in its place.
            if row_clicked == mine_row and mine_column == mine_row:
                mine_row = mines[MINES] // COLUMNS
                mine_column = mines[MINES] % COLUMNS
            
            self.grid[mine_row][mine_column] = True
        
        # Test to see if this code is necessary
        if self.grid[row_clicked][column_clicked] == True:
            self.grid[row_clicked][column_clicked] = False
            
class MineNeighborGrid(Grid):
    def __init__(self):
        """
        Creates a ROWS by COLUMNS grid that holds what color each
        block should be. This is based on the amount of mine-neighbors
        each block has.
        """
        self.grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
    
    def generate_grid(self, mine_grid):
        """
        Creates the grid that holds how many mine-neighbors each space
        has. In the original, this is the number that is displayed on
        the block after they have been clicked.
        """
        self.grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.grid[row][column] = self._count_mine_neighbors(
                    row, column, mine_grid)

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
        
class ColorGrid(Grid):
    def __init__(self):
        self.grid = [[WHITE for x in range(COLUMNS)] for y in range(ROWS)]
    
    def generate_grid(self, mine_grid, mine_neighbor_grid):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if mine_grid[row][column] == 1:
                    self.grid[row][column] = COLOR_DICT['MINE']
                else:
                    self.grid[row][column] = COLOR_DICT[
                        mine_neighbor_grid[row][column]]

class FlagGrid(Grid):
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.grid = [[False for x in range(COLUMNS)] for y in range(COLUMNS)]
        self.flag_count = 0
        
    def set_flag(self, row, column, click_grid):
        # Turn on/off flag.
        if not click_grid.get_value(row, column):
            self.grid[row][column] = not self.grid[row][column]
            
            if self.grid[row][column]:
                self.flag_count += 1
            else:
                self.flag_count -= 1
            
    def get_value(self, row, column):
        return self.grid[row][column]
