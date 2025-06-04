# 🗺️ Maze Solver Visualization 🧩

This project provides a visual demonstration of popular pathfinding algorithms navigating through mazes. Watch Breadth-First Search (BFS), Depth-First Search (DFS), and A* (A-star) in action as they find the shortest path from a start to an end point in a dynamically generated or predefined maze!

## ✨ Features

* **Visual Maze Representation:** Displays the maze grid, walls, open paths, start (🟢), and goal (🔴) points.
* **Algorithm Visualization:**
    * See visited cells (🟧) as the algorithm explores.
    * Watch the final path (👣/🟦) being drawn.
* **Multiple Algorithms:** Choose between:
    * 🍞 Breadth-First Search (BFS)
    * 🌲 Depth-First Search (DFS)
    * ⭐ A* Search (using Manhattan distance heuristic)
* **Dynamic Maze Generation:**
    * Starts with a predefined maze.
    * Generate new, random, solvable mazes with a click (🆕).
* **Interactive Controls:**
    * Buttons to select algorithms.
    * Button to generate a new maze.
* **Step Counter:** Track the number of steps (🔢) each algorithm takes to find the solution or explore.
* **Step-by-Step Animation:** Clearly visualizes the decision-making process of each algorithm, making it a great educational tool.

## 📸 Demo 

**Example placeholder:**
![Solve Demo](https://github.com/user-attachments/assets/3babf8c5-4717-470d-9a31-3a7d1264ea06)


## 🛠️ Technologies Used

* **Python 3.12** (🐍)
* **Pygame** (🎮): For graphics, event handling, and the main game loop.
* **Asyncio** (⏳): For managing the asynchronous main loop, allowing for smooth step-by-step visualization.
* Standard Python libraries: `collections.deque`, `heapq`, `random`.

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/JvFg92/Maze_Solver
    cd Maze_Solver
    ```
    
2.  **Install dependencies** (Pygame is the main external library):
    ```bash
    pip install pygame
    ```
    (If you don't have `pip`, ensure you have Python installed and look up how to install pip for your system.)

## ▶️ How to Run

Once Pygame is installed, navigate to the directory containing `solve.py` and run:
```bash
python solve.py
