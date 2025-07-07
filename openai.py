import openai

openai.api_key = "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"

messages = [
    {"role": "system", "content": "Você é muito prestativo"}
]

input_message = input('Digite a pergunta: ')
messages.append({"role": "user", "content": input_message})

while input_message != 'fim':
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = 1,
        max_tokens = 200
    )
    
answer = response['choices'][0]['message']['content']
messages.append({"role": "assistent", "content": answer})

print("Resposta: ", answer)

input_message = input('Digite a pergunta: ')
messages.append({"role": "user", "content": input_message})

