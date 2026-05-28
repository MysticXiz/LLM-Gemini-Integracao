from fastapi.testclient import TestClient
from main import app, botoes, PerguntaRequest
import time

client = TestClient(app)

# ==================================================
# TESTE UNITÁRIO
# ==================================================

def test_metodo_resumir():
    """
    Verifica se o método Resumir existe corretamente
    """
    assert botoes.get("Resumir") == "Resuma o seguinte texto: Se olharmos a vida em seus pequenos detalhes, tudo parece bem ridículo. É como uma gota d`água vista num microscópio, uma só gota cheia de protozoários. Achamos muita graça como eles se agitam e lutam tanto entre si. Aqui, no curto período da vida humana, essa atividade febril produz um efeito cômico."


def test_metodo_invalido():
    """
    Verifica comportamento para método inexistente
    """
    assert botoes.get("ABC") is None


def test_request_model():
    """
    Verifica criação correta do modelo PerguntaRequest
    """
    req = PerguntaRequest(
        texto="Olá",
        metodo="Resumir"
    )

    assert req.texto == "Olá"
    assert req.metodo == "Resumir"


# ==================================================
# TESTE DE INTEGRAÇÃO
# ==================================================

def test_integracao_endpoint():
    """
    Testa integração completa:
    FastAPI -> Gemini -> resposta
    """

    response = client.post(
        "/perguntar",
        json={
            "texto": "Python é uma linguagem de programação.",
            "metodo": "Resumir"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "resultado" in data
    assert len(data["resultado"]) > 0


# ==================================================
# TESTE DE ENTRADA INVÁLIDA
# ==================================================

def test_metodo_invalido_api():
    """
    Testa envio de método inválido
    """

    response = client.post(
        "/perguntar",
        json={
            "texto": "Olá",
            "metodo": "INVALIDO"
        }
    )

    data = response.json()

    assert "erro" in data
    assert data["erro"] == "Método inválido"


def test_texto_vazio():
    """
    Testa envio de texto vazio
    """

    response = client.post(
        "/perguntar",
        json={
            "texto": "",
            "metodo": "Resumir"
        }
    )

    assert response.status_code == 200


# ==================================================
# TESTE DE PERFORMANCE
# ==================================================

def test_tempo_resposta():
    """
    Mede tempo de resposta da API
    """

    inicio = time.time()

    response = client.post(
        "/perguntar",
        json={
            "texto": "Explique inteligência artificial.",
            "metodo": "Resumir"
        }
    )

    fim = time.time()

    tempo = fim - inicio

    print(f"\nTempo de resposta: {tempo:.2f} segundos")

    assert response.status_code == 200

    # limite aceitável
    assert tempo < 15


# ==================================================
# TESTE DE ESTRESSE
# ==================================================

def test_varias_requisicoes():
    """
    Envia várias requisições seguidas
    """

    for i in range(2):

        response = client.post(
            "/perguntar",
            json={
                "texto": f"Mensagem número {i}",
                "metodo": "Resumir"
            }
        )

        assert response.status_code == 200


# ==================================================
# TESTE DE INTEGRIDADE DE DADOS
# ==================================================

def test_retorno_string():
    """
    Verifica se retorno é string válida
    """

    response = client.post(
        "/perguntar",
        json={
            "texto": "Teste de integridade.",
            "metodo": "Resumir"
        }
    )

    data = response.json()

    assert "resultado" in data
    assert isinstance(data["resultado"], str)


# ==================================================
# TESTE DE SISTEMA BÁSICO
# ==================================================

def test_fluxo_completo():
    """
    Simula fluxo principal do sistema
    """
    texto = """
    Python é uma linguagem de programação
    muito utilizada em inteligência artificial.
    """
    response = client.post(
        "/perguntar",
        json={
            "texto": texto,
            "metodo": "Simplificar"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert "resultado" in data