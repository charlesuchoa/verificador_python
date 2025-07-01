import subprocess
import sys
import os
import re
from utils.remover_comentarios import limpar_codigo
from utils.flake8_codigos import flake8_codigos  # Novo import com descrições dos erros

def run_flake8(file_path):
    """
    Executa Flake8 ignorando comentários e retorna lista de problemas com descrição.
    """
    print(f"Analisando {file_path}")

    # Limpa o código fonte ignorando comentários
    codigo_limpo = limpar_codigo(file_path)

    # Cria arquivo temporário no mesmo diretório do original
    base, ext = os.path.splitext(file_path)
    caminho_temp = f"{base}_sem_comentarios{ext}"

    with open(caminho_temp, 'w', encoding='utf-8') as f:
        f.write(codigo_limpo)

    try:
        # Executa flake8 com saída formatada
        result = subprocess.run(
            [
                sys.executable, "-m", "flake8", caminho_temp,
                "--statistics", "--show-source", "--count",
                "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        issues = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split(":")
                if len(parts) >= 4:
                    linha = int(parts[1])
                    coluna = int(parts[2])
                    mensagem = parts[3].strip()

                    # Extração do código (ex: E302, F821)
                    match = re.match(r'([A-Z]\d+)', mensagem)
                    if match:
                        cod_erro = match.group(1)
                        descricao = flake8_codigos.get(cod_erro, "Descrição não disponível.")
                    else:
                        cod_erro = "N/A"
                        descricao = "Erro desconhecido."

                    issues.append({
                        "file": parts[0],
                        "line": linha,
                        "column": coluna,
                        "message": mensagem,
                        "code": cod_erro,
                        "description": descricao
                    })
        return issues

    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)
