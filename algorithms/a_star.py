# TODO: Implement A* algorithm

# Hint: You must be able to reconstruct the path once the algorithm has finished
# Hint: You must be able to visualize the algorithm in action i.e call the methods to draw on the screen to visualize the algorithm in action in the astar function

import pygame
import math
from queue import PriorityQueue
from typing import List

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


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
        #print("I now have", len(self.neighbours), "neighbours")


def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def algorithm(draw, grid, start, end):
    #print("algo running")
    count = 0
    opens = PriorityQueue()
    opens.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    opens_hash = {start}  # tracks which nodes have been visited
    while not opens.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get the node at the queue head from the triple at the queue head
        current: Node = opens.get()[2]
        opens_hash.remove(current)

        if current == end:
            #print("found path")
            return True
        #print("number of neighbours of node is ", len(current.neighbours))
        for neighbour in current.neighbours:
            g_temp = g_score[current] + 1  # all distances are 1

            if g_temp < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = g_temp
                f_score[neighbour] = g_temp + \
                    heuristic(neighbour.get_pos(), end.get_pos())

                if neighbour not in opens_hash:
                    count += 1
                    opens.put((f_score[neighbour], count, neighbour))
                    opens_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            current.make_closed()
    print("no path found")
    return False


def _make_grid(rows, width):
    gap = width//rows
    return [[Node(row, col, gap, rows) for col in range(rows)] for row in range(rows)]


def _draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):  # horizontal lines
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for i in range(rows):  # vertical lines
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw(win, grid: List[List[Node]], rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    _draw_grid(win, rows, width)
    pygame.display.update()


def get_hover_gridsquare(mouse_pos, rows, width):
    gap = width//rows
    y, x = mouse_pos

    row = y//gap
    col = x//gap

    return (row, col)


def main(win, width):
    ROWS = 50
    grid = _make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                row, col = get_hover_gridsquare(pos, ROWS, width)
                node = grid[row][col]

                if not start and not node.is_end():
                    start = node
                    node.make_start()

                elif not end and not node.is_start():
                    end = node
                    node.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                row, col = get_hover_gridsquare(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    #print("game start")
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

    pygame.quit()


main(WIN, WIDTH)
