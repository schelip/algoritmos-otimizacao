import random
from typing import List, Tuple

def log(string: str):
    """Função útil para habilitar ou desabilitar impressão no console

    Args:
        string (str): valor a ser impresso
    """
    if False:
        print(string)

def gerar_solucao_inicial(tam: int) -> List[int]:
    """
    Gera uma solução inicial aleatória.

    Args:
        tam (int): tamanho da solução.

    Returns:
        List[int]: solução inicial aleatória.
    """
    return [random.randint(0, 1) for _ in range(tam)]


def calcular_qualidade_solucao(solucao: List[int], pesos: List[int], valores: List[int], capacidade: int) -> int:
    """
    Calcula a qualidade de uma solução.
    Args:
        solucao (List[int]): solução a ser avaliada.
        pesos (List[int]): pesos dos itens.
        valores (List[int]): valores dos itens.
        capacidade (int): capacidade da mochila.

    Returns:
        int: valor da solução. Se a solução ultrapassar a capacidade da mochila, retorna -1.
    """
    valor_total = 0
    peso_total = 0
    for i in range(len(solucao)):
        if solucao[i] == 1:
            peso_total += pesos[i]
            valor_total += valores[i]
    if peso_total <= capacidade:
        return valor_total
    return -1


def gerar_vizinhanca(solucao: List[int]) -> List[List[int]]:
    """
    Gera os vizinhos de uma solução.

    Args:
        solucao (List[int]): solução a ser avaliada.

    Returns:
        List[List[int]]: lista com todas as soluções vizinhas da solução dada.
    """
    vizinhos = []
    for i in range(len(solucao)):
        nova_solucao = solucao.copy()
        nova_solucao[i] = 1 - nova_solucao[i]
        vizinhos.append(nova_solucao)
    return vizinhos


def encontrar_melhor_vizinho(vizinhanca: List[List[int]], tabu: List[List[int]], pesos: List[int], valores: List[int], capacidade: int) -> Tuple[List[int], int]:
    """Encontra o melhor vizinho na vizinhança de uma solução.

    Args:
        vizinhanca (List[List[int]]): soluções vizinhas
        tabu (List[List[int]]): soluções na lista tabu.
        pesos (List[int]): pesos dos itens.
        valores (List[int]): valores dos itens.
        capacidade (int): capacidade da mochila.

    Returns:
        Uma tupla contendo a melhor solução vizinha encontrada e o valor dessa solução.
    """
    melhor_vizinho = None
    valor_melhor_vizinho = -1
    for vizinho in vizinhanca:
        if vizinho not in tabu:
            valor_vizinho = calcular_qualidade_solucao(vizinho, pesos, valores, capacidade)
            if valor_vizinho > valor_melhor_vizinho:
                melhor_vizinho = vizinho
                valor_melhor_vizinho = valor_vizinho
    return melhor_vizinho, valor_melhor_vizinho


def busca_tabu(pesos: List[float], valores: List[float], capacidade: float, max_iter: int, tamanho_tabu: int) -> Tuple[List[int], float]:
    """
    Executa uma busca em tabu para resolver o problema da mochila.

    Args:
        pesos (List[int]): pesos dos itens.
        valores (List[int]): valores dos itens.
        capacidade (int): capacidade da mochila.
        max_iter (int): número máximo de iterações.
        tamanho_tabu (int): tamanho da lista tabu.

    Returns:
        Uma tupla contendo a melhor solução encontrada e o valor dessa solução.
        A melhor solução é representada por uma lista de inteiros (0 ou 1), onde cada
        posição representa se o objeto correspondente está presente ou não na mochila.
    """
    atual = gerar_solucao_inicial(len(pesos))
    melhor = atual.copy()
    valor_melhor = calcular_qualidade_solucao(melhor, pesos, valores, capacidade)
    tabu = [atual]
    log(f"Inicial: {melhor, valor_melhor}")

    iter_sem_melhora = 0
    i = 0
    while iter_sem_melhora < max_iter:
        melhor_vizinho, valor_melhor_vizinho = encontrar_melhor_vizinho(gerar_vizinhanca(atual), tabu, pesos, valores, capacidade)
        log(f"Melhor vizinho (iter {i}): {melhor_vizinho, valor_melhor_vizinho}")

        if melhor_vizinho is None:
            break
        
        atual = melhor_vizinho
        tabu.append(atual)

        if valor_melhor_vizinho > valor_melhor:
            melhor = atual.copy()
            valor_melhor = valor_melhor_vizinho
            iter_sem_melhora = 0
            log("Novo melhor")
        else:
            iter_sem_melhora += 1

        # Caso a lista tabu passe do tamanho máximo a solucao mais velha é retirada
        if len(tabu) > tamanho_tabu:
            tabu.pop(0)

        i += 1

    return melhor, calcular_qualidade_solucao(melhor, pesos, valores, capacidade)
