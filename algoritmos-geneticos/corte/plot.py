from model import *
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

def renderizar_individuo(individuo: Individuo, ax: plt.Axes) -> plt.Axes:
    """
    Renderiza um indivíduo no gráfico.

    Args:
        individuo (Individuo): O indivíduo a ser renderizado.
        ax (matplotlib.axes.Axes): O objeto de eixo do matplotlib para o gráfico.

    Returns:
        plt.Axes: O objeto de eixo do matplotlib atualizado.
    """
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

def prepar_plot(n_populacao: int) -> Tuple[plt.Figure, np.ndarray]:
    """
    Prepara o gráfico.

    Args:
        n_populacao (int): O tamanho da população.

    Returns:
        Tuple[plt.Figure, np.ndarray]: Um objeto de figura do matplotlib e um array de eixos do matplotlib.
    """
    num_individuos = min(16, n_populacao)
    max_linhas = min(num_individuos // 4 + (num_individuos % 4 != 0), 4)  # até 4 linhas
    fig, axs = plt.subplots(nrows=max_linhas, ncols=4, figsize=(12, 3.5 * max_linhas))
    fig.subplots_adjust(wspace=0.3, hspace=0.5)
    return fig, axs

def renderizar_graficos(populacao: List[Individuo], geracao: int, fig: plt.figure, axs: np.ndarray, nome_arquivo: str | None=None):
    """
    Renderiza o gráfico com a população atual e a geração atual.

    Args:
        populacao (List[Individuo]): A lista de indivíduos a serem renderizados.
        geracao (int): O número da geração atual.
        fig (plt.Figure): O objeto de figura do matplotlib.
        axs (np.ndarray): O array de objetos de eixos do matplotlib.
        nome_arquivo (str): O nome do arquivo para salvar a renderização.

    Returns:
        None
    """
    plt.cla()
    fig.suptitle(f"Geracao: {geracao}")

    renderizar_individuo(populacao[0], axs[0, 0])

    sample = random.sample(populacao[1:], k=15)

    for i in range(15):
        linha = (i + 1) // 4
        coluna = (i + 1) % 4
        renderizar_individuo(sample[i], axs[linha, coluna])
    
    if nome_arquivo is not None:
        fig.savefig(nome_arquivo)

    fig.canvas.draw()
    fig.canvas.flush_events()

    


