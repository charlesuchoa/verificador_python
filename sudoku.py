import random

N = 9  # Tamanho do Sudoku (12x12)
SQN = 3  # Raiz quadrada de N (3x3 blocos)

def imprime_sudoku(tabuleiro):
    for i in range(N):
        linha = ''
        for j in range(N):
            linha += f'{tabuleiro[i][j]} '
            if (j + 1) % SQN == 0 and j < N - 1:
                linha += '| '
        print(linha)
        if (i + 1) % SQN == 0 and i < N - 1:
            print('-' * 21)

def num_valido(tabuleiro, linha, coluna, num):
    # Verifica a linha
    if num in tabuleiro[linha]:
        return False
    # Verifica a coluna
    if num in [tabuleiro[i][coluna] for i in range(N)]:
        return False
    # Verifica o bloco 3x3
    start_linha = linha - linha % SQN
    start_coluna = coluna - coluna % SQN
    for i in range(SQN):
        for j in range(SQN):
            if tabuleiro[start_linha + i][start_coluna + j] == num:
                return False
    return True

def resolve(tabuleiro):
    for linha in range(N):
        for coluna in range(N):
            if tabuleiro[linha][coluna] == 0:
                numeros = list(range(1, N + 1))
                random.shuffle(numeros)
                for num in numeros:
                    if num_valido(tabuleiro, linha, coluna, num):
                        tabuleiro[linha][coluna] = num
                        if resolve(tabuleiro):
                            return True
                        tabuleiro[linha][coluna] = 0
                return False
    return True

def gerar_sudoku():
    tabuleiro = [[0 for _ in range(N)] for _ in range(N)]
    resolve(tabuleiro)
    return tabuleiro

if __name__ == "__main__":
    print("\n Sudoku Gerado com sucesso:\n")
    sudoku = gerar_sudoku()
    imprime_sudoku(sudoku)
