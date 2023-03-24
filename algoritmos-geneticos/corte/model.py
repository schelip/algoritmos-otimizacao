import random
from typing import List, Self

class Peca:
    def __init__(self, id: int, largura: int, altura: int):
        self.id = id
        self.largura = largura
        self.altura = altura
        self.x = None
        self.y = None

    def posicionar(self, x: int, y: int):
        self.x = x
        self.y = y

    def gerar_pecas_aleatorias(n: int, max_altura: int, max_largura: int) -> List[Self]:
        pecas = []
        for i in range(n):
            largura = random.randint(1, max_altura)
            altura = random.randint(1, max_largura)
            pecas.append(Peca(i, largura, altura))
        return pecas
    
    def __str__(self) -> str:
        return f"Peca {self.id} [{self.largura}x{self.altura}] ({self.x}, {self.y})"

class Individuo:
    def __init__(self, largura: int, altura: int, pecas: List[Peca], posicionar: bool = True):
        self.largura = largura
        self.altura = altura
        self.n_pecas = len(pecas)
        if posicionar: self.inserir_pecas_aleatoriamente(pecas)
        else: self.pecas = pecas

    def inserir_peca(self, peca: Peca, x: int, y: int) -> bool:
        for outra_peca in self.pecas:
            if outra_peca.x < x + peca.largura and outra_peca.x + outra_peca.largura > x and \
                    outra_peca.y < y + peca.altura and outra_peca.y + outra_peca.altura > y:
                return False

        # insere a peça na posição desejada
        peca.posicionar(x, y)
        self.pecas.append(peca)
        self.calcular_fitness()
        return True

    def inserir_pecas_aleatoriamente(self, pecas) -> bool:
        self.pecas = []
        for peca in pecas:
            # tenta inserir a peça em posições aleatórias até encontrar uma posição válida
            for _ in range(1000):
                x = random.randint(0, self.largura - peca.largura)
                y = random.randint(0, self.altura - peca.altura)
                if self.inserir_peca(peca, x, y):
                    break
            else:
                # se não encontrou uma posição válida, retorna
                self.calcular_fitness()
    
    def calcular_fitness(self):
        if len(self.pecas) < self.n_pecas:
            self.fitness = 0
            return
        
        for peca in self.pecas:
            if peca.x + peca.largura > self.largura or peca.y + peca.altura > self.altura:
                self.fitness = 0
                return
            
        area_total_pecas = max([peca.x + peca.largura for peca in self.pecas]) * max([peca.y + peca.altura for peca in self.pecas])
        area_ocupada_pecas = sum(peca.largura * peca.altura for peca in self.pecas)

        self.fitness = area_ocupada_pecas / area_total_pecas   

    def crossover(self, outro_individuo: Self) -> Self:
        filho = Individuo(self.largura, self.altura, [], False)
        filho.n_pecas = self.n_pecas

        for i in range(self.n_pecas):
            pecas = [p for p in filter(lambda peca: peca.id == i, self.pecas if random.random() < 0.5 else outro_individuo.pecas)]
            if len(pecas) == 0: break
            peca = pecas[0]
            filho.inserir_peca(Peca(peca.id, peca.largura, peca.altura), peca.x, peca.y)
        
        return filho
    
    def mutacao(self):

        # escolhe uma peça aleatória
        peca_mutada = random.choice(self.pecas)
        self.pecas.remove(peca_mutada)
        
        # tenta inserir a peça em uma nova posição aleatória
        for _ in range(10000):
            x = random.randint(0, self.largura - peca_mutada.largura)
            y = random.randint(0, self.altura - peca_mutada.altura)
            if self.inserir_peca(peca_mutada, x, y):
                break
        
        self.pecas = sorted(self.pecas, key=lambda p: p.id)
        
        self.calcular_fitness()

    
    def gerar_populacao_inicial(n_populacao: int) -> List[Self]:
        TAM_INDIVIDUO = (50, 50)
        TAM_PECA = (15, 15)
        N_PECAS = 10
        pecas = Peca.gerar_pecas_aleatorias(N_PECAS, TAM_PECA[0], TAM_PECA[1])
        return [Individuo(TAM_INDIVIDUO[0], TAM_INDIVIDUO[1], [Peca(peca.id, peca.largura, peca.altura) for peca in pecas]) for _ in range(n_populacao)]