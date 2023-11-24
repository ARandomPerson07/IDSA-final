from typing import List
import sys

import pygame

from components.node import Node
from components.grid import *
from components.user_interface import *
from algorithms.a_star import algorithm as a_star_algo
from algorithms.dijkstra import algorithm as djikstra_algo
# initialize stuff
WIDTH = 750
SIDEBAR_WIDTH = 200
WIN = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, WIDTH))
pygame.display.set_caption("Final Project Pathfinding Visualiser")


def show_grid(grid: List[List[Node]]):
    for row in grid:
        print([color_map[cell.color] for cell in row])


def draw(win, grid: List[List[Node]], rows, width, *misc_ui):
    # might be worth making it so that this never reruns if the grid is already drawn
    win.fill(BLACK)

    for row in grid:
        for node in row:
            # asks each node in the grid to draw itself with the appropriate colour
            node.draw(win)

    draw_grid(win, rows, width)

    for ui_element in misc_ui:  # ensure each ui element has a .draw method or else this will fail
        ui_element.draw(win)
    pygame.display.update()


def main(win, width, rows=20):
    ROWS = rows
    grid = make_grid(ROWS, width)
    # win.fill(WHITE)
    # draw_grid(win, ROWS, width)
    # pygame.display.update()

    # algorithm selector
    algo_toggle = ToggleButton(
        WIDTH + 20, 200, 170, 75, "A*", "Djikstra", False)
    # info box
    header = TextBox(WIDTH + 20, 10, 170, 100,
                     "Left-click to place Start/End/Barrier Nodes.\n\nRight-click to erase Nodes.")
    header2 = TextBox(WIDTH + 20, 130, 170, 60,
                      "Click below to toggle the algorithm used.")
    header3 = TextBox(WIDTH + 20, 290, 170, 110,
                      "Space = start\n\nBackspace = clear algorithm output\n\nEscape = clear all")

    # results boxes
    runtime = 0.0
    path_len = 0
    space = 0
    algorithm_stats = TextBox(WIDTH + 20, 420, 170, 300,
                              f"Results will show up here\n\nLast Runtime: {runtime}s\n\nPath Length: {path_len} Steps\n\nTraversed Nodes:{space}")

    # Node inits
    start = None
    end = None

    # Control flags
    run = True
    started = False

    # main loop
    while run:
        draw(win, grid, ROWS, width, algo_toggle,
             header, header2, header3, algorithm_stats)
        # algo_toggle.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # mouse input processing
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
                    elif algo_toggle.rect.collidepoint(pos):
                        algo_toggle.change_state()

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
                # start logic
                if event.key == pygame.K_SPACE and not started and start and end:
                    started = True
                    # show_grid(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    if algo_toggle.get_state():
                        result, path_len, runtime, space = djikstra_algo(lambda: draw(win, grid, ROWS, width, algo_toggle, header, header2, header3, algorithm_stats),
                                                                         grid, start, end)
                    else:
                        result, path_len, runtime, space = a_star_algo(lambda: draw(win, grid, ROWS, width, algo_toggle, header, header2, header3, algorithm_stats),
                                                                       grid, start, end)

                    algorithm_stats.set_text(
                        f"Results will show up here\n\nLast Runtime: {runtime:.4f}s\n\nPath Length: {path_len} Steps\n\nTraversed Nodes: {space}")
                    draw(win, grid, ROWS, width, algo_toggle,
                         header, header2, header3)

                # soft clear
                if event.key == pygame.K_BACKSPACE:
                    started = False
                    print("Clearing results")
                    for row in grid:
                        for node in row:
                            if not ((node.is_barrier() or node.is_start()) or node.is_end()):
                                node.reset()

                # hard clear
                if event.key == pygame.K_ESCAPE:
                    started = False
                    for row in grid:
                        for node in row:
                            node.reset()
                            start = None
                            end = None
    pygame.quit()


# allow user to set custom dimensions
if len(sys.argv) > 1:
    main(WIN, WIDTH, int(sys.argv[1]))
else:
    main(WIN, WIDTH)
