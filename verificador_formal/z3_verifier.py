from z3 import *
import ast


def extrair_asserts(codigo):
    """
    Recebe código-fonte Python como string e extrai instruções assert.
    Retorna uma lista de expressões string.
    """
    tree = ast.parse(codigo)
    asserts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            asserts.append(ast.unparse(node.test))
    return asserts


def analisar_com_z3(expressao_str):
    """
    Tenta traduzir uma string de expressão Python em Z3.
    (Exemplo: 'x + 1 > x')
    """
    x = Int('x')
    y = Int('y')
    z = Int('z')
    try:
        expr = eval(expressao_str)
        solver = Solver()
        solver.add(Not(expr))
        print("Propriedade:", expressao_str)
        print("Enviando para Z3...")
        if solver.check() == unsat:
            print("✔ Verificado: Propriedade é sempre verdadeira")
            return True
        else:
            print("✘ Falhou: Existe contraexemplo")
            print("Modelo:", solver.model())
            return False
    except Exception as e:
        print(f"Erro ao processar a expressão: {expressao_str}")
        print(e)
        return None


def verificar_arquivo_com_z3(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        codigo = f.read()
    asserts = extrair_asserts(codigo)
    print(f"Encontradas {len(asserts)} assertivas no arquivo.")
    resultados = []
    for i, exp in enumerate(asserts):
        print(f"\nAssertiva {i+1}:")
        resultado = analisar_com_z3(exp)
        resultados.append((exp, resultado))
    return resultados