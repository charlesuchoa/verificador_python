import random

N = 12  # Tamanho do Sudoku (12x12)
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
    if num in tabuleiro[linha]:
        return False
    if num in [tabuleiro[i][coluna] for i in range(N)]:
        return False
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

def simular_falha(tabuleiro):
    """10% de chance de inserir um erro proposital no Sudoku"""
    if random.random() < 0.1:
        print("\n⚠️  Falha proposital inserida no Sudoku!\n")
        # Escolhe uma célula aleatória e insere um número inválido
        linha = random.randint(0, N - 1)
        coluna = random.randint(0, N - 1)
        valor_invalido = tabuleiro[linha][coluna]
        while valor_invalido == tabuleiro[linha][coluna]:
            valor_invalido = random.randint(1, N)
        tabuleiro[linha][coluna] = valor_inv_
