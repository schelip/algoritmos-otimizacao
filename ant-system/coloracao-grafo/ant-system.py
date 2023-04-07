import random
import networkx as nx
import matplotlib.pyplot as plt
import os
from typing import List, Tuple

# Parâmetros do Ant System
NUM_FORMIGAS = 10
NUM_ITERACOES = 100
TAXA_EVAPORACAO = 0.5 # taxa de evaporação do feromônio
FEROMONIO_INICIAL = 1.0 # quantidade inicial de feromônio em todas as arestas

NOME_ARQUIVO = 'grafo.txt'
NUM_VERTICES_GERACAO = 15

def main():
    carregar_configuracao = input("Deseja carregar uma configuração existente? (S/N): ").lower() == "s"

    if carregar_configuracao and not os.path.exists(NOME_ARQUIVO):
        print("Não existe nenhuma configuração salva. Gerando nova configuração...")
        carregar_configuracao = False

    if carregar_configuracao:
        print(f"Carregando configuração existente em {NOME_ARQUIVO}")
        with open('grafo.txt', 'r') as arquivo:
            lista_adjacencia = [[int(vertice) for vertice in linha.split()] for linha in arquivo]
    else:
        print(f"Gerando pecas aleatórias e salvando em {NOME_ARQUIVO}")
        lista_adjacencia = []
        with open('grafo.txt', 'w') as arquivo:
            for i in range(NUM_VERTICES_GERACAO):
                lista_adjacencia.append([])
                for j in range(NUM_VERTICES_GERACAO):
                    if (random.random() <= 0.3):
                        lista_adjacencia[i].append(j)
                        arquivo.write(f'{j} ')
                arquivo.write('\n')

    num_vertices = len(lista_adjacencia)
    matriz_adjacencia = [[False] * num_vertices for _ in range(num_vertices)]
    for i, vizinhos in enumerate(lista_adjacencia):
        for j in vizinhos:
            matriz_adjacencia[i][j] = True
        
    print("Iniciando ...")
    melhor_solucao, custo_melhor_solucao = ant_system(matriz_adjacencia)
    print(f"Melhor solução: {melhor_solucao}")
    print(f"Cores melhor solução: {custo_melhor_solucao} - list(set(melhor_solucao))")
    plotar_grafo_colorido(melhor_solucao, matriz_adjacencia)

