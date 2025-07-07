from z3 import *
import ast

# Mapeia padrões perigosos comuns para gerar asserts automaticamente
PADROES_CRITICOS = {
    'DivisaoPorZero': lambda node: isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div),
    'IndiceNegativo': lambda node: isinstance(node, ast.Subscript),
    'AcessoAtributo': lambda node: isinstance(node, ast.Attribute),
    'ComparacaoNone': lambda node: isinstance(node, ast.Compare) and any(isinstance(op, ast.Is) or isinstance(op, ast.Eq) for op in node.ops),
}

def gerar_asserts_automaticos(tree):
    """
    Gera asserts para padrões perigosos em tempo de verificação estática.
    """
    asserts = []
    for node in ast.walk(tree):
        for nome, func in PADROES_CRITICOS.items():
            if func(node):
                if nome == 'DivisaoPorZero':
                    asserts.append("b != 0")
                elif nome == 'IndiceNegativo':
                    asserts.append("index >= 0")
                elif nome == 'AcessoAtributo':
                    asserts.append("obj is not None")
                elif nome == 'ComparacaoNone':
                    asserts.append("variavel is not None")
    return list(set(asserts))

def verificar_arquivo_com_z3(file_path, incremental=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    resultado = []
    try:
        tree = ast.parse(source)

        # Extrai asserts manuais
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                expr_str = ast.unparse(node.test)
                s = Solver()
                x = Int('x')
                try:
                    expr_z3 = eval(expr_str, {'x': x, 'Int': Int, 'And': And, 'Or': Or})
                    s.add(Not(expr_z3))
                    check = s.check()
                    resultado.append({
                        "assert": expr_str,
                        "resultado": "VALIDO" if check == unsat else f"FALHA: {check}"
                    })
                except Exception as e:
                    resultado.append({
                        "assert": expr_str,
                        "resultado": f"ERRO NA ANALISE: {e}"
                    })

        # Adiciona asserts automáticos
        auto_asserts = gerar_asserts_automaticos(tree)
        for expr in auto_asserts:
            s = Solver()
            x, b, index, obj, variavel = Int('x'), Int('b'), Int('index'), Int('obj'), Int('variavel')
            try:
                expr_z3 = eval(expr, {'x': x, 'b': b, 'index': index, 'obj': obj, 'variavel': variavel,
                                      'Int': Int, 'And': And, 'Or': Or})
                s.add(Not(expr_z3))
                check = s.check()
                resultado.append({
                    "assert": expr,
                    "resultado": "VALIDO" if check == unsat else f"FALHA: {check}"
                })
            except Exception as e:
                resultado.append({
                    "assert": expr,
                    "resultado": f"ERRO NA ANALISE: {e}"
                })

    except Exception as e:
        resultado.append({"erro": str(e)})

    return resultado