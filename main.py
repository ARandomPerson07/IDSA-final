from typing import List

import pygame

from components.node import Node
from components.grid import *
from components.user_interface import *
from algorithms.a_star import algorithm as a_star_algo

# initialize stuff
WIDTH = 800
SIDEBAR_WIDTH = 200
WIN = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, WIDTH))
pygame.display.set_caption("Final Project Pathfinding Visualiser")

algorithm = a_star_algo

# draw function


def show_grid(grid: List[List[Node]]):
    for row in grid:
        print([color_map[cell.color] for cell in row])


def draw(win, grid: List[List[Node]], rows, width):
    # might be worth making it so that this never reruns if the grid is already drawn
    win.fill(WHITE)

    for row in grid:
        for node in row:
            # asks each node in the grid to draw itself with the appropriate colour
            node.draw(win)

    draw_grid(win, rows, width)

    pygame.display.update()


def main(win, width):
    ROWS = 25
    grid = make_grid(ROWS, width)
    # win.fill(WHITE)
    # draw_grid(win, ROWS, width)
    # pygame.display.update()
    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not started:
                if pygame.mouse.get_pressed()[0]:  # left click
                    pos = pygame.mouse.get_pos()
                    if pos[0] <= WIDTH:
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
                    if pos[0] <= WIDTH:
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
                    show_grid(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                if event.key == pygame.K_BACKSPACE:
                    started = False
                    print("Clearing results")
                    for row in grid:
                        for node in row:
                            if not ((node.is_barrier() or node.is_start()) or node.is_end()):
                                node.reset()

    pygame.quit()


main(WIN, 800)
