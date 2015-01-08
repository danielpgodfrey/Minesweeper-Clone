# File locations of images.
FLAG_LOCATION = 'flag.png'
MINE_LOCATION = 'mine.png'
RED_X_LOCATION = 'red_x.png'

DIFFICULTY = 'beginner'

# Size of the blocks, and the margin between them.
GRID_WIDTH = 20
GRID_HEIGHT = 20
MARGIN = 5

# How many rows and columns of blocks to create.
if DIFFICULTY == 'expert':
    ROWS = 16
    COLUMNS = 30
    MINES = 99
elif DIFFICULTY == 'intermediate':
    ROWS = 16
    COLUMNS = 16
    MINES = 40
elif DIFFICULTY == 'beginner':
    ROWS = 9
    COLUMNS = 9
    MINES = 10

# Screen resolution
INFO_HEIGHT = 75 # Height for display counters, time, etc.
SCREEN_HEIGHT = ROWS * (GRID_HEIGHT + MARGIN) + MARGIN + INFO_HEIGHT
SCREEN_WIDTH = COLUMNS * (GRID_WIDTH + MARGIN) + MARGIN

WORD_FONT_SIZE = int(ROWS * 1.2 - COLUMNS * .2)
NUMBER_FONT_SIZE = int(0.7 * GRID_WIDTH)

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
DARKBLUE = (   0,   0, 128)
CYAN     = (   0, 255, 255)
PURPLE   = ( 128,   0, 128)
PINK     = ( 255, 130, 171)
YELLOW   = ( 255, 255,   0)
ORANGE   = ( 255, 165,   0)
GRAY     = ( 175, 175, 175)
DARKGRAY = ( 75, 75, 75)
BROWN    = ( 165,  42,  42)
LITEBLUE = ( 118, 215, 234)

COLOR_DICT = {'MINE': RED,
                   0: DARKGRAY, 
                   1: LITEBLUE, 
                   2: GREEN,
                   3: RED,
                   4: DARKBLUE,
                   5: BROWN,
                   6: CYAN,
                   7: GRAY,
                   8: ORANGE }
# Misc
# Milliseconds to wait between clicks
CLICK_WAIT = 100 
