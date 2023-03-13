from busca_tabu import *

# Caso de teste 1
# Mochila com capacidade 10, 5 itens com pesos e valores diferentes
# Resultado esperado: 23, escolhendo [1, 1, 0, 1, 0] 
capacidade = 10
pesos = [2, 3, 4, 5, 6]
valores = [5, 8, 9, 10, 12]
n = 100
tamanho = 10
melhor, valor = busca_tabu(pesos, valores, capacidade, n, tamanho)
print(f"\nMochila 1: {melhor, valor} (Esperado: {[1, 1, 0, 1, 0], 23})\n")

# Caso de teste 2
# Mochila com capacidade 15, 4 itens com o mesmo peso e valores diferentes
# Resultado esperado: 11, escolhendo [0, 1, 1, 1]
capacidade = 15
pesos = [4, 4, 4, 4]
valores = [1, 2, 3, 6]
n = 100
tamanho = 10
melhor, valor = busca_tabu(pesos, valores, capacidade, n, tamanho)
print(f"\nMochila 2: {melhor, valor} (Esperado: {[0, 1, 1, 1], 11})\n")

# Caso de teste 3
# Mochila com capacidade 20, 6 itens com pesos e valores diferentes
# Resultado esperado: 31, escolhendo [1, 1, 1, 0, 1, 0]
capacidade = 20
pesos = [2, 3, 5, 7, 9, 11]
valores = [6, 7, 8, 9, 10, 12]
n = 100
tamanho = 10
melhor, valor = busca_tabu(pesos, valores, capacidade, n, tamanho)
print(f"\nMochila 3: {melhor, valor} (Esperado: {[1, 1, 1, 0, 1, 0], 31})\n")
