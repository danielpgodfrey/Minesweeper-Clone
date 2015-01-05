# File locations of images.
FLAG_LOCATION = 'flag.png'

# Size of the blocks, and the margin between them.
GRID_WIDTH = 20
GRID_HEIGHT = 20
MARGIN = 5

# How many rows and columns of blocks to create.
ROWS = 10
COLUMNS = 10

# Screen resolution
SCREEN_HEIGHT = ROWS * (GRID_HEIGHT + MARGIN) + MARGIN
SCREEN_WIDTH = COLUMNS * (GRID_WIDTH + MARGIN) + MARGIN

# Number of mines to place on the grid
# This should check if this is a certain percentage
# of total blocks.
MINES = 10

NON_MINES = ROWS * COLUMNS - MINES

assert(NON_MINES > 0)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
DARKGREEN= (   0, 100,   0)
GREEN    = (   0, 255,   0)
LITEGREEN= ( 144, 238, 144)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
CYAN     = (   0, 255, 255)
PURPLE   = ( 128,   0, 128)
PINK     = ( 255, 130, 171)
YELLOW   = ( 255, 255,   0)
ORANGE   = ( 255, 165,   0)

# Misc
# Milliseconds to wait between clicks
CLICK_WAIT = 100 
