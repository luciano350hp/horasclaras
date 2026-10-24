import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from app.controllers.chat_controller import get_chatbot
from app.main import app
from app.services.chatbot_service import ChatbotService
from app.services.embeddings_hash import HashEmbeddings


class LLMEspia(FakeListChatModel):
    """Guarda los prompts que recibe para poder inspeccionarlos en los tests."""

    prompts: list = []

    def _call(self, messages, *args, **kwargs):
        self.prompts.append(messages)
        return super()._call(messages, *args, **kwargs)


@pytest.fixture
def bot() -> ChatbotService:
    llm = LLMEspia(responses=["respuesta de prueba"], prompts=[])
    # coleccion en memoria (sin persistir en disco) + embeddings sin descargas
    servicio = ChatbotService(llm=llm, embeddings=HashEmbeddings(), coleccion="test_chat")
    app.dependency_overrides[get_chatbot] = lambda: servicio
    yield servicio
    app.dependency_overrides.pop(get_chatbot, None)


def test_responde_y_devuelve_conversation_id(client: TestClient, bot) -> None:
    r = client.post("/api/chat", json={"mensaje": "Cuantos clientes puedo tener?"})
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["respuesta"] == "respuesta de prueba"
    assert len(cuerpo["conversation_id"]) > 10


def test_recupera_el_fragmento_correcto_de_la_base_vectorial(client: TestClient, bot) -> None:
    client.post("/api/chat", json={"mensaje": "Cuantos clientes puedo tener como maximo?"})
    contexto = bot.llm.prompts[-1][0].content
    assert "10 clientes" in contexto


def test_busca_descuento_de_palabras_repetidas(client: TestClient, bot) -> None:
    r = client.post("/api/chat", json={"mensaje": "como se calcula el descuento de las palabras repetidas"})
    assert "reglas_de_negocio.md" in r.json()["fuentes"]
    assert "repetidas" in bot.llm.prompts[-1][0].content


def test_mantiene_historial_por_conversacion(client: TestClient, bot) -> None:
    primero = client.post("/api/chat", json={"mensaje": "hola"}).json()
    cid = primero["conversation_id"]
    client.post("/api/chat", json={"mensaje": "y las horas de planificacion?", "conversation_id": cid})
    prompt = bot.llm.prompts[-1]
    textos = [m.content for m in prompt]
    assert "hola" in textos and "respuesta de prueba" in textos  # el turno anterior viaja al modelo
    historial = client.get(f"/api/chat/{cid}").json()
    assert [m["rol"] for m in historial] == ["user", "assistant", "user", "assistant"]


def test_conversaciones_separadas(client: TestClient, bot) -> None:
    a = client.post("/api/chat", json={"mensaje": "hola"}).json()["conversation_id"]
    b = client.post("/api/chat", json={"mensaje": "chau"}).json()["conversation_id"]
    assert a != b
    assert len(client.get(f"/api/chat/{b}").json()) == 2


def test_mensaje_vacio_422(client: TestClient, bot) -> None:
    assert client.post("/api/chat", json={"mensaje": ""}).status_code == 422


def test_sin_clave_de_groq_503(client: TestClient, monkeypatch) -> None:
    from app.core.config import settings

    monkeypatch.setattr(settings, "groq_api_key", "")
    servicio = ChatbotService(embeddings=HashEmbeddings(), coleccion="test_sin_clave")
    app.dependency_overrides[get_chatbot] = lambda: servicio
    try:
        r = client.post("/api/chat", json={"mensaje": "hola"})
    finally:
        app.dependency_overrides.pop(get_chatbot, None)
    assert r.status_code == 503
    assert "GROQ_API_KEY" in r.json()["detail"]


def test_error_del_modelo_502(client: TestClient) -> None:
    class Roto:
        def invoke(self, _):
            raise RuntimeError("groq caido")

    servicio = ChatbotService(llm=Roto(), embeddings=HashEmbeddings(), coleccion="test_roto")
    app.dependency_overrides[get_chatbot] = lambda: servicio
    try:
        r = client.post("/api/chat", json={"mensaje": "hola"})
    finally:
        app.dependency_overrides.pop(get_chatbot, None)
    assert r.status_code == 502
