from model import *
from typing import List
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

def renderizar_individuo(individuo, ax):
    ax.clear()
    ax.set_xlim([0, individuo.largura])
    ax.set_ylim([0, individuo.altura])
    ax.set_aspect('equal')
    ax.set_title(f"Fitness: {individuo.fitness:.5f}")
    for peca in individuo.pecas:
        rect = plt.Rectangle((peca.x, peca.y), peca.largura, peca.altura, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(peca.x + peca.largura/2, peca.y + peca.altura/2, str(peca.id), ha='center', va='center', fontsize=8)
    return ax

def prepar_plot(n_populacao):
    num_individuos = min(16, n_populacao)
    max_linhas = min(num_individuos // 4 + (num_individuos % 4 != 0), 4)  # até 4 linhas
    fig, axs = plt.subplots(nrows=max_linhas, ncols=4, figsize=(12, 3.5 * max_linhas))
    fig.subplots_adjust(wspace=0.3, hspace=0.5)
    return fig, axs

def renderizar_graficos(populacao, geracao, fig, axs):
    plt.cla()
    fig.suptitle(f"Geracao: {geracao}")

    renderizar_individuo(populacao[0], axs[0, 0])

    sample = random.sample(populacao[1:], k=15)

    for i in range(15):
        linha = (i + 1) // 4
        coluna = (i + 1) % 4
        renderizar_individuo(sample[i], axs[linha, coluna])
    
    
    fig.canvas.draw()
    fig.canvas.flush_events()

    


