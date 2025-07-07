variavel = "import requests
import json

API_KEY = "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"
link = "https://api.openai.com/v1/models"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
id_modelo = "gpt-3.5-turbo"
body_mensagem = {
    "model": id_modelo,
    "messages": [
        {"role": "user","content": "Escreva o valor da cotação do dolar hoje em relação a moeda REAL do Brasil."}
    ]
}

body_mensagem = json.dumps(body_mensagem)"

print(variavel)