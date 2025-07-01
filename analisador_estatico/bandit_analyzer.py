import subprocess
import sys
import os
import json
from utils.remover_comentarios import limpar_codigo

def run_bandit(file_path):
    """
    Executa Bandit ignorando comentários.
    Gera um arquivo temporário sem comentários no mesmo diretório do original.
    """
    # Limpa o código
    codigo_limpo = limpar_codigo(file_path)

    # Cria arquivo temporário no mesmo diretório do original
    base, ext = os.path.splitext(file_path)
    caminho_temp = f"{base}_sem_comentarios{ext}"

    with open(caminho_temp, 'w', encoding='utf-8') as f:
        f.write(codigo_limpo)

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'bandit','--verbose', '-f', 'json', '-r', caminho_temp],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Converte saída JSON para lista de dicionários
        output = json.loads(result.stdout)
        return output.get("results", [])

    finally:
        # Remove o arquivo temporário
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)
