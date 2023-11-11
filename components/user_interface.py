from components.colors import *


def get_hover_gridsquare(mouse_pos, rows, width):
    gap = width//rows
    y, x = mouse_pos

    row = y//gap
    col = x//gap

    return (row, col)
