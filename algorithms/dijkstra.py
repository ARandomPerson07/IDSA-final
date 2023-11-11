import pygame
from typing import List
from queue import PriorityQueue
from components.node import Node
#the algorithm's job is to take in a draw function, a grid, a start, and an end, and find the shortest path via backtracking
#it is also in charge of changing the states of each node in the grid

def algorithm(draw, grid : List[List[Node]], start, end):
    #step 1 : initialise neighbours is already done
    #step 2 : we use a priority queue to track the next node to traverse