def plotar_grafo_colorido(vertices: List[int], matriz_adjacencia: List[List[int]]):
    """
    Plota um grafo colorido com base em uma lista de cores e uma matriz de adjacência.

    Args:
    - vertices (List[int]): Uma lista de inteiros representando cada nó do grafo. Cada inteiro deve estar entre 0 e 9.
    - matriz_adjacencia (List[List[int]]): Uma matriz de adjacência representando as conexões entre os nós do grafo.
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
    plt.show()


def escolher_cor(vertice: int, cores: List[str], feromonios: List[List[float]], matriz_adjacencia: List[List[int]]) -> int:
    """
    Escolhe uma cor para um vértice de acordo com as cores disponíveis e os feromônios presentes na matriz.

    Args:
        vertice (int): índice do vértice que se deseja escolher uma cor.
        cores (List[str]): lista de cores disponíveis para a escolha.
        feromonios (List[List[float]]): matriz de feromônios em cada vértice para cada cor disponível.
        matriz_adjacencia (List[List[int]]): matriz de adjacência do grafo.

    Returns:
        int: cor escolhida para o vértice.
    """
    cores_disponiveis = [c for c in cores if c not in matriz_adjacencia[vertice]]
    if len(cores_disponiveis) == 0:
        return random.choice(cores)
    valores_feromonio = [feromonios[vertice][c] for c in range(len(cores)) if cores[c] in cores_disponiveis]
    total_feromonio = sum(valores_feromonio)
    probabilidades = [feromonio / total_feromonio for feromonio in valores_feromonio]
    indice_escolhido = random.choices(range(len(cores_disponiveis)), probabilidades)[0]
    cor_escolhida = cores_disponiveis[indice_escolhido]
    return cor_escolhida

def calcular_custo(solucao: List[int], matriz_adjacencia: List[List[int]]) -> Tuple[int, int]:
    """
    Calcula o custo de uma solução para o problema de coloração de grafos.
    
    Args:
        solucao (List[int]): lista de inteiros representando as cores utilizadas para cada vértice do grafo.
        matriz_adjacencia (List[List[int]]): matriz de adjacência representando as conexões entre os vértices do grafo.

    Returns:
        Tuple[int, int]: Uma tupla contendo o número de conflitos na solução e o número de cores utilizadas.
    """
    num_vertices = len(solucao)
    num_cores = len(set(solucao))
    
    num_conflitos = sum([1 for i in range(num_vertices) 
                         for j in range(i + 1, num_vertices)
                         if matriz_adjacencia[i][j] and solucao[i] == solucao[j]])
    
    return num_conflitos, num_cores

def ant_system(matriz_adjacencia: List[List[int]]) -> Tuple[List[int], int]:
    """Executa o algoritmo do Ant System para coloração de grafos.
    
    Args:
        lista_adjacencia (List[List[int]]): Lista de adjacência do grafo.

    Returns:
        Tuple[List[int], int]: Tupla contendo a melhor solução encontrada e o número de cores utilizadas.
    """
    num_vertices = len(matriz_adjacencia)

    feromonios = [[FEROMONIO_INICIAL for _ in range(num_vertices)] for _ in range(num_vertices)]

    melhor_solucao = [-1] * num_vertices
    custo_melhor_solucao = float('inf')
    num_cores_melhor_solucao = float('inf')

    for i in range(NUM_ITERACOES):
        # Inicializar as soluções parciais das formigas
        solucoes = [[-1] * num_vertices for _ in range(NUM_FORMIGAS)]
        custos = [float('inf') for _ in range(NUM_FORMIGAS)]
        lista_num_cores = [float('inf') for _ in range(NUM_FORMIGAS)]
        
        # Para cada formiga, construir uma solução parcial
        for formiga in range(NUM_FORMIGAS):
            # Inicializar a solução parcial com uma cor aleatória para o primeiro vértice
            cores = list(range(num_vertices))
            random.shuffle(cores)
            solucoes[formiga][0] = cores[0]
            
            # Escolher as cores para os vértices restantes com base na regra de escolha de cor
            for i in range(1, num_vertices):
                vertice = i
                cor_escolhida = escolher_cor(vertice, cores, feromonios, matriz_adjacencia)
                solucoes[formiga][vertice] = cor_escolhida
            
            # Avaliar a qualidade da solução parcial e atualizar a melhor solução encontrada
            custo, num_cores = calcular_custo(solucoes[formiga], matriz_adjacencia)
            custos[formiga] = custo
            lista_num_cores[formiga] = num_cores
            if custo < custo_melhor_solucao or (custo == custo_melhor_solucao and num_cores < num_cores_melhor_solucao):
                melhor_solucao = solucoes[formiga]
                custo_melhor_solucao = custo
                num_cores_melhor_solucao = num_cores
        
        # Atualizar a trilha de feromônio com base nas melhores soluções encontradas
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                delta_feronomio = sum([1.0 / custo if custo != 0 else 0 / num_colors
                                       for custo, num_colors, solution in zip(custos, lista_num_cores, solucoes)
                                       if solution[i] == solution[j]])
                feromonios[i][j] = (1.0 - TAXA_EVAPORACAO) * feromonios[i][j] + delta_feronomio / num_cores_melhor_solucao
                feromonios[j][i] = feromonios[i][j]
        
        # Imprimir o progresso a cada 10 iterações
        if i % 10 == 0:
            print(f"Iteração {i}: Custo melhor solução = {custo_melhor_solucao}; Cores melhor solução = {num_cores_melhor_solucao}")

    return melhor_solucao, num_cores_melhor_solucao

if __name__ == '__main__':
    main()
