def safe_divide(a, b):
    assert b != 0, "Divisão por zero detectada"
    return a / b

def linear_constraint(x):
    assert 2 * x + 3 > x - 4
    return 2 * x + 3

def compara_strings(s):
    assert isinstance(s, str)
    return s == "openai"

def operacao_modular(x):
    assert x % 2 == 0
    return x // 2

def soma_numeros(x, y):
    assert x + y >= x  # sempre verdade para números positivos
    return x + y

def multiplica_matriz(a, b):
    assert len(a[0]) == len(b), "Número de colunas de A deve ser igual ao número de linhas de B"
    result = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result

if __name__ == "__main__":
    a = 10
    b = 2
    print("Divisão:", safe_divide(a, b))

    print("Resultado linear:", linear_constraint(5))

    print("Comparação de string:", compara_strings("openai"))

    print("Operação modular:", operacao_modular(8))

    print("Soma:", soma_numeros(10, 20))

    matriz_a = [[1, 2], [3, 4]]
    matriz_b = [[2, 0], [1, 2]]
    print("Multiplicação de matrizes:", multiplica_matriz(matriz_a, matriz_b))
