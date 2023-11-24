# Pathfinding Algorithm Visualizer

## Description of Algorithms Implemented

Two algorithms were implemented for this project: Dijkstra's algorithm and A*algorithm. Both algorithms are used to find the shortest path between two nodes in a graph. The difference between the two algorithms is that A* uses a heuristic function to estimate the distance between the current node and the end node, while Dijkstra's algorithm does not. This means that A* is more efficient than Dijkstra's algorithm, but it is not guaranteed to find the shortest path.

A* is guaranteed to find the shortest path if the heuristic function is "admissible", i.e. it never overestimates the distance between the current node and the end node. In this project, the heuristic function used is the Manhattan distance, which is the sum of the absolute values of the differences in the x and y coordinates of the current node and the end node. This heuristic function is admissible because the shortest distance between two points is a straight line, and the Manhattan distance is always less than or equal to the straight line distance.

## Code Structure

To preserve modularity and readability, the code was split into multiple files.

- The main file is ```main.py```, which contains the main loop of the program. It is responsible for creating the grid, accepting user input, and calling the pathfinding algorithms.
- The ```algorithms``` folder contains the ```dijkstra.py``` and ```astar.py``` files, which contain the implementations of Dijkstra's algorithm and A* algorithm respectively. These algorithms are implemented as functions that take in a "draw" function, a grid and the start and end nodes as parameters, and return the path as a list of nodes. The "draw" function is a function dynamically declared with the target window and the internal grid matrix in the main loop that is called after every node traversal, and is used to update the display.  This allows the algorithm to be visualized in real time.
- The ```grid.py``` file contains the ```Grid``` class, which is responsible for drawing the grid and initializing the internal representation of the grid, which is a 2D array of ```Node``` objects.
- The ```node.py``` file contains the ```Node``` class, which represents a single node in the grid. It also provides abstractions for drawing the node and changing its state.
- The ```colors.py``` file contains the colors used in the program, providing abstractions for colours to avoid handling messy RGB values.
- The ```user_interface.py``` file contains the custom classes for text and buttons, which are used to display text and buttons on the screen. These classes are used to create the user interface for the program.

## Encountered Issues or Challenges

The main issue encountered in this project was the usage of the unfamiliar Pygame library. Coming from a more visual interface editor like Godot, it was difficult to understand how to use Pygame to draw elements on screen. However, after watching the tutorial videos and reading the documentation, it was relatively straightforward, if not a little obtuse with having to implement my own basic classes like text and buttons.

## Instructions on code execution

In a terminal environment with Python 3 installed and the pygame library installed, simply do ```python3 main.py```. The program will then run and the user can interact with the program.

In addition, running ```python3 main.py <size>``` allows the user to specify the size of the grid. For example, ```python3 main.py 50``` will create a grid of size 50x50. The default size is 20x20.

## Additional Features Implemented

In addition to the basic features laid out in the requirements, I also implemented the following features:

- The user can choose between Dijkstra's algorithm and A* algorithm at any time during the program except when the pathfinding algorithm is running, and not just during the initial setup.

- The user can either choose to clear the path without clearing the barriers, or clear both the path and the barriers.

- Runtime statistics are displayed at the end of the pathfinding algorithm, including the time taken to traverse, the number of nodes traversed, and the total distance of the path.

## Group Members

- Chan, Adam Christopher Yamson A0242453L
