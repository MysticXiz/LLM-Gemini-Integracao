import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Configure a API key via variável de ambiente em Render: GENAI_API_KEY
API_KEY = os.getenv("GENAI_API_KEY")
# if not API_KEY:
#     raise RuntimeError("Defina a variável de ambiente GENAI_API_KEY no Render")

genai.configure(api_key=API_KEY)

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
    "Traduzir": "Traduza o seguinte texto para o inglês:",
}
class PerguntaRequest(BaseModel):
    texto: str
    metodo: str

def fazer_pergunta(texto: str) -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    resposta = model.generate_content(texto)
    return getattr(resposta, "text", str(resposta))

@app.post("/perguntar")
async def perguntar(request: PerguntaRequest):
    texto = request.texto
    metodo = request.metodo
    pergunta = f"{botoes.get(metodo)} {texto}"
    resultado = fazer_pergunta(pergunta)
    return {"resultado": resultado}

# Opcional: servir frontend estático (apenas se quiser deploy único)
if os.path.isdir("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")