import google.generativeai as genai

genai.configure(api_key='Sua_Chave_Aqui')

#selecione o modelo abaixo
model = genai.GenerativeModel('gemini-2.5-flash')


if __name__ == "__main__":
    print("Bem-vindo ao Assistente do Gemini 🤖")
    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() == "sair":
            break
        resposta = model.generate_content(pergunta)
        print(f"\n💡 {resposta.text}")
