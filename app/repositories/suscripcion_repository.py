from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.suscripcion import Suscripcion


class SuscripcionRepository:
    def obtener_por_email(self, db: Session, email: str) -> Suscripcion | None:
        return db.execute(select(Suscripcion).where(Suscripcion.email == email)).scalar_one_or_none()

    def crear(self, db: Session, email: str) -> Suscripcion:
        s = Suscripcion(email=email)
        db.add(s)
        db.commit()
        db.refresh(s)
        return s

    def listar(self, db: Session) -> list[Suscripcion]:
        return list(db.execute(select(Suscripcion).order_by(Suscripcion.id)).scalars().all())
