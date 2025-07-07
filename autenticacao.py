def autenticar(usuario, senha):
    if usuario == "admin" and senha == "123456":
        return True
    return False

if __name__ == "__main__":
    user = input("Usuário: ")
    senha = input("Senha: ")

    if autenticar(user, senha):
        print("Acesso concedido.")
    else:
        print("Acesso negado.")
