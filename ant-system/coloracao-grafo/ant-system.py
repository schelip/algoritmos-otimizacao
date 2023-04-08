import random
import networkx as nx
import matplotlib.pyplot as plt
import os
from typing import List, Tuple
import time

# Parâmetros do Ant System
NUM_FORMIGAS = 10
NUM_ITERACOES = 15
TAXA_EVAPORACAO = 0.5 # taxa de evaporação do feromônio
FEROMONIO_INICIAL = 0.1 # quantidade inicial de feromônio em todas as arestas
PESO_SATURACAO = 0.5 # peso heurística

NOME_ARQUIVO = 'grafo_15.txt'
NUM_VERTICES_GERACAO = 100
P_ARESTAS_GERACAO = 0.3

def main():
    carregar_configuracao = input("Deseja carregar uma configuração existente? (S/N): ").lower() == "s"

    if carregar_configuracao and not os.path.exists(NOME_ARQUIVO):
        print("Não existe nenhuma configuração salva. Gerando nova configuração...")
        carregar_configuracao = False

    if carregar_configuracao:
        print(f"Carregando configuração existente em {NOME_ARQUIVO}")
        with open(NOME_ARQUIVO, 'r') as arquivo:
            lista_adjacencia = [[int(vertice) for vertice in linha.split()] for linha in arquivo]
    else:
        print(f"Gerando pecas aleatórias e salvando em {NOME_ARQUIVO}")
        lista_adjacencia = []
        with open(NOME_ARQUIVO, 'w') as arquivo:
            G = nx.binomial_graph(NUM_VERTICES_GERACAO, P_ARESTAS_GERACAO)
            matriz_grafo = nx.to_numpy_array(G).tolist()
            for i, v in enumerate(matriz_grafo):
                lista_adjacencia.append([])
                for j, a in enumerate(v):
                    if j != i and a == 1:
                        arquivo.write(f"{int(j)} ")
                        lista_adjacencia[i].append(j)
                arquivo.write("\n")

    num_vertices = len(lista_adjacencia)
    matriz_adjacencia = [[False] * num_vertices for _ in range(num_vertices)]
    for i, vizinhos in enumerate(lista_adjacencia):
        for j in vizinhos:
            matriz_adjacencia[i][j] = True
        
    print("Iniciando ...")
    start_time = time.time()
    melhor_solucao, custo_melhor_solucao = ant_system(matriz_adjacencia)
    print(f"Tempo execução: {time.time() - start_time}")
    
    print(f"Melhor solução: {melhor_solucao}")
    print(f"Cores melhor solução: {custo_melhor_solucao} - {list(set(melhor_solucao))}")
    plotar_grafo_colorido(melhor_solucao, matriz_adjacencia)

def plotar_grafo_colorido(vertices: List[int], matriz_adjacencia: List[List[bool]]):
    """
    Plota um grafo colorido com base em uma lista de cores e uma matriz de adjacência.

    Args:
    - vertices (List[int]): Uma lista de inteiros representando cada nó do grafo. Cada inteiro deve estar entre 0 e 9.
    - matriz_adjacencia (List[List[bool]]): Uma matriz de adjacência representando as conexões entre os nós do grafo.
    """
    G = nx.Graph()

    num_vertices = len(vertices)
    for i in range(num_vertices):
        G.add_node(i)

    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            if matriz_adjacencia[i][j]:
                G.add_edge(i,j)

    max_color = max(vertices)
    node_colors = [c / max_color for c in vertices]

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.show()

