import pygame
from components.node import Node
from components.colors import *


def make_grid(rows, width):
    gap = width//rows
    return [[Node(row, col, gap, rows) for col in range(rows)] for row in range(rows)]


def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):  # horizontal lines
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for i in range(rows):  # vertical lines
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))
    # draw the last vertical line that separates the menu from the play field
    pygame.draw.line(win, GREY, (width, 0), (width, width))
