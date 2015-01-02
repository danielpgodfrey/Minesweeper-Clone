import pygame
import random
from constants import *


def initialize():
    """
    Do initial window and pygame management.
    """
    pygame.init()
    pygame.display.set_caption("Minesweeper PRE-ALPHA")


def get_screen():
    """
    Create and return the screen object.
    """
    size = (SCREEN_HEIGHT, SCREEN_WIDTH)
    screen = pygame.display.set_mode(size)

    return screen


def generate_mine_grid():
    """
    Generate a double list of points. Each point with a value
    of 1 should have a mine in it, and every other one should
    have a value of 0.
    """
    mine_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
    total_mines = 0

   # Generate mines randomly.
    for rows in range(ROWS):
        while total_mines < MINES:
            row = random.randrange(0, ROWS)
            column = random.randrange(0, COLUMNS)
            if mine_grid[row][column] == 0:
                mine_grid[row][column] = 1
                total_mines += 1

    return mine_grid


def reveal_neighbors(row, column, clicked_grid):
    """
    Reveal neighbors of input block. Treat them as though they were clicked.
    """
    # Check whether the block is on an edge or not
    left = row >= 1
    right = row < ROWS - 1
    up = column >= 1
    down = column < COLUMNS - 1

    if right:
        clicked_grid[row + 1][column] = 1
    if up:
        clicked_grid[row][column - 1] = 1
    if down:
        clicked_grid[row][column + 1] = 1
    if left:
        clicked_grid[row - 1][column] = 1


def get_block_color(row, column, clicked_grid):
    """
    Return the color of the block based on the amount of blocks
    beside or diagonal to it that contain mines.

    This code will also call reveal_neighbors appropriately (FIX THIS).
    """
    mine_count = count_mine_neighbors(row, column, mine_grid)
    if clicked_grid[row][column] == 0:
        grid_color = WHITE
    elif mine_grid[row][column] == 1:
        grid_color = RED
    elif mine_count == 0:
        grid_color = BLUE
        reveal_neighbors(row, column, clicked_grid)
    elif mine_count == 1:
        grid_color = CYAN
    elif mine_count == 2:
        grid_color = DARKGREEN
    elif mine_count == 3:
        grid_color = GREEN
    elif mine_count == 4:
        grid_color = LITEGREEN
    elif mine_count == 5:
        grid_color = PURPLE
    elif mine_count == 6:
        grid_color = PINK
    elif mine_count == 7:
        grid_color = YELLOW
    elif mine_count == 8:
        grid_color = ORANGE

    return grid_color


def draw_grid(clicked_grid, mine_grid, screen):
    """
    Draw the grid for the game. Update the screen with appropriate
    colorings.
    """
    for column in range(0, COLUMNS):
        for row in range(0, ROWS):
            block_color = get_block_color(row, column, clicked_grid)

            pygame.draw.rect(screen, block_color,
                            (column * GRID_WIDTH + (column + 1) * MARGIN,
                             row * GRID_HEIGHT + (row + 1) * MARGIN,
                             GRID_WIDTH,
                             GRID_HEIGHT))


def main_loop():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game when the user clicks close.
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                Controls.mouse_down(clicked_grid)

        draw_grid(clicked_grid, mine_grid, screen)

        # Update the screen with what is drawn.
        pygame.display.flip()
        clock.tick(60)


def count_mine_neighbors(row, column, mine_grid):
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


class Controls:

    def mouse_down(clicked_grid):
        """
        Update the clicked_grid list when the user clicks a grid
        """

        pos = pygame.mouse.get_pos()

        # Find the row and column the user clicked on.
        col_clicked = pos[0] // (GRID_WIDTH + MARGIN)
        row_clicked = pos[1] // (GRID_HEIGHT + MARGIN)

        # If the user clicks below the final row, count it as the final row.
        if row_clicked >= ROWS:
            row_clicked = ROWS - 1
        if col_clicked >= COLUMNS:
            col_clicked = COLUMNS - 1

        clicked_grid[row_clicked][col_clicked] = 1

if __name__ == "__main__":
    initialize()

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    screen = get_screen()

    # Holds rows that have been clicked
    clicked_grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

    # Holds location of the mines
    mine_grid = generate_mine_grid()

    # Loop until the user clicks the close button.
    done = False
    main_loop()

    # Clean up
    pygame.quit()
