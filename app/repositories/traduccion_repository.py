from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.traduccion import Traduccion


class TraduccionRepository:
    def listar(self, db: Session, cliente_id: int | None = None, skip: int = 0, limit: int = 100):
        stmt = select(Traduccion).order_by(Traduccion.id)
        if cliente_id is not None:
            stmt = stmt.where(Traduccion.cliente_id == cliente_id)
        return list(db.execute(stmt.offset(skip).limit(limit)).scalars().all())

    def listar_del_mes(self, db: Session, desde: date, hasta: date) -> list[Traduccion]:
        stmt = select(Traduccion).where(Traduccion.fecha >= desde, Traduccion.fecha < hasta)
        return list(db.execute(stmt).scalars().all())

    def obtener_por_id(self, db: Session, traduccion_id: int) -> Traduccion | None:
        return db.get(Traduccion, traduccion_id)

    def crear(self, db: Session, datos: dict) -> Traduccion:
        t = Traduccion(**datos)
        db.add(t)
        db.commit()
        db.refresh(t)
        return t

    def eliminar(self, db: Session, t: Traduccion) -> None:
        db.delete(t)
        db.commit()
