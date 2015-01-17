import random
from block import Block
from constants import *

class Grid:
    """
    This class handle the grid of the game and it properties. It is
    responsible for generating elements associated with the grid like
    Blocks, as well as any properties associated with the Block.

    Parameters:
    blocks = number of Block objects equal to amount of self.row_count * self.col_count
    in the current game.
    """
    def __init__(self, click_position):
        row, col = find_clicked_row_column(click_position)
        
        self.row_count = 9
        self.col_count = 9
        
        mines = self.generate_mines(row, col)
        mine_grid = self.calc_mine_grid(mines)
        mine_neighbor_grid = self.calc_mine_neighbors(mines)

        self.blocks = [[Block(mine_grid[x][y], mine_neighbor_grid[x][y])
            for x in range(self.row_count)] for y in range(self.col_count)]

    def update_grid(self, click_position, click_type):
        """
        Updates the grid based on the click.
        """

        row, col = find_clicked_row_column(click_position)
        if click_type == "left":
            self.blocks[row][col].reveal()
            self.blocks[row][col].draw()
            if self.blocks[row][col].mine_neighbors == 0:
                self.reveal_around(row, column)

        elif click_type == "right":
            self.blocks[row][col].cycle_flag()
            self.blocks[row][col].draw()

    def reveal_around(self, row_clicked, col_clicked):
        # Find all blocks around the clicked block
        neighbors = find_neighbors(row_clicked, column_clicked)

        for neighbor in neighbors:
            row = neighbor[0]
            col = neighbor[1]
            self.block[row][col].reveal()

            neighborless = self.block[row][col].mine_neighbor_count == 0
            revealed = self.blocks[row][col].is_revealed

            if neighborless and not revealed:
                self.reveal_around(row, col)

    @staticmethod
    def generate_mines(row_clicked, col_clicked):
        """
        Creates mines for the grid. This will not create any mines within
        1 block of the block that the user clicked.

        Returns a 2D list of coordinates corresponding to the
        locations of mines.
        """
        mines = random.sample(range(self.col_count * self.row_count), MINES + 8)

        # Compose the integers into grid rows and self.col_count
        mine_rows = [x // self.col_count for x in mines]
        mine_cols = [x % self.col_count for x in mines]
        mine_grid = list(zip(mine_rows, mine_cols))
        
        # Mines should not be generated in any block around the
        # clicked block.
        invalid_zones = Grid.find_neighbors(row_clicked, col_clicked)
        
        # Remove mines that were generated in the invalid zone
        invalid_mines = list(set(invalid_zones) & set(mine_grid))
        mine_grid = list(set(mine_grid) - set(invalid_mines))
    
        # Since we made extra mines just in case, only return the number
        # of mines we need.
        return mine_grid[:MINES - 1]

    @staticmethod
    def calc_mine_grid(mines):
        mine_grid = [[False for x in range(self.row_count)] 
            for y in range(self.col_count)]
        
        for mine in mines:
            mine_grid[mine[0]][mine[1]] = True
        
        return mine_grid

    @staticmethod
    def calc_mine_neighbors(mines):
        """
        Takes a list of 2-tuples corresponding to coordinates of
        mine locations and returns a 2D list of integers corresponding
        to the mine neighbor count of all of the blocks.
        """
        mine_neighbor_grid = [[0 for x in range(self.row_count)] for y in range(self.col_count)]
        for mine in mines:
            mine_row = mine[0]
            mine_col = mine[1]
            neighbors = Grid.find_neighbors(mine_row, mine_col)
            
            for neighbor in neighbors:
                neighbor_row = neighbor[0]
                neighbor_col = neighbor[1]
                mine_neighbor_grid[neighbor_row][neighbor_col] += 1
                
        return mine_neighbor_grid

    @staticmethod
    def find_neighbors(row, col):
        """
        Returns a list of 2-tuples containing the neighbors of the 
        input row and column. (Returns tuple that just +/- 1 for row and col
        and makes sure that it isn't negative.)
        """
        neighbors = [(row + x, col + y)
            for x in range(-1, 2) for y in range(-1, 2)]

        # Take into account edge and corner cases (literally!)
        return [neighbor for neighbor in neighbors
            if neighbor[0] >= 0 and neighbor[1] >= 0 
            and neighbor[0] < self.row_count and neighbor[1] < self.col_count]

if __name__ == "__main__":
    grid = Grid('a')
    for block in grid.blocks:
        print(block)
