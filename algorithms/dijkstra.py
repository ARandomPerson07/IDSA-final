import pygame
from typing import List
from queue import PriorityQueue
from components.node import Node
import time


def algorithm(draw, grid: List[List[Node]], start, end):
    start_time = time.time()
    print("Executing Djikstra's Algorithm")
    # step 1 : initialise neighbours is already done
    # step 2 : we use a priority queue to track the next node to traverse
    pq = PriorityQueue()
    visited = set()
    dists = {node: float('inf') for row in grid for node in row}
    dists[start] = 0
    previous = {}
    pq.put((0, start))  # (dist, node)
    path_found = False

    # pathfinding loop
    while not pq.empty() and not path_found:
        # quit should always take priority
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = pq.get()
        visited.add(current_node)
        # print("added to visited")

        # check if end has been found
        if current_node == end:
            path_found = True
            end_time = time.time()
            break

        # iterate over neighbours
        for neighbour in current_node.neighbours:
            # print("current node distance", dists[current_node])
            # print("neighbour distance", dists[neighbour])
            if dists[current_node] + 1 < dists[neighbour]:
                dists[neighbour] = dists[current_node] + \
                    1  # all distances are 1
                previous[neighbour] = current_node

                # add to prio queue
                if neighbour not in visited:
                    # print("this neighbour has not been visited, adding")
                    pq.put((dists[neighbour], neighbour))
                    if not neighbour == end:
                        neighbour.make_open()

        # call draw to update the grid
        draw()

        if not current_node == start and not current_node == end:
            current_node.make_closed()

    if path_found:
        print("Path found")
        path_len = 1
        path_current = previous[current_node]
        while path_current != start:
            path_current.make_path()
            path_len += 1
            path_current = previous[path_current]
            time.sleep(0.002)
            draw()
        return True, path_len, end_time - start_time, len(visited)
    else:
        end_time = time.time()
        print("No Path Found")
        return False, -1, end_time - start_time, len(visited)
