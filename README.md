# Implementação de Busca em Largura e Profundidade para resolução de Labirintos

Como atividade proposta na disciplina de Sistemas Inteligentes ofertada na Universidade Federal de Santa Catarina, desenvolveu-se um código em python versão 3.12.3 que gera um labirinto matricialmente composto de Células com valor 1 são por onde é possível se mover, células com valor 0 (zero) representarão lugares que o agente não poderá percorrer (paredes). A célula com valor 2 representa o local de onde o agente iniciará e a célula de valor 3 o lugar onde ele precisa chegar. 

## Funções Desenvolvidas:
- generate_maze(): Gera um Labirinto a partir de divisão recursiva;
- actions(state, maze_ref=None): Verifica quais são as direções de sequência possível;
- find_start_and_goal(maze_ref): Busca o inicio do labirinto e seu objetivo antes de iniciar a solução;
- heuristic(state, goal): Calcula a Distância de Manhattan;
- bfs(start): Executa a Busca em Largura;
- dfs(start): Executa a Busca em Profundidade;
- a_star(start, goal): Encontra o caminho mais curto que resolve o labirinto;
- print_maze_with_path(maze_ref, path) & run_textual_solvers() & draw_maze(): Mostram a resolução do labirinto;


## Exemplo Gerado:
![image](https://github.com/user-attachments/assets/74a0e65e-952f-4f7b-b5bd-c78e252f814a)


**Para o exemplo, obteve-se o seguinte resultado:**

- Busca em Largura (BFS):

  Caminho encontrado: [(1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (8, 9)]

  Custo do caminho: 61


- Busca em Profundidade (DFS):

  Caminho encontrado: [(1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (2, 8), (3, 8), (4, 8), (4, 9), (5, 9), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (4, 1), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 7), (9, 8), (9, 9), (8, 9)]

  Custo do caminho: 49

- Busca A*:

  Caminho encontrado: [(1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (8, 9)]

  Custo do caminho: 18

### Proposição:
[Referência:](https://www.galirows.com.br/meublog/blog/proposta-de-trabalho-metodos-de-busca-para-resolver-um-labirinto/)
https://www.galirows.com.br/meublog/blog/proposta-de-trabalho-metodos-de-busca-para-resolver-um-labirinto/
