import json
import os

def gerar_relatorio_html(dados, arquivo_html="relatorios/relatorio_final.html"):
    html_inicio = """<!DOCTYPE html>
<html lang='pt-BR'>
<head>
    <meta charset='UTF-8'>
    <title>Relatório de Verificação</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h2 { color: #2E86C1; }
        .section { margin-bottom: 30px; }
        .item { margin-left: 20px; }
        pre { background: #f4f4f4; padding: 10px; }
    </style>
</head>
<body>
<h1>Relatório de Verificação de Código</h1>
"""

    html_conteudo = ""

    html_conteudo += "<div class='section'><h2>Análise Bandit</h2>"
    for arquivo, issues in dados.get("bandit", {}).items():
        html_conteudo += f"<h3>{arquivo}</h3><ul>"
        for item in issues:
            html_conteudo += f"<li class='item'>Linha {item['line_number']}: {item['issue_text']}</li>"
        html_conteudo += "</ul>"
    html_conteudo += "</div>"

    html_conteudo += "<div class='section'><h2>Análise Flake8</h2>"
    for arquivo, issues in dados.get("flake8", {}).items():
        html_conteudo += f"<h3>{arquivo}</h3><ul>"
        for item in issues:
            html_conteudo += f"<li class='item'>Linha {item['line']}: {item['message']}</li>"
        html_conteudo += "</ul>"
    html_conteudo += "</div>"

    html_conteudo += "<div class='section'><h2>Verificação Formal</h2><ul>"
    for verif in dados.get("formal", []):
        if "propriedade" in verif:
            html_conteudo += f"<li class='item'>{verif['propriedade']}: {verif['resultado']}</li>"
        elif "assert" in verif:
            html_conteudo += f"<li class='item'>[assert] {verif['assert']}: {verif['resultado']}</li>"
        elif "erro" in verif:
            html_conteudo += f"<li class='item'>Erro: {verif['erro']}</li>"
        else:
            html_conteudo += f"<li class='item'>Verificação desconhecida: {verif}</li>"


    html_conteudo += "</ul></div>"

    html_fim = "</body></html>"

    os.makedirs(os.path.dirname(arquivo_html), exist_ok=True)
    with open(arquivo_html, "w", encoding="utf-8") as f:
        f.write(html_inicio + html_conteudo + html_fim)

    print(f"Relatório HTML salvo em: {arquivo_html}")
