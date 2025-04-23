# 🧭 Implementação de Busca em Largura e Profundidade para Resolução de Labirintos

Este projeto foi desenvolvido como parte da disciplina de **Sistemas Inteligentes** da Universidade Federal de Santa Catarina (UFSC), utilizando **Python 3.12.3**. O programa gera labirintos onde o agente deve encontrar o caminho entre um ponto inicial e um objetivo utilizando diferentes algoritmos de busca. 

🧠 A execução deste se dá diretamente pela execução do arquivo solve.py e a iteração com a janela do labirinto!

## 🧱 Representação do Labirinto

- `1`: Caminho possível
- `0`: Parede (obstáculo)
- `2`: Início
- `3`: Objetivo

---

## 🛠️ Funções Desenvolvidas

- `generate_maze()`: Gera um labirinto válido por divisão recursiva.
- `get_neighbors()`: Retorna vizinhos possíveis (para escavação de caminhos).
- `carve_path()`: Escava os caminhos do labirinto.
- `is_solvable()`: Verifica se há caminho entre início e objetivo.
- `actions(state, maze_ref=None)`: Retorna ações válidas (cima, baixo, esquerda, direita).
- `find_start_and_goal(maze_ref)`: Localiza início e fim no labirinto.
- `heuristic(state, goal)`: Heurística de Manhattan.
- `bfs_step_by_step(start)`: Implementação da Busca em Largura (BFS).
- `dfs_step_by_step(start)`: Implementação da Busca em Profundidade (DFS).
- `a_star_step_by_step(start, goal)`: Implementação da Busca A*(Solução Ideal).
- `draw_maze()`, `update_loop()`, `setup()`: Interface gráfica com pygame.

---

## 📸 Exemplo de Saída

