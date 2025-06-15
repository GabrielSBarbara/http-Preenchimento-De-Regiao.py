import array
import os
from typing import List, Tuple, TypeVar, Generic, Any

# Definindo tipos e exceções
T = TypeVar('T')

class PilhaCheiaErro(Exception): pass
class PilhaVaziaErro(Exception): pass
class TipoErro(Exception): pass

class Pilha(Generic[T]):
    def __init__(self, capacidade: int = 1000):
        self._capacidade = capacidade
        self._dados: List[T] = []
        self._tamanho = 0

    def empilha(self, dado: T) -> None:
        if self.pilha_esta_cheia():
            raise PilhaCheiaErro()
        
        self._dados.append(dado)
        self._tamanho += 1

    def desempilha(self) -> T:
        if self.pilha_esta_vazia():
            raise PilhaVaziaErro()
        self._tamanho -= 1
        return self._dados.pop()

    def pilha_esta_vazia(self) -> bool:
        return self._tamanho == 0

    def pilha_esta_cheia(self) -> bool:
        return self._tamanho == self._capacidade

    def troca(self) -> None:
        if self._tamanho >= 2:
            self._dados[-1], self._dados[-2] = self._dados[-2], self._dados[-1]

    def tamanho(self) -> int:
        return self._tamanho

    def __str__(self):
        return str(list(self._dados))

# Funções para o flood fill
def ler_matriz(nome_arquivo: str) -> List[List[str]]:
    try:
        with open(nome_arquivo) as f:
            return [list(linha.strip()) for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado!")
        exit(1)

def mostrar_matriz(matriz: List[List[str]], passo: Any):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Passo: {passo}")
    for linha in matriz:
        print(''.join(' ' if c == '1' else '#' if c == '0' else c for c in linha))
    input("Pressione ENTER...")

def flood_recursivo(matriz: List[List[str]], x: int, y: int, p: int, passo: int = 0) -> int:
    if x < 0 or x >= len(matriz) or y < 0 or y >= len(matriz[0]) or matriz[x][y] != '1':
        return passo
    
    matriz[x][y] = '0'
    passo += 1
    
    if p > 0 and passo % p == 0:
        mostrar_matriz(matriz, passo)
    
    passo = flood_recursivo(matriz, x+1, y, p, passo)
    passo = flood_recursivo(matriz, x-1, y, p, passo)
    passo = flood_recursivo(matriz, x, y+1, p, passo)
    passo = flood_recursivo(matriz, x, y-1, p, passo)
    
    return passo

def flood_pilha(matriz: List[List[str]], x: int, y: int, p: int) -> int:
    pilha = Pilha[Tuple[int, int]](len(matriz)*len(matriz[0]))
    pilha.empilha((x, y))
    passo = 0
    
    while not pilha.pilha_esta_vazia():
        x, y = pilha.desempilha()
        
        if x < 0 or x >= len(matriz) or y < 0 or y >= len(matriz[0]) or matriz[x][y] != '1':
            continue
        
        matriz[x][y] = '0'
        passo += 1
        
        if p > 0 and passo % p == 0:
            mostrar_matriz(matriz, passo)
        
        pilha.empilha((x+1, y))
        pilha.empilha((x-1, y))
        pilha.empilha((x, y+1))
        pilha.empilha((x, y-1))
    
    return passo

def main():
    nome_arquivo = input("Nome do arquivo com a matriz: ")
    matriz = ler_matriz(nome_arquivo)
    
    # Encontrar posição inicial 'X'
    pos = None
    for i, linha in enumerate(matriz):
        for j, c in enumerate(linha):
            if c == 'X':
                pos = (i, j)
                matriz[i][j] = '1'
                break
        if pos: break
    
    if not pos:
        print("Posição inicial 'X' não encontrada na matriz!")
        return
    
    p = int(input("Passos entre exibições (0 para sem pausas): "))
    
    print("\nMatriz original:")
    mostrar_matriz(matriz, 0)
    
    # Cópias para cada método
    m_rec = [linha.copy() for linha in matriz]
    m_pilha = [linha.copy() for linha in matriz]
    
    print("\nMétodo recursivo:")
    passos = flood_recursivo(m_rec, pos[0], pos[1], p)
    print(f"Concluído em {passos} passos!")
    mostrar_matriz(m_rec, passos)
    
    print("\nMétodo com pilha:")
    passos = flood_pilha(m_pilha, pos[0], pos[1], p)
    print(f"Concluído em {passos} passos!")
    mostrar_matriz(m_pilha, passos)
    
    print("\nResultados iguais?", m_rec == m_pilha)

if __name__ == "__main__":
    main()