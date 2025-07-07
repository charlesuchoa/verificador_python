def divisao_segura(a, b):
    if b == 0:
        return None
    return a / b

if __name__ == "__main__":
    a = float(input("Digite o valor de a: "))
    b = float(input("Digite o valor de b: "))
    resultado = divisao_segura(a, b)
    if resultado is None:
        print("Divisão por zero não permitida.")
    else:
        print(f"Resultado: {resultado}")
