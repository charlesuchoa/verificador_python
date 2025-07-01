import importlib.util
from rich.console import Console


def executar_testes_hypothesis(path):
    console = Console()
    console.print("\n[cyan]Executando testes Hypothesis...[/cyan]")

    spec = importlib.util.spec_from_file_location("hypo_module", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Procura funções que comecem com 'test_'
    for nome in dir(mod):
        if nome.startswith("test_"):
            func = getattr(mod, nome)
            console.print(f"Testando {nome}...")
            try:
                func()  # Hypothesis roda automaticamente com o decorator @given
            except AssertionError as e:
                console.print(f"[red]Falha: {e}[/red]")
            except Exception as e:
                console.print(f"[red]Erro inesperado: {e}[/red]")