def escolher_proximo(vertice_atual: int,
                     cor: int,
                     solucao_parcial: List[int],
                     feromonios: List[List[int]],
                     matriz_adjacencia: List[List[bool]]):
    """Move a formiga para um próximo vértice disponível para ser pintado com uma
    cor, com base na heurística (saturação) e nos feromonios

    Args:
        vertice_atual (int): posição atual da formiga
        cor (int): cor para pintura do vértice
        solucao_parcial (List[int]): cores atuais dos vértices do grafo
        feromonios (List[List[int]]): feromonios entre cada par de vértices do grafo
        matriz_adjacencia (List[List[bool]]): Matriz de adjacência do grafo.

    Returns:
        int: Vértice para o qual a formiga escolheu ir
    """
    possiveis = [i for i, v in enumerate(solucao_parcial)
                 if v == -1 and
                 not any([adj and solucao_parcial[j] == cor
                          for j, adj in enumerate(matriz_adjacencia[i])
                          if adj])]
    saturacoes = [len([adj for adj in matriz_adjacencia[v] if adj]) for v in possiveis]

    if len(possiveis) == 0:
        return None

    probabilidades = [((1 / saturacoes[i]) ** PESO_SATURACAO) * feromonios[vertice_atual][i]
                        for i in range(len(possiveis))]
    soma = sum(probabilidades)

    return random.choices(possiveis, [p / soma for p in probabilidades])[0]

def atualizar_feromonios(feromonios: List[List[float]],
                         delta_feromonios) -> List[List[float]]:
    """Aplica evaporação e adicona os feromonios depositados pelas formigas

    Args:
        feromonios (List[List[float]]): Matriz dos feromônios atuais
        delta_feromonios (List[List[float]]): Feromonios depositados pelas formigas

    Returns:
        List[List[float]]: Nova matriz de feromônios
    """
    num_vertices = len(feromonios)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            feromonios[i][j] = (1.0 - TAXA_EVAPORACAO) * feromonios[i][j] + delta_feromonios[i][j]
            feromonios[j][i] = feromonios[i][j]
    return feromonios

def ant_system(matriz_adjacencia: List[List[bool]]) -> Tuple[List[int], int]:
    """Executa o algoritmo do Ant System para coloração de grafos.
    
    Args:
        matriz_adjacencia (List[List[bool]]): Matriz de adjacência do grafo.

    Returns:
        Tuple[List[int], int]: Tupla contendo a melhor solução encontrada e o número de cores utilizadas.
    """
    num_vertices = len(matriz_adjacencia)

    feromonios = [[FEROMONIO_INICIAL for _ in range(num_vertices)] for _ in range(num_vertices)]

    melhor_solucao = [-1] * num_vertices
    custo_melhor_solucao = float('inf')

    for it in range(NUM_ITERACOES):
        solucoes = [[-1] * num_vertices for _ in range(NUM_FORMIGAS)]
        custos = [float('inf') for _ in range(NUM_FORMIGAS)]
        delta_feromonios = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        
        for formiga in range(NUM_FORMIGAS):
            cor = 0
            vertice_atual = random.randint(0, num_vertices - 1)
            solucoes[formiga][vertice_atual] = cor
            visitados = [vertice_atual]
            
            while len(visitados) < num_vertices:
                proximo_vertice = escolher_proximo(vertice_atual, cor, solucoes[formiga], feromonios, matriz_adjacencia)
                if proximo_vertice is not None:
                    visitados.append(proximo_vertice)
                    solucoes[formiga][proximo_vertice] = cor
                    
                    vertice_atual = proximo_vertice
                else:
                    cor += 1

            custos[formiga] = cor + 1

            delta_feromonio = 1 / float(custos[formiga])
            caminho = zip(visitados[:-1], visitados[1:])
            for i, j in caminho:
                delta_feromonios[i][j] += delta_feromonio
                delta_feromonios[j][i] = delta_feromonios[i][j]
            
            if custos[formiga] < custo_melhor_solucao:
                melhor_solucao = solucoes[formiga][:]
                custo_melhor_solucao = custos[formiga]
        
        feromonios = atualizar_feromonios(feromonios, delta_feromonios)
        
        print(f"Iteração {it}: Custo melhor solução = {custo_melhor_solucao};")

    return melhor_solucao, custo_melhor_solucao

if __name__ == '__main__':
    main()
