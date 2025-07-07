def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    x = int(input("Digite o primeiro número: "))
    y = int(input("Digite o segundo número: "))
    resultado = mdc(x, y)
    print(f"O MDC de {x} e {y} é {resultado}.")
