import logging
import uuid
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import BASE_DIR, settings
from app.dtos.chat_dto import ChatRequest, ChatResponse, MensajeRead
from app.repositories.mensaje_chat_repository import MensajeChatRepository
from app.services.embeddings_hash import HashEmbeddings

# LangChain se importa recien al usar el asistente: si no esta instalado, el resto de la API anda igual.

log = logging.getLogger(__name__)

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
MENSAJES_DE_HISTORIAL = 6
FRAGMENTOS = 4

SISTEMA = """Sos el asistente virtual de HorasClaras, una aplicación para docentes de inglés y \
traductores independientes que llevan horas, tarifas y cobros.
Respondé en español, de forma breve y clara, usando SOLO la documentación que te paso abajo.
Si la respuesta no está en la documentación, decí que no tenés esa información y sugerí \
probar la pantalla correspondiente. No inventes montos ni reglas.

DOCUMENTACIÓN:
{contexto}"""


def crear_embeddings():
    """fastembed (multilingue, local). Si no se puede bajar el modelo, usa HashEmbeddings."""
    if settings.embeddings_backend == "fastembed":
        try:
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

            emb = FastEmbedEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
            emb.embed_query("prueba")
            return emb
        except Exception as e:  # sin red, modelo bloqueado, paquete faltante
            log.warning("fastembed no disponible (%s). Uso embeddings locales por hash.", e)
    return HashEmbeddings()


class ChatbotService:
    """RAG: busca fragmentos en la base vectorial (Chroma) y se los pasa al LLM (Groq)."""

    def __init__(self, llm=None, embeddings=None, coleccion: str | None = None) -> None:
        self._llm = llm
        self._embeddings = embeddings
        self._coleccion = coleccion
        self._store = None
        self.mensajes = MensajeChatRepository()

    # --- piezas perezosas (no se arman hasta la primera pregunta) ---
    @property
    def llm(self):
        if self._llm is None:
            if not settings.groq_api_key:
                raise HTTPException(
                    status_code=503,
                    detail="El asistente no esta configurado: falta GROQ_API_KEY en el archivo .env",
                )
            from langchain_groq import ChatGroq

            self._llm = ChatGroq(model=settings.groq_model, api_key=settings.groq_api_key, temperature=0.2)
        return self._llm

    @property
    def store(self):
        if self._store is None:
            from langchain_chroma import Chroma

            self._embeddings = self._embeddings or crear_embeddings()
            nombre = self._coleccion or f"horasclaras_{type(self._embeddings).__name__.lower()}"
            persist = None if self._coleccion else settings.chroma_dir
            self._store = Chroma(
                collection_name=nombre, embedding_function=self._embeddings, persist_directory=persist
            )
            if self._store._collection.count() == 0:
                self._indexar()
        return self._store

    def _indexar(self) -> None:
        from langchain_core.documents import Document
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        cortador = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
        docs: list[Document] = []
        for archivo in sorted(Path(KNOWLEDGE_DIR).glob("*.md")):
            texto = archivo.read_text(encoding="utf-8")
            docs += cortador.create_documents([texto], metadatas=[{"fuente": archivo.name}])
        if docs:
            self._store.add_documents(docs)

    # --- caso de uso ---
    def responder(self, db: Session, datos: ChatRequest) -> ChatResponse:
        try:
            from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
        except ImportError as e:
            raise HTTPException(
                status_code=503,
                detail="El asistente no esta instalado: corre pip install -r requirements.txt",
            ) from e
        conversation_id = datos.conversation_id or uuid.uuid4().hex
        fragmentos = self.store.similarity_search(datos.mensaje, k=FRAGMENTOS)
        contexto = "\n\n---\n".join(f.page_content for f in fragmentos)

        historial = self.mensajes.historial(db, conversation_id, MENSAJES_DE_HISTORIAL)
        prompt = [SystemMessage(content=SISTEMA.format(contexto=contexto))]
        for m in historial:
            prompt.append(HumanMessage(content=m.contenido) if m.rol == "user" else AIMessage(content=m.contenido))
        prompt.append(HumanMessage(content=datos.mensaje))

        try:
            respuesta = self.llm.invoke(prompt).content
        except HTTPException:
            raise
        except Exception as e:
            log.exception("Error llamando al LLM")
            raise HTTPException(status_code=502, detail=f"No pude consultar el modelo: {type(e).__name__}") from e

        self.mensajes.guardar(db, conversation_id, "user", datos.mensaje)
        self.mensajes.guardar(db, conversation_id, "assistant", str(respuesta))
        fuentes = sorted({f.metadata.get("fuente", "") for f in fragmentos} - {""})
        return ChatResponse(conversation_id=conversation_id, respuesta=str(respuesta), fuentes=fuentes)

    def historial(self, db: Session, conversation_id: str) -> list[MensajeRead]:
        return [MensajeRead.model_validate(m) for m in self.mensajes.historial(db, conversation_id)]
