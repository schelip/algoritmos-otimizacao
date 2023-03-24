from typing import List, Tuple
import random
import numpy as np
from model import *
from plot import *
import matplotlib.pyplot as plt

def corte(n_populacao: int, max_chamadas: int, p_mutacao: float):
    populacao = Individuo.gerar_populacao_inicial(n_populacao)
    populacao = sorted(populacao, key=lambda individuo: -individuo.fitness)

    fig, axs = prepar_plot(n_populacao)
    renderizar_graficos(populacao, 0, fig, axs)

    j = 0
    for i in range(max_chamadas):
        random.shuffle(populacao)
        pares = [populacao[i:i+2] for i in range(0, len(populacao), 2)]
        pares = list(zip(pares[0], pares[1]))

        for pai1, pai2 in zip(populacao[::2], populacao[1::2]):
            filho1, filho2 = pai1.crossover(pai2), pai2.crossover(pai1)
            if random.random() < p_mutacao: filho1.mutacao()
            if random.random() < p_mutacao: filho2.mutacao()
            populacao += [filho1, filho2]

        populacao = sorted(populacao, key=lambda individuo: -individuo.fitness)
        elitismo = n_populacao // 2
        populacao = populacao[:elitismo] + random.sample(populacao[elitismo:], k=n_populacao - elitismo)

        if j == 25:
            renderizar_graficos(populacao, i, fig, axs)
            j = 0
        j += 1

    return populacao[0]

corte(1000, 100000, 0.2)
    