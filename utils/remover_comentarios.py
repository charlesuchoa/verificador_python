import re

def limpar_codigo(caminho_arquivo):
    """
    Lê um arquivo Python e retorna seu conteúdo sem comentários.
    """
    codigo_limpo = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    for linha in linhas:
        linha_strip = linha.strip()
        if linha_strip.startswith("#") or linha_strip == "":
            continue

        # Remove comentários inline (ex: x = 1  # comentário)
        linha_sem_inline = re.sub(r'#.*', '', linha)
        if linha_sem_inline.strip() != "":
            codigo_limpo.append(linha_sem_inline.rstrip())

    return "\n".join(codigo_limpo)
