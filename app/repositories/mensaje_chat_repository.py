from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.mensaje_chat import MensajeChat


class MensajeChatRepository:
    def guardar(self, db: Session, conversation_id: str, rol: str, contenido: str) -> MensajeChat:
        m = MensajeChat(conversation_id=conversation_id, rol=rol, contenido=contenido)
        db.add(m)
        db.commit()
        db.refresh(m)
        return m

    def historial(self, db: Session, conversation_id: str, limite: int | None = None) -> list[MensajeChat]:
        stmt = select(MensajeChat).where(MensajeChat.conversation_id == conversation_id)
        stmt = stmt.order_by(MensajeChat.id)
        mensajes = list(db.execute(stmt).scalars().all())
        return mensajes[-limite:] if limite else mensajes
