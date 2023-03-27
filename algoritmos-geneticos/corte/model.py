import random
import pickle
from typing import List, Tuple

class Peca:
    """
    Classe que representa uma peça.

    Args:
        id (int): ID da peça
        largura (int): Largura da peça
        altura (int): Altura da peça

    Attributes:
        id (int): ID da peça
        largura (int): Largura da peça
        altura (int): Altura da peça
        x (int): Coordenada X da peça
        y (int): Coordenada Y da peça
    """

    def __init__(self, id: int, largura: int, altura: int):
        self.id = id
        self.largura = largura
        self.altura = altura
        self.x = None
        self.y = None

    def posicionar(self, x: int, y: int):
        """Posiciona a peça em uma coordenada específica"""
        self.x = x
        self.y = y

    @staticmethod
    def gerar_pecas_aleatorias(n: int, max_altura: int, max_largura: int) -> List['Peca']:
        """
        Gera uma lista de peças aleatórias.

        Args:
            n (int): Número de peças a serem geradas
            max_altura (int): Altura máxima da peça
            max_largura (int): Largura máxima da peça

        Returns:
            List['Peca']: Lista de peças geradas aleatoriamente
        """
        pecas = []
        for i in range(n):
            largura = random.randint(1, max_altura)
            altura = random.randint(1, max_largura)
            pecas.append(Peca(i, largura, altura))
        return pecas
    
    @staticmethod
    def salvar_pecas(pecas: List['Peca'], arquivo: str) -> None:
        """
        Salva as peças do indivíduo em um arquivo binário usando pickle.
        
        Parâmetros:
            arquivo (str): nome do arquivo onde as peças serão salvas.
            
        Retorno:
            None
        """
        with open(arquivo, 'wb') as f:
            pickle.dump(pecas, f)

    @staticmethod
    def carregar_pecas(arquivo: str) -> List['Peca']:
        """
        Carrega as peças salvas em um arquivo binário usando pickle.
        
        Parâmetros:
            arquivo (str): nome do arquivo onde as peças estão salvas.
            
        Retorno:
            List[Peca]: lista de objetos Peca carregados do arquivo.
        """
        with open(arquivo, 'rb') as f:
            pecas = pickle.load(f)
        return pecas
    
    def __str__(self) -> str:
        return f"Peca {self.id} [{self.largura}x{self.altura}] ({self.x}, {self.y})"

class Individuo:
    """
    Classe que representa um indivíduo.

    Args:
        largura (int): Largura do indivíduo
        altura (int): Altura do indivíduo
        pecas (List['Peca']): Lista de peças a serem inseridas no indivíduo
        posicionar (bool): Se True, as peças serão inseridas aleatoriamente

    Attributes:
        largura (int): Largura do indivíduo
        altura (int): Altura do indivíduo
        n_pecas (int): Número de peças no indivíduo
        pecas (List['Peca']): Lista de peças inseridas no indivíduo
        fitness (float): Fitness do indivíduo
    """
    def __init__(self, largura: int, altura: int, pecas: List[Peca], posicionar: bool = True):
        self.largura = largura
        self.altura = altura
        self.n_pecas = len(pecas)
        if posicionar: self.inserir_pecas_aleatoriamente(pecas)
        else: self.pecas = pecas

    def inserir_peca(self, peca: Peca, x: int, y: int) -> bool:
        """
        Insere uma peça na posição especificada.
        
        Args:
            peca (Peca): Peça a ser inserida.
            x (int): Posição X para inserir a peça.
            y (int): Posição Y para inserir a peça.
        
        Returns:
            bool: True se a peça foi inserida com sucesso, False caso contrário.
        """
        for outra_peca in self.pecas:
            if outra_peca.x < x + peca.largura and outra_peca.x + outra_peca.largura > x and \
                    outra_peca.y < y + peca.altura and outra_peca.y + outra_peca.altura > y:
                return False

        peca.posicionar(x, y)
        self.pecas.append(peca)
        self.calcular_fitness()
        return True

    def inserir_pecas_aleatoriamente(self, pecas) -> bool:
        """
        Insere as peças aleatoriamente no retângulo.
        
        Args:
            pecas (List[Peca]): Peças a serem inseridas.
        
        Returns:
            bool: True se todas as peças foram inseridas com sucesso, False caso contrário.
        """
        self.pecas = []
        for peca in pecas:
            for _ in range(1000):
                x = random.randint(0, self.largura - peca.largura)
                y = random.randint(0, self.altura - peca.altura)
                if self.inserir_peca(peca, x, y):
                    break
            else:
                self.calcular_fitness()
    
    def calcular_fitness(self):
        """calcula o fitness do indivíduo com base na área total ocupada pelas peças e a
           área total disponível no tabuleiro.
           Se a área total ocupada pelas peças for menor que a área total necessária para
           acomodar todas as peças, o fitness é zero.
           Se uma ou mais peças estiverem fora dos limites do tabuleiro, o fitness é zero.
           Caso contrário, o fitness é calculado como a razão entre a área total ocupada
           pelas peças e a área total disponível no tabuleiro.
        """
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

    def crossover(self, outro_individuo: 'Individuo') -> 'Individuo':
        """Realiza o crossover entre o indivíduo atual e outro indivíduo passado como parâmetro, criando um novo filho.

        Args:
            outro_individuo (Individuo): O indivíduo com o qual será realizado o crossover.

        Returns:
            Individuo: Um novo indivíduo filho criado a partir do crossover dos pais.
        """
        filho = Individuo(self.largura, self.altura, [], False)
        filho.n_pecas = self.n_pecas

        for i in range(self.n_pecas):
            pecas = [p for p in filter(lambda peca: peca.id == i, self.pecas if random.random() < 0.5 else outro_individuo.pecas)]
            if len(pecas) == 0: break
            peca = pecas[0]
            filho.inserir_peca(Peca(peca.id, peca.largura, peca.altura), peca.x, peca.y)
        
        return filho
    
    def mutacao(self):
        """
        Realiza a mutação do indivíduo, alterando aleatoriamente uma das peças já existentes na solução.

        A função escolhe uma peça aleatória, remove-a da solução, e tenta inseri-la em uma nova posição aleatória. Caso a 
        inserção seja possível, o processo de mutação termina. Caso contrário, são feitas mais 9999 tentativas de inserção.
        Se após as 10000 tentativas a inserção não for possível, a função termina sem realizar alterações na solução.

        Após realizar a mutação, a função recalcula o fitness do indivíduo.
        """
        peca_mutada = random.choice(self.pecas)
        self.pecas.remove(peca_mutada)
        
        for _ in range(10000):
            x = random.randint(0, self.largura - peca_mutada.largura)
            y = random.randint(0, self.altura - peca_mutada.altura)
            if self.inserir_peca(peca_mutada, x, y):
                break
        
        self.pecas = sorted(self.pecas, key=lambda p: p.id)
        
        self.calcular_fitness()

    
    def gerar_populacao_inicial(n_populacao: int, pecas: List[Peca], tam: Tuple[int, int]) -> List['Individuo']:
        """Gera uma população inicial de indivíduos para o algoritmo genético.

        Returns:
            int: o número de indíviduos da população a ser gerada.
        """
        return [Individuo(tam[0], tam[1], [Peca(peca.id, peca.largura, peca.altura) for peca in pecas]) for _ in range(n_populacao)]