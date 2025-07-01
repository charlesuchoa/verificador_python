from analisador_estatico.bandit_analyzer import run_bandit
from analisador_estatico.flake8_analyzer import run_flake8
from verificador_formal.z3_verifier import verificar_arquivo_com_z3
from testes_automatizados.test_runner import executar_testes_hypothesis
from rich.console import Console
from relatorios.gerador_relatorio import gerar_relatorio
import os

def main_cli():
    import argparse
    parser = argparse.ArgumentParser(description="Verificador Python inspirado no ESBMC")
    parser.add_argument("file", help="Caminho para o arquivo Python a ser analisado")
    args = parser.parse_args()

    console = Console()
    arquivos = []

    if os.path.isfile(args.file):
        arquivos = [args.file]
    elif os.path.isdir(args.file):
        for root, _, files in os.walk(args.file):
            for f in files:
                if f.endswith(".py"):
                    arquivos.append(os.path.join(root, f))

    resultados = {"bandit": {}, "flake8": {}, "formal": []}

    for arquivo in arquivos:
        console.print(f"\n[bold green]Analisando {arquivo}[/]")

        # Análise com Bandit
        bandit_results = run_bandit(arquivo)
        console.print("[bold yellow]Bandit:[/bold yellow]")
        for item in bandit_results:
            console.print(f" {item['line_number']}: {item['issue_text']}")
        resultados["bandit"][arquivo] = bandit_results

        # Análise com Flake8
        flake8_results = run_flake8(arquivo)
        console.print(f"[magenta]Flake8:[/]")
        for item in flake8_results:
            console.print(f" {item['line']}: {item['message']}")
            console.print(f"    → [dim]{item['description']}[/]")
        resultados["flake8"][arquivo] = flake8_results

        # Verificação formal com Z3
        console.print("[blue]\nIniciando verificação formal com Z3...[/blue]")
        z3_resultados = verificar_arquivo_com_z3(arquivo)
        for prop, resultado in z3_resultados:
            resultados["formal"].append({"propriedade": prop, "resultado": resultado})

    # Executa testes Hypothesis (caso arquivo esteja presente)
    hypo_teste_path = "testes_automatizados/hypothesis_tester.py"
    if os.path.exists(hypo_teste_path):
        executar_testes_hypothesis(hypo_teste_path)

    # Geração de relatórios
    gerar_relatorio(resultados)

    from relatorios.relatorio_html import gerar_relatorio_html
    gerar_relatorio_html(resultados)

    from relatorios.relatorio_pdf import gerar_relatorio_pdf
    gerar_relatorio_pdf(resultados)
