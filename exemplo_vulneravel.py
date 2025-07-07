import os

def vulneravel():
    comando = input("Digite o comando:")
    eval(comando)
    os.system("ls")