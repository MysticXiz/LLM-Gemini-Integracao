import google.generativeai as genai

genai.configure(api_key='Sua_Chave_Aqui')

#selecione o modelo abaixo
def fazer_pergunta(texto):
    model = genai.GenerativeModel('gemini-2.5-flash')
    resposta = model.generate_content(texto)
    return resposta.text


if __name__ == "__main__":
    print("Bem-vindo ao Assistente do Gemini 🤖")
    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() == "sair":
            break
        resposta = fazer_pergunta(pergunta)
        print(f"\n💡 {resposta}")
