from block import Block

class Grid:
    def __init__(self, click_position):
        row, col = find_clicked_row_column(click_position)
        mines = generate_mines(row, col)
        mine_neighbors = calc_mine_neighbors(mines)
        self.blocks = [[Block(mines[x][y] for y in range(COLUMNS)] 
            for x in range(ROWS)]

    def update_grid(self, click_position, click_type):
        row, col = find_clicked_row_column(click_position)
        if click_type == "left":
            self.blocks[row][column].reveal_block()
            self.blocks[row][column].draw_block()
            if self.blocks[row][column].mine_neighbors == 0:
                self._reveal_around(row, column)
        
        elif click_type == "right":
            self.blocks[row][column].cycle_flag()
            self.blocks[row][column].draw_block()
