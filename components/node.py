import pygame
from components.colors import *


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width  # xy determines the position of the Node on screen
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.total_row = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        has_above = self.row > 0
        has_below = (self.row + 1) < len(grid)
        has_left = self.col > 0
        has_right = (self.col + 1) < len(grid[0])
        if has_above:
            above: Node = grid[self.row - 1][self.col]
            if not above.is_barrier():
                self.neighbours.append(above)
        if has_below:
            below: Node = grid[self.row + 1][self.col]
            if not below.is_barrier():
                self.neighbours.append(below)
        if has_left:
            left: Node = grid[self.row][self.col - 1]
            if not left.is_barrier():
                self.neighbours.append(left)
        if has_right:
            right: Node = grid[self.row][self.col + 1]
            if not right.is_barrier():
                self.neighbours.append(right)

    def __lt__(self, other):
        return False
