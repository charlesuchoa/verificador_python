from hypothesis import given, strategies as st
from hypothesis import settings
import importlib.util
import traceback
import sys
import os

def executar_hypothesis_em_arquivo(file_path):
    nome_modulo = os.path.splitext(os.path.basename(file_path))[0]
    try:
        spec = importlib.util.spec_from_file_location(nome_modulo, file_path)
        modulo = importlib.util.module_from_spec(spec)
        sys.modules[nome_modulo] = modulo
        spec.loader.exec_module(modulo)

        # Procura funções que começam com test_
        testes = [getattr(modulo, nome) for nome in dir(modulo) if callable(getattr(modulo, nome)) and nome.startswith("test_")]

        resultados = []
        for teste in testes:
            try:
                teste()
                resultados.append({"teste": teste.__name__, "resultado": "SUCESSO"})
            except Exception as e:
                resultados.append({"teste": teste.__name__, "resultado": f"FALHOU: {str(e)}"})
        return resultados

    except Exception as e:
        return [{"erro": traceback.format_exc()}]
