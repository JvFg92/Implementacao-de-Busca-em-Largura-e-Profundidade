import asyncio
import platform
import pygame
from collections import deque
import heapq

# Definição do labirinto (matriz 10x10 corrigida)
maze = [
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # Corrigido: adicionado 0
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Configurações da janela para Pygame
CELL_SIZE = 50
GRID_SIZE = 10
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Encontra o estado inicial e objetivo
def find_start_and_goal(maze):
    start = goal = None
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                start = (i, j)
            if maze[i][j] == 3:
                goal = (i, j)
    return start, goal

# Função de ações possíveis
def actions(state):
    row, col = state
    possible_actions = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esq, dir
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != 0:
            possible_actions.append((new_row, new_col))
    return possible_actions

# Teste de objetivo
def is_goal(state):
    row, col = state
    return maze[row][col] == 3

# Custo de passo
def step_cost(state, action, next_state):
    return 1

# Custo de caminho
def path_cost(path):
    return len(path) - 1

# Heurística para A* (distância de Manhattan)
def heuristic(state, goal):
    row, col = state
    goal_row, goal_col = goal
    return abs(row - goal_row) + abs(col - goal_col)

# Busca em Largura (BFS)
def bfs(start):
    frontier = deque([(start, [start])])
    visited = set([start])
    
    while frontier:
        state, path = frontier.popleft()
        
        if is_goal(state):
            return path
        
        for next_state in actions(state):
            if next_state not in visited:
                visited.add(next_state)
                frontier.append((next_state, path + [next_state]))
    
    return None

# Busca em Profundidade (DFS)
def dfs(start):
    frontier = [(start, [start])]
    visited = set([start])
    
    while frontier:
        state, path = frontier.pop()
        
        if is_goal(state):
            return path
        
        for next_state in actions(state):
            if next_state not in visited:
                visited.add(next_state)
                frontier.append((next_state, path + [next_state]))
    
    return None

# Busca A*
def a_star(start, goal):
    frontier = [(0, start, [start])]  # (f_score, estado, caminho)
    visited = set()
    g_score = {start: 0}
    
    while frontier:
        f_score, state, path = heapq.heappop(frontier)
        
        if is_goal(state):
            return path
        
        if state in visited:
            continue
        
        visited.add(state)
        
        for next_state in actions(state):
            if next_state not in visited:
                new_g_score = g_score[state] + step_cost(state, None, next_state)
                if next_state not in g_score or new_g_score < g_score[next_state]:
                    g_score[next_state] = new_g_score
                    f_score = new_g_score + heuristic(next_state, goal)
                    heapq.heappush(frontier, (f_score, next_state, path + [next_state]))
    
    return None

# Função para exibir o labirinto com o caminho (textual)
def print_maze_with_path(maze, path):
    maze_copy = [row[:] for row in maze]
    for row, col in path:
        if maze[row][col] not in [2, 3]:
            maze_copy[row][col] = '*'
    
    for row in maze_copy:
        print(' '.join(str(cell) for cell in row))

# Parte textual: executa BFS, DFS e A*
def run_textual_solvers():
    start, goal = find_start_and_goal(maze)
    
    print("Labirinto inicial:")
    for row in maze:
        print(' '.join(str(cell) for cell in row))
    
    print("\nBusca em Largura (BFS):")
    bfs_path = bfs(start)
    if bfs_path:
        print("Caminho encontrado:", bfs_path)
        print("Custo do caminho:", path_cost(bfs_path))
        print("Labirinto com caminho:")
        print_maze_with_path(maze, bfs_path)
    else:
        print("Nenhum caminho encontrado.")
    
    print("\nBusca em Profundidade (DFS):")
    dfs_path = dfs(start)
    if dfs_path:
        print("Caminho encontrado:", dfs_path)
        print("Custo do caminho:", path_cost(dfs_path))
        print("Labirinto com caminho:")
        print_maze_with_path(maze, dfs_path)
    else:
        print("Nenhum caminho encontrado.")
    
    print("\nBusca A*:")
    a_star_path = a_star(start, goal)
    if a_star_path:
        print("Caminho encontrado:", a_star_path)
        print("Custo do caminho:", path_cost(a_star_path))
        print("Labirinto com caminho:")
        print_maze_with_path(maze, a_star_path)
    else:
        print("Nenhum caminho encontrado.")
    
    return a_star_path  # Retorna o caminho do A* para a parte gráfica

# Inicialização do Pygame
def setup():
    global screen, path
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Labirinto")
    screen.fill(WHITE)
    
    # Executa solvers textuais e obtém o caminho do A*
    path = run_textual_solvers() or []

# Desenha o labirinto e o caminho
def draw_maze():
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
    
    # Desenha o caminho
    for row, col in path:
        if maze[row][col] not in [2, 3]:
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Desenha a grade
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))
    
    pygame.display.flip()

# Loop de atualização
def update_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
    draw_maze()

# Loop principal
async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

# Executa o programa
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())