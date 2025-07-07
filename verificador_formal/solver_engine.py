import ast
import z3
from pysmt.shortcuts import Symbol, Int, Equals, NotEquals, is_sat
from pysmt.typing import INT


def executar_solver(file_path, solver="z3", incremental=False):
    resultados = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            codigo = f.read()
        arvore = ast.parse(codigo)

        if solver == "z3":
            resultados.extend(verificacao_z3(arvore, incremental))
        elif solver in ["cvc5", "boolector"]:
            resultados.extend(verificacao_pysmt(arvore, backend=solver))
        else:
            resultados.append({"erro": f"Solver '{solver}' nao suportado."})

    except Exception as e:
        resultados.append({"erro": str(e)})

    return resultados


def verificacao_z3(arvore_ast, incremental=False):
    resultados = []
    b = z3.Int('b')
    s = z3.Solver()
    if incremental:
        s.set("incremental", True)

    # Exemplo: detectar divisao por zero simbolicamente
    s.push()
    s.add(b == 0)
    status = s.check()
    if status == z3.sat:
        print(f"[Z3] Propriedade: assert b != 0  | Linha: {linha_b} | Resultado: FALHA (sat)")
        resultados.append({"propriedade": "assert b != 0", "resultado": "FALHA: sat", "linha": linha_b})
    else:
        print(f"[Z3] Propriedade: assert b != 0  | Linha: {linha_b} | Resultado: VALIDO")
        resultados.append({"propriedade": "assert b != 0", "resultado": "VALIDO", "linha": linha_b})
    s.pop()

    # Propriedade simbolica falsa
    x = z3.Int('x')
    s.push()
    s.add(x != x)
    status = s.check()
    if status == z3.sat:
        resultados.append({"propriedade": "assert x == x", "resultado": "FALHA: sat"})
    else:
        resultados.append({"propriedade": "assert x == x", "resultado": "VALIDO"})
    s.pop()

    return resultados


def verificacao_pysmt(arvore_ast, backend="cvc5"):
    resultados = []
    from pysmt.environment import get_env
    get_env().factory.enable_solver(backend)

    b = Symbol("b", INT)
    formula = Equals(b, Int(0))  # simulando tentativa de b == 0

    if is_sat(formula, solver_name=backend):
        resultados.append({"propriedade": f"assert b != 0 [{backend}]", "resultado": "FALHA: sat"})
    else:
        resultados.append({"propriedade": f"assert b != 0 [{backend}]", "resultado": "VALIDO"})

    return resultados
