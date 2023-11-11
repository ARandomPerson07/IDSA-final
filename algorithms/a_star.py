# TODO: Implement A* algorithm

# Hint: You must be able to reconstruct the path once the algorithm has finished
# Hint: You must be able to visualize the algorithm in action i.e call the methods to draw on the screen to visualize the algorithm in action in the astar function

import pygame
from queue import PriorityQueue
from typing import List
from components.node import Node
from components.colors import *
import time


def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# orange is start, turquoise is end, red is closed, green is open, black is barrier


def algorithm(draw, grid, start, end):
    # print("algo running")
    start_time = time.time()
    count = 0
    opens = PriorityQueue()
    opens.put((0, count, start))
    came_from = {}
    path_found = False
    # track space complexity
    visited_count = 0

    # init g_score and f_score arrays
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    opens_hash = {start}  # tracks which nodes have been visited
    while not opens.empty() and not path_found:
        visited_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get the node at the queue head from the triple at the queue head
        current: Node = opens.get()[2]
        opens_hash.remove(current)

        if current == end:
            path_found = True
            end_time = time.time()
            break
        # print("number of neighbours of node is ", len(current.neighbours))
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
                    if not neighbour == end:
                        neighbour.make_open()
        draw()

        if current != start:
            current.make_closed()

    if path_found:
        # backtrack and visualise path
        path_len = 1
        path_current: Node = came_from[end]
        while path_current != start:
            path_current.make_path()
            time.sleep(0.002)
            path_current = came_from[path_current]
            path_len += 1
            draw()
        return True, path_len, end_time - start_time, visited_count
    else:
        end_time = time.time()
        print("Path not found")
        return False, -1, end_time - start_time, visited_count
