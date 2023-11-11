import pygame
from components.node import Node
from components.colors import *
import time


def make_grid(rows, width):
    gap = width//rows
    return [[Node(row, col, gap, rows) for col in range(rows)] for row in range(rows)]


def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):  # horizontal lines
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for i in range(rows):  # vertical lines
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


win = pygame.display.set_mode((800, 800))

grid = make_grid(50, 800)

draw_grid(win, 50, 800)
pygame.display.update()
time.sleep(5)
