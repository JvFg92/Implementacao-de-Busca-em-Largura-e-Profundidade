import asyncio
import platform
import pygame
from collections import deque
import heapq
import random

#Configurações do labirinto
GRID_SIZE = 10
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

#Configurações da janela para Pygame
CELL_SIZE = 50
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Função para gerar labirinto solucionável usando Recursive Backtracking
def generate_maze():
    global maze
    def get_neighbors(row, col, maze_temp):
        neighbors = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  #Cima, baixo, esq, dir
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
                #Abre o caminho entre as células
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

    while True:
        #Inicializa a matriz com paredes
        maze_temp = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        #Escolhe uma posição inicial aleatória (coordenadas ímpares para alinhar com o algoritmo)
        start_row = random.randrange(1, GRID_SIZE, 2)
        start_col = random.randrange(1, GRID_SIZE, 2)
        start = (start_row, start_col)
        
        #Gera o labirinto a partir da posição inicial
        carve_path(start_row, start_col, maze_temp)
        
        #Define o início
        maze_temp[start_row][start_col] = 2
        
        #Escolhe uma posição para o objetivo (célula acessível, diferente do início)
        accessible_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if maze_temp[i][j] == 1]
        if not accessible_cells:
            continue  #Regenera se não houver células acessíveis
        goal = random.choice(accessible_cells)
        maze_temp[goal[0]][goal[1]] = 3
        
        #Verifica se o labirinto é solucionável
        if is_solvable(maze_temp, start, goal):
            return maze_temp

#Função de ações possíveis
def actions(state, maze_ref=None):
    if maze_ref is None:
        maze_ref = maze
    row, col = state
    possible_actions = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #cima, baixo, esq, dir
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(maze_ref) and 0 <= new_col < len(maze_ref[0]) and maze_ref[new_row][new_col] != 0:
            possible_actions.append((new_row, new_col))
    return possible_actions

#Encontra o estado inicial e objetivo
def find_start_and_goal(maze_ref):
    start = goal = None
    try:
        for i in range(len(maze_ref)):
            for j in range(len(maze_ref[0])):
                if maze_ref[i][j] == 2:
                    start = (i, j)
                if maze_ref[i][j] == 3:
                    goal = (i, j)
        if start is None or goal is None:
            raise ValueError("Início ou objetivo não encontrados no labirinto.")
        return start, goal
    except Exception as e:
        print(f"Erro ao encontrar início e objetivo: {e}")
        return None, None

#Teste de objetivo
def is_goal(state):
    try:
        row, col = state
        return maze[row][col] == 3
    except Exception as e:
        print(f"Erro no teste de objetivo: {e}")
        return False

#Custo de passo
def step_cost(state, action, next_state):
    return 1

#Custo de caminho
def path_cost(path):
    return len(path) - 1 if path else 0

#Heurística para A* (distância de Manhattan)
def heuristic(state, goal):
    row, col = state
    goal_row, goal_col = goal
    return abs(row - goal_row) + abs(col - goal_col)

#Busca em Largura (BFS)
def bfs(start):
    try:
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
    except Exception as e:
        print(f"Erro na BFS: {e}")
        return None

#Busca em Profundidade (DFS)
def dfs(start):
    try:
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
    except Exception as e:
        print(f"Erro na DFS: {e}")
        return None

#Busca A*
def a_star(start, goal):
    try:
        frontier = [(0, start, [start])]  #(f_score, estado, caminho)
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
    except Exception as e:
        print(f"Erro na A*: {e}")
        return None

#Função para exibir o labirinto com o caminho (textual)
def print_maze_with_path(maze_ref, path):
    try:
        if not maze_ref or not all(isinstance(row, list) for row in maze_ref):
            raise ValueError("Matriz do labirinto inválida.")
        maze_copy = [row[:] for row in maze_ref]
        for row, col in path or []:
            if maze_ref[row][col] not in [2, 3]:
                maze_copy[row][col] = '*'
        
        print("\nLabirinto:")
        for row in maze_copy:
            print(' '.join(str(cell).replace('0', '█').replace('1', ' ').replace('2', 'S').replace('3', 'G').replace('*', '*') for cell in row))
    except Exception as e:
        print(f"Erro ao exibir labirinto: {e}")

#Parte textual: executa BFS, DFS e A*
def run_textual_solvers():
    start, goal = find_start_and_goal(maze)
    if start is None or goal is None:
        print("Não foi possível executar os solvers devido a erro no labirinto.")
        return None
    
    print("\n=== Resultados dos Algoritmos de Busca ===")
    
    print("\nBusca em Largura (BFS):")
    bfs_path = bfs(start)
    if bfs_path:
        print("Caminho encontrado:", bfs_path)
        print("Custo do caminho:", path_cost(bfs_path))
        print_maze_with_path(maze, bfs_path)
    else:
        print("Nenhum caminho encontrado.")
    
    print("\nBusca em Profundidade (DFS):")
    dfs_path = dfs(start)
    if dfs_path:
        print("Caminho encontrado:", dfs_path)
        print("Custo do caminho:", path_cost(dfs_path))
        print_maze_with_path(maze, dfs_path)
    else:
        print("Nenhum caminho encontrado.")
    
    print("\nBusca A*:")
    a_star_path = a_star(start, goal)
    if a_star_path:
        print("Caminho encontrado:", a_star_path)
        print("Custo do caminho:", path_cost(a_star_path))
        print_maze_with_path(maze, a_star_path)
    else:
        print("Nenhum caminho encontrado.")
    
    return a_star_path

#Função de configuração do Pygame
def setup():
    global screen, path, maze
    try:
        if not maze: generate_maze() 
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Labirinto")
        screen.fill(WHITE)
        
        #Executa solvers textuais e obtém o caminho do A*
        path = run_textual_solvers() or []
    except Exception as e:
        print(f"Erro na inicialização: {e}")
        if platform.system() != "Emscripten":
            pygame.quit()

#Desenha o labirinto e o caminho
def draw_maze():
    try:
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
        
        #Caminho
        for row, col in path:
            if maze[row][col] not in [2, 3]:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        #Grade
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))
        
        pygame.display.flip()
    except Exception as e:
        print(f"Erro ao desenhar o labirinto: {e}")

def update_loop():
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        draw_maze()
        return True
    except Exception as e:
        print(f"Erro no loop de atualização: {e}")
        return False

# Loop principal
async def main():
    setup()
    if platform.system() == "Emscripten":
        print("Executando em Pyodide. Certifique-se de que o Pygame está configurado corretamente.")
    while update_loop():
        await asyncio.sleep(1.0 / FPS)

# Executa o programa
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pygame.quit()