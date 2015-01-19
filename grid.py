import random
from block import Block


class Grid:
    """This class handles the grid of the game and its properties. It is
    responsible for generating elements associated with the grid like
    mines and Blocks, as well as some properties associated with the Block.

    Parameters:
    blocks = 2D list of Block objects.
    row_count = number of rows in the grid
    col_count = number of columns in the grid
    mine_count = number of mines in the grid
    """
    def __init__(self, click_position):
        # Default to beginner game
        self.row_count = 9
        self.col_count = 9
        self.mine_count = 10

        self.initialize_grid(click_position)

    def __str__(self):
        block_list = list()

        for row in self.blocks:
            for block in row:
                if block.is_mine:
                    block_list.append('M')
                elif block.is_revealed and block.mine_neighbor_count == 0:
                    block_list.append('~')
                else:
                    block_list.append(str(block.mine_neighbor_count))
            block_list.append('\n')

        return ''.join(block_list)

    def initialize_grid(self, click_position):
        """Create mines and blocks based on initial click position.
        Reveal the blocks around the initial clicked block.

        Keyword arguments:
        click_position - tuple containing the x-pixel and y-pixel that the
        mouse has clicked
        """
        row, col = self._find_clicked_row_col(click_position)
        mines = self._generate_mines(row, col)
        mine_grid = self._calc_mine_grid(mines)
        mine_neighbor_grid = self._calc_mine_neighbors(mines)

        self.blocks = [[Block(mine_grid[x][y], mine_neighbor_grid[x][y])
                       for x in range(self.row_count)]
                       for y in range(self.col_count)]

        self._reveal_around(row, col)

    def click_grid(self, click_position, click_type):
        """Updates the grid based on the a mouse click.
        Takes in
        """
        row, col = self._find_clicked_row_col(click_position)
        if click_type == "left":
            self.blocks[row][col].reveal()
            self.blocks[row][col].draw()
            if self.blocks[row][col].mine_neighbors == 0:
                self.reveal_around(row, col)

        elif click_type == "right":
            self.blocks[row][col].cycle_flag()
            self.blocks[row][col].draw()

    def update_params(self, row_count, col_count, mine_count):
        """Change the parameters of the grid.
        """
        self.row_count = row_count
        self.col_count = col_count
        self.mine_count = mine_count
        assert(mine_count < row_count * col_count - 8)

    def _reveal_around(self, row_clicked, col_clicked):
        # Find all blocks around the clicked block
        neighbors = self._find_neighbors(row_clicked, col_clicked)

        for neighbor in neighbors:
            row = neighbor[0]
            col = neighbor[1]

            neighborless = self.blocks[row][col].mine_neighbor_count == 0
            revealed = self.blocks[row][col].is_revealed
            self.blocks[row][col].reveal()

            if neighborless and not revealed:
                self._reveal_around(row, col)

    def _generate_mines(self, row_clicked, col_clicked):
        """
        Create mines for the grid. This will not create any mines within
        1 block of the block that the user clicked.

        Return a 2D list of coordinates corresponding to the
        locations of mines.
        """
        mines = random.sample(range(self.col_count * self.row_count),
                              self.mine_count + 8)

        # Compose the integers into grid rows and columns
        mine_rows = [x // self.col_count for x in mines]
        mine_cols = [x % self.col_count for x in mines]
        mine_grid = set(zip(mine_rows, mine_cols))

        # Mines should not be generated in any block around the
        # clicked block.
        invalid_zones = self._find_neighbors(row_clicked, col_clicked)

        # Remove mines that were generated in the invalid zone
        invalid_mines = invalid_zones & mine_grid
        mine_grid = list(mine_grid - invalid_mines)

        # Since we made extra mines just in case, only return the number
        # of mines we need.
        return mine_grid[:self.mine_count]

    def _calc_mine_grid(self, mines):
        mine_grid = [[False for x in range(self.row_count)]
                     for y in range(self.col_count)]

        for mine in mines:
            mine_grid[mine[0]][mine[1]] = True

        return mine_grid

    def _calc_mine_neighbors(self, mines):
        """
        Take a list of 2-tuples corresponding to coordinates of
        mine locations and return a 2D list of integers corresponding
        to the mine neighbor count of all of the blocks.
        """
        mine_neighbor_grid = [[0 for x in range(self.row_count)]
                              for y in range(self.col_count)]

        for mine in mines:
            mine_row = mine[0]
            mine_col = mine[1]
            neighbors = self._find_neighbors(mine_row, mine_col)

            for neighbor in neighbors:
                neighbor_row = neighbor[0]
                neighbor_col = neighbor[1]
                mine_neighbor_grid[neighbor_row][neighbor_col] += 1

        return mine_neighbor_grid

    def _find_neighbors(self, row, col):
        """
        Return a set of 2-tuples containing the neighbors of the
        input row and column. (Return set that is just +/- 1 of row and col
        and make sure that it isn't negative or past the number of rows.)
        """
        neighbors = {(row + x, col + y)
                     for x in range(-1, 2) for y in range(-1, 2)}

        # Take into account edge and corner cases (literally!)
        return {neighbor for neighbor in neighbors
                if neighbor[0] >= 0 and neighbor[1] >= 0
                and neighbor[0] < self.row_count and
                neighbor[1] < self.col_count}

    def _find_clicked_row_col(self, click_position):
        """
        Convert the tuple of a mouse click position (given in pixels, x
        and y position) to a tuple of block position on the grid.
        """
        column_clicked = click_position[0] // \
            (Block.BLOCK_WIDTH + Block.MARGIN)

        row_clicked = click_position[1] // (Block.BLOCK_HEIGHT + Block.MARGIN)

        # If the user clicks below the final row, count it as the final row.
        if row_clicked >= self.row_count:
            row_clicked = self.row_count - 1
        if column_clicked >= self.col_count:
            column_clicked = self.col_count - 1

        return row_clicked, column_clicked

if __name__ == "__main__":
    # Demo
    grid = Grid((120, 120))
    print(grid)

    grid.update_params(20, 20, 40)
    grid.initialize_grid((120, 120))
    print(grid)
