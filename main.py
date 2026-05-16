import os
from google import genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException

# Configure a API key via variável de ambiente em Render: GENAI_API_KEY
API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Defina a variável de ambiente GENAI_API_KEY no Render")

client = genai.Client(api_key=API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

botoes = {
    "Resumir": "Resuma o seguinte texto:",
    "Simplificar": "Simplifique o seguinte texto:",
    "Explicar": "Explique o seguinte texto de forma simples:",
    "Traduzir": "Traduza o seguinte texto para o português:",
}
class PerguntaRequest(BaseModel):
    texto: str
    metodo: str

def fazer_pergunta(texto: str) -> str:
    try:
        resposta = client.models.generate_content(
         model="gemini-2.5-flash",
         contents=texto,
        )
        return resposta.text
    
    except Exception as e:
        return f"Erro na API Gemini: {str(e)}"

@app.post("/perguntar")
async def perguntar(request: PerguntaRequest):

    try:

        texto = request.texto
        metodo = request.metodo
        prompt_base = botoes.get(metodo)
        if not prompt_base:
            return {"erro": "Método inválido"}
        pergunta = f"Apenas realize o que será pedido agora de forma simples sem opções: {prompt_base} {texto}"
        resultado = fazer_pergunta(pergunta)
        return {"resultado": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ajustar a função para filtrar modelos relevantes para texto
@app.get("/modelos")
async def listar_modelos():
    try:
        modelos = client.models.list()
        modelos_texto = [
            modelo.name for modelo in modelos
            if any(keyword in modelo.name.lower() for keyword in ["flash", "pro", "lite"])
            and not any(exclude in modelo.name.lower() for exclude in ["image", "audio", "generate", "embedding", "tts", "robotics", "clip"])
        ]
        return {"modelos": modelos_texto}
    except Exception as e:
        return {"erro": str(e)}

# Opcional: servir frontend estático (apenas se quiser deploy único)
if os.path.isdir("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")