![image](https://github.com/user-attachments/assets/310235d3-795f-41b9-ad83-8736d5a78aaf)
![image](https://github.com/user-attachments/assets/05385558-8c51-4a72-9062-95f22e508b47)
![image](https://github.com/user-attachments/assets/ba55f54e-951c-4e48-8b14-c8c115478a24)

---

### Resultados Obtidos:

- **🔵 BFS**  
  Caminho encontrado:  
  `[(1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (8, 9)]`  
  Custo: `61`

- **🟠 DFS**  
  Caminho encontrado:  
  `[(1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (2, 8), (3, 8), (4, 8), (4, 9), (5, 9), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (4, 1), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 7), (9, 8), (9, 9), (8, 9)]`  
  Custo: `49`

- **⭐ A\***  
  Caminho encontrado:  
  `[(1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (8, 9)]`  
  Custo: `18`

---


## 📚 Proposição
https://www.galirows.com.br/meublog/blog/proposta-de-trabalho-metodos-de-busca-para-resolver-um-labirinto/

---

## 🚀 Código:
<details>
<summary>Clique para expandir o código completo</summary>

```python
import asyncio
import pygame
from collections import deque
import heapq
import random

# Configurações do labirinto
GRID_SIZE = 10
maze = [
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
CELL_SIZE = 50
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)

screen = None
path = []
visited_cells = []
start = None
goal = None
search_generator = None
current_algorithm = "A*" 
steps_counter = 0  

#Funções base do labirinto
def get_neighbors(row, col, maze_temp):
    neighbors = []
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    random.shuffle(directions)
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and maze_temp[new_row][new_col] == 0:
            neighbors.append((new_row, new_col))
    return neighbors

def carve_path(row, col, maze_temp):
    maze_temp[row][col] = 1
    for new_row, new_col in get_neighbors(row, col, maze_temp):
        if maze_temp[new_row][new_col] == 0:
            maze_temp[row + (new_row - row) // 2][col + (new_col - col) // 2] = 1
            carve_path(new_row, new_col, maze_temp)

def is_solvable(maze_temp, start, goal):
    frontier = deque([(start, [start])])
    visited = set([start])
    while frontier:
        state, _ = frontier.popleft()
        if state == goal:
            return True
        for next_state in actions(state, maze_temp):
            if next_state not in visited:
                visited.add(next_state)
                frontier.append((next_state, []))
    return False

def actions(state, maze_ref=None):
    if maze_ref is None:
        maze_ref = maze
    row, col = state
    possible_actions = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and maze_ref[new_row][new_col] != 0:
            possible_actions.append((new_row, new_col))
    return possible_actions

def find_start_and_goal(maze_ref):
    start = goal = None
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if maze_ref[i][j] == 2:
                start = (i, j)
            elif maze_ref[i][j] == 3:
                goal = (i, j)
    return start, goal

def is_goal(state):
    row, col = state
    return maze[row][col] == 3

def heuristic(state, goal):
    row, col = state
    goal_row, goal_col = goal
    return abs(row - goal_row) + abs(col - goal_col)

####Funções de Busca####

#Busca em Largura (BFS)
def bfs_step_by_step(start):
    global steps_counter
    steps_counter = 0
    try:
        frontier = deque([(start, [start])])
        visited = set([start])
        
        while frontier:
            state, path = frontier.popleft()
            yield state, path, visited
            steps_counter += 1
            
            if is_goal(state):
                print("\n\n", path)
                return path
            
            for next_state in actions(state):
                if next_state not in visited:
                    visited.add(next_state)
                    frontier.append((next_state, path + [next_state]))

        return None
    except Exception as e:
        print(f"Erro na BFS: {e}")
        return None

#Busca em Profundidade (DFS)
def dfs_step_by_step(start):
    global steps_counter
    steps_counter = 0
    
    try:
        frontier = [(start, [start])]
        visited = set([start])
        
        while frontier:
            state, path = frontier.pop()
            yield state, path, visited
            steps_counter += 1
            
            if is_goal(state):
                print("\n\n", path)
                return path 
            
            for next_state in actions(state):
                if next_state not in visited:
                    visited.add(next_state)
                    frontier.append((next_state, path + [next_state]))

        return None
    except Exception as e:
        print(f"Erro na DFS: {e}")
        return None

def a_star_step_by_step(start, goal):
    global steps_counter
    steps_counter = 0
    frontier = [(0, start, [start])]
    visited = set()
    g_score = {start: 0}
    while frontier:
        f_score, state, path = heapq.heappop(frontier)
        yield state, path, visited
        steps_counter += 1 
        if is_goal(state):
            print("\n\n", path)
            return
        if state in visited:
            continue
        visited.add(state)
        for next_state in actions(state):
            new_g = g_score[state] + 1
            if next_state not in g_score or new_g < g_score[next_state]:
                g_score[next_state] = new_g
                f = new_g + heuristic(next_state, goal)
                heapq.heappush(frontier, (f, next_state, path + [next_state]))
        
###Labirinto e Interface Gráfica###

def setup():
    global screen, path, visited_cells, start, goal, search_generator, steps_counter
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 60))
    pygame.display.set_caption("Busca em Labirinto")
    generate_new_maze()

first_maze_generated = False  

def generate_new_maze():
    global maze, start, goal, path, visited_cells, search_generator, steps_counter, first_maze_generated

    if not first_maze_generated:
        first_maze_generated = True
        start, goal = find_start_and_goal(maze)
    else:
        while True:
            maze_temp = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            start_row = random.randrange(1, GRID_SIZE, 2)
            start_col = random.randrange(1, GRID_SIZE, 2)
            carve_path(start_row, start_col, maze_temp)

            empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if maze_temp[i][j] == 1]
            if len(empty_cells) < 2:
                continue

            start, goal = random.sample(empty_cells, 2)
            maze_temp[start[0]][start[1]] = 2
            maze_temp[goal[0]][goal[1]] = 3

            if is_solvable(maze_temp, start, goal):
                maze = maze_temp
                break

    path = []
    visited_cells = []
    steps_counter = 0
    search_generator = get_algorithm_generator(current_algorithm)

def get_algorithm_generator(algo):
    if algo == "BFS":
        return bfs_step_by_step(start)
    elif algo == "DFS":
        return dfs_step_by_step(start)
    else:
        return a_star_step_by_step(start, goal)

def draw_button(text, x, y, w, h, active=False):
    color = (180, 180, 250) if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont(None, 24)
    txt = font.render(text, True, BLACK)
    txt_rect = txt.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(txt, txt_rect)

def draw_maze():
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE
            if maze[i][j] == 0:
                color = BLACK
            elif maze[i][j] == 2:
                color = GREEN
            elif maze[i][j] == 3:
                color = RED
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for row, col in visited_cells:
        if maze[row][col] not in [2, 3]:
            pygame.draw.rect(screen, ORANGE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for row, col in path:
        if maze[row][col] not in [2, 3]:
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))

    draw_button("Novo Labirinto", 10, WINDOW_SIZE + 10, 140, 40)
    draw_button("BFS", 160, WINDOW_SIZE + 10, 60, 40, current_algorithm == "BFS")
    draw_button("DFS", 230, WINDOW_SIZE + 10, 60, 40, current_algorithm == "DFS")
    draw_button("A*", 300, WINDOW_SIZE + 10, 60, 40, current_algorithm == "A*")

    font = pygame.font.SysFont(None, 24)
    steps_text = font.render(f"Passos: {steps_counter}", True, BLACK)
    screen.blit(steps_text, (WINDOW_SIZE - 100, WINDOW_SIZE + 15))

    pygame.display.flip()

def update_loop():
    global path, visited_cells, search_generator, current_algorithm
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y > WINDOW_SIZE:
                if 10 <= x <= 150:
                    generate_new_maze()
                elif 160 <= x <= 220:
                    current_algorithm = "BFS"
                    search_generator = get_algorithm_generator(current_algorithm)
                    path = []
                    visited_cells = []
                    steps_counter = 0  
                elif 230 <= x <= 290:
                    current_algorithm = "DFS"
                    search_generator = get_algorithm_generator(current_algorithm)
                    path = []
                    visited_cells = []
                    steps_counter = 0  
                elif 300 <= x <= 360:
                    current_algorithm = "A*"
                    search_generator = get_algorithm_generator(current_algorithm)
                    path = []
                    visited_cells = []
                    steps_counter = 0  

    try:
        state, path_so_far, visited = next(search_generator)
        visited_cells = list(visited)
        path[:] = path_so_far
    except StopIteration:
        pass

    draw_maze()
    return True

async def main():
    setup()
    while update_loop():
        await asyncio.sleep(1.0 / FPS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pygame.quit()


```
