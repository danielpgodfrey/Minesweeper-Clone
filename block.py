class Block:
    def __init__(self, is_mine, mine_neighbors, coordinates):
        self.is_mine = is_mine
        self.mine_neighbor_count = mine_neighbors
        self.flagged = False
        self.color = WHITE
        self.is_revealed = False
        self.coordinates = coordinates
    
    def cycle_flag(self):
        self.flagged = not self.flagged

    def reveal_block(self):
        self.is_revealed = True
    
        if self.is_mine:
            self.color = BLOCK_COLORS["MINE"]
        else:
            self.color = BLOCK_COLORS[self.mine_neighbor_count]

    def draw_block(self, screen):
        if not self.flagged:
            block_rect = pygame.Rect(BLOCK_SIZE)
            screen.fill(self.color, block_rect)
        elif self.flagged:
            pass
            #TODO: Draw flags.
       
