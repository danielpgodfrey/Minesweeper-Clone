from constants import *


class Block:
    BLOCK_COLORS = {'MINE': RED,
                       0: DARKGRAY, 
                       1: LITEBLUE, 
                       2: GREEN,
                       3: RED,
                       4: DARKBLUE,
                       5: BROWN,
                       6: CYAN,
                       7: GRAY,
                       8: ORANGE }
           
    # Size of the blocks, and the margin between them.
    BLOCK_WIDTH = 20
    BLOCK_HEIGHT = 20
    MARGIN = 5
    
    def __init__(self, is_mine, mine_neighbors):
        self.is_mine = is_mine
        self.mine_neighbor_count = mine_neighbors
        self.flagged = False
        self.color = WHITE
        self.is_revealed = False
    
    def cycle_flag(self):
        self.flagged = not self.flagged

    def reveal(self):
        self.is_revealed = True
    
        if self.is_mine:
            self.color = self.BLOCK_COLORS["MINE"]
        else:
            self.color = self.BLOCK_COLORS[self.mine_neighbor_count]

    def draw_block(self, screen):
        if not self.flagged:
            block_rect = pygame.Rect(BLOCK_SIZE)
            screen.fill(self.color, block_rect)
        elif self.flagged:
            pass
            #TODO: Draw flags.
