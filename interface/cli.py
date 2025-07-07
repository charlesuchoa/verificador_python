import os
import ast
import argparse
from rich.console import Console
from verificador_formal.z3_verifier import verificar_arquivo_com_z3
from testes_automatizados.hypothesis_runner import executar_hypothesis_em_arquivo
from analisador_estatico.bandit_analyzer import run_bandit
from analisador_estatico.flake8_analyzer import run_flake8
from relatorios.gerador_relatorio import gerar_relatorio


def main_cli():
    parser = argparse.ArgumentParser(description="Verificador Python inspirado no ESBMC")
    parser.add_argument("file", help="Arquivo Python a ser analisado")
    parser.add_argument("--skip-static", action="store_true", help="Ignora Bandit e Flake8")
    parser.add_argument("--run-z3", action="store_true", help="Executa a verificação formal com Z3")
    parser.add_argument("--run-hypothesis", action="store_true", help="Executa os testes automatizados com Hypothesis")
    parser.add_argument("--z3-incremental", action="store_true", help="Usa verificador Z3 em modo incremental")
    parser.add_argument("--solver", choices=["z3", "cvc5", "boolector"], default="z3", help="Escolhe o solver a ser usado na verificação formal")
    parser.add_argument("--context-switch", type=int, default=0, help="Nível de comutação de contexto (reserva para multi-thread)")

    args = parser.parse_args()
    file_path = args.file
    console = Console()

    resultados = {"bandit": {}, "flake8": {}, "formal": [], "hypothesis": []}

    if not args.skip_static:
        console.print(f"[bold green]Analisando {file_path} com Bandit e Flake8...[/bold green]")
        resultados["bandit"][file_path] = run_bandit(file_path)
        resultados["flake8"][file_path] = run_flake8(file_path)

    if args.run_z3:
        console.print("\n[bold yellow]Iniciando Verificação Formal com Z3:[/bold yellow]")
        formals = verificar_arquivo_com_z3(file_path, incremental=args.z3_incremental)
        for item in formals:
            if "assert" in item:
                console.print(f" [green]Propriedade:[/] assert {item['assert']}")
                console.print(f" [cyan]Resultado:[/] {item['resultado']}")
            elif "erro" in item:
                console.print(f" [red]Erro:[/] {item['erro']}")
        resultados["formal"].extend(formals)

    if args.run_hypothesis:
        console.print("\n[bold cyan]Iniciando Testes com Hypothesis:[/bold cyan]")
        hypothesis_result = executar_hypothesis_em_arquivo(file_path)
        for res in hypothesis_result:
            if "teste" in res:
                console.print(f" [blue]Teste:[/] {res['teste']} -> {res['resultado']}")
            elif "erro" in res:
                console.print(f" [red]Erro de execução:[/] {res['erro']}")
        resultados["hypothesis"].append(hypothesis_result)

    # Gera relatório final
    gerar_relatorio(resultados)

    from relatorios.relatorio_html import gerar_relatorio_html
    from relatorios.relatorio_pdf import gerar_relatorio_pdf

    gerar_relatorio_html(resultados)
    gerar_relatorio_pdf(resultados)


if __name__ == "__main__":
    main_cli()