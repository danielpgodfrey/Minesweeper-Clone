from block import Block

class Grid:
    """
    This class handle the grid of the game and it properties. It is 
    responsible for generating elements associated with the grid like
    Blocks, as well as any properties associated with the Block.
    
    Parameters:
    blocks = number of Block objects equal to amount of ROWS * COLS
    in the current game.
    """
    def __init__(self, click_position):
        row, col = find_clicked_row_column(click_position)
        mines = generate_mines(row, col)
        mine_neighbors = calc_mine_neighbors(mines)
        self.blocks = [[Block(mines[x][y]) for y in range(COLUMNS)] 
            for x in range(ROWS)]

    def update_grid(self, click_position, click_type):
        """
        Updates the grid based on the click.
        """
        
        row, col = find_clicked_row_column(click_position)
        if click_type == "left":
            self.blocks[row][column].reveal_block()
            self.blocks[row][column].draw_block()
            if self.blocks[row][column].mine_neighbors == 0:
                self.reveal_around(row, column)
        
        elif click_type == "right":
            self.blocks[row][column].cycle_flag()
            self.blocks[row][column].draw_block()

    @staticmethod
    def generate_mines(row, col):
        """
        Creates mines for the grid. This will not create any mines within 
        8 spaces of where the user clicked.
        """
        cell_clicked = (row, col)
        mines = random.sample(range(COLUMNS * ROWS), MINES + 8)
        
        # Decompose the integers into grid rows and columns
        mine_rows = [x // COLUMNS for x in mines]
        mine_cols = [x % COLUMNS for x in mines]
        mine_grid = zip(mine_rows, mine_cols)
        
        # Mines should not be generated in any block around the 
        # clicked block.
        invalid_zones = [(row + x, col + y) for x in range(-1, 2) 
            for y in range(-1, 2)]
        
        # Remove mines that were generated in the invalid zone
        invalid_mines = list(set(invalid_zones) & set(mine_grid))
        mines = list(set(mines) - set(invalid_mines))
        
        # Since we made extra mines just in case, only return the number 
        # of mines we need.
        return mines[0:MINES]
