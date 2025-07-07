import random
import time

PRESSAO_MIN = 40   # PSI
PRESSAO_MAX = 100  # PSI

def ler_sensor_pressao():
    return random.uniform(30, 120)

def acionar_valvula_alivio(abrir):
    if abrir:
        print("[ATUADOR] Válvula de alívio ABERTA para reduzir pressão.")
    else:
        print("[ATUADOR] Válvula de alívio FECHADA. Pressão dentro dos limites.")

def controle_pressao():
    pressao = ler_sensor_pressao()
    print(f"[SENSOR] Pressão atual: {pressao:.2f} PSI")

    if pressao < PRESSAO_MIN:
        print("[STATUS] Pressão muito BAIXA. Mantendo válvula FECHADA.")
        acionar_valvula_alivio(False)
    elif pressao > PRESSAO_MAX:
        print("[STATUS] Pressão muito ALTA. Abrindo válvula de alívio.")
        acionar_valvula_alivio(True)
    else:
        print("[STATUS] Pressão dentro dos limites operacionais.")
        acionar_valvula_alivio(False)

if __name__ == "__main__":
    print("=== Sistema de Controle de Pressão da Caldeira ===")
    try:
        while True:
            controle_pressao()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[SISTEMA] Encerrando o controle de pressão.")
