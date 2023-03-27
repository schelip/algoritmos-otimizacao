import random
import os
from model import *
from plot import *

N_POPULACAO = 100
N_GERACOES = 1000
P_MUTACAO = 0.2
GEN_RENDERIZAR = 25
TAM_INDIVIDUO = (50, 50)
TAM_PECA = (15, 15)
N_PECAS = 10
NOME_ARQUIVO = "pecas_2"

def main():
    carregar_configuracao = input("Deseja carregar uma configuração existente? (S/N): ").lower() == "s"

    if carregar_configuracao and not os.path.exists(NOME_ARQUIVO):
        print("Não existe nenhuma configuração salva. Gerando nova configuração...")
        carregar_configuracao = False

    if carregar_configuracao:
        print(f"Carregando configuração existente em {NOME_ARQUIVO}")
        pecas = Peca.carregar_pecas(NOME_ARQUIVO)
    else:
        print(f"Gerando pecas aleatórias e salvando em {NOME_ARQUIVO}")
        pecas = Peca.gerar_pecas_aleatorias(N_PECAS, TAM_PECA[0], TAM_PECA[1])
        Peca.salvar_pecas(pecas, NOME_ARQUIVO)
        
    populacao_inicial = Individuo.gerar_populacao_inicial(N_POPULACAO, pecas, TAM_INDIVIDUO)

    print("Iniciando evolução...")
    melhor = algoritmo_genetico(populacao_inicial)
    print(f"Melhor resultado encontrado: {melhor.fitness:.5f}")


def algoritmo_genetico(populacao_inicial: List[Individuo]):
    populacao = sorted(populacao_inicial, key=lambda individuo: -individuo.fitness)

    fig, axs = prepar_plot(N_POPULACAO)
    renderizar_graficos(populacao, 1, fig, axs)

    for i in range(1, N_GERACOES + 1):
        random.shuffle(populacao)
        pares = [populacao[i:i+2] for i in range(0, len(populacao), 2)]
        pares = list(zip(pares[0], pares[1]))

        for pai1, pai2 in zip(populacao[::2], populacao[1::2]):
            filho1, filho2 = pai1.crossover(pai2), pai2.crossover(pai1)
            if random.random() < P_MUTACAO: filho1.mutacao()
            if random.random() < P_MUTACAO: filho2.mutacao()
            populacao += [filho1, filho2]

        populacao = sorted(populacao, key=lambda individuo: -individuo.fitness)
        elitismo = N_POPULACAO // 2
        populacao = populacao[:elitismo] + random.sample(populacao[elitismo:], k=N_POPULACAO - elitismo)

        if i % GEN_RENDERIZAR == 0:
            renderizar_graficos(populacao, i, fig, axs)
    renderizar_graficos(populacao, 1000, fig, axs, "resultado_corte.png")
    return populacao[0]

if __name__ == "__main__":
    main()
