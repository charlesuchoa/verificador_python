import json
import os

def gerar_relatorio(resultados, arquivo="relatorios/relatorio_final.json"):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)
    print(f"Relatório salvo em: {arquivo}")