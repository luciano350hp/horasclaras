from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.chat_dto import ChatRequest, ChatResponse, MensajeRead
from app.services.chatbot_service import ChatbotService

router = APIRouter(prefix="/api/chat", tags=["asistente virtual"])

_service = ChatbotService()


def get_chatbot() -> ChatbotService:
    return _service


@router.post("", response_model=ChatResponse)
def preguntar(
    datos: ChatRequest, db: Session = Depends(get_db), bot: ChatbotService = Depends(get_chatbot)
) -> ChatResponse:
    return bot.responder(db, datos)


@router.get("/{conversation_id}", response_model=list[MensajeRead])
def historial(
    conversation_id: str, db: Session = Depends(get_db), bot: ChatbotService = Depends(get_chatbot)
) -> list[MensajeRead]:
    return bot.historial(db, conversation_id)
