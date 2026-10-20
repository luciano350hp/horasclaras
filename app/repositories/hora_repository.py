from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.hora import Hora


class HoraRepository:
    def listar(
        self,
        db: Session,
        cliente_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Hora]:
        stmt = select(Hora).order_by(Hora.id)
        if cliente_id is not None:
            stmt = stmt.where(Hora.cliente_id == cliente_id)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def obtener_por_id(self, db: Session, hora_id: int) -> Hora | None:
        return db.get(Hora, hora_id)

    def crear(self, db: Session, datos: dict) -> Hora:
        hora = Hora(**datos)
        db.add(hora)
        db.commit()
        db.refresh(hora)
        return hora

    def eliminar(self, db: Session, hora: Hora) -> None:
        db.delete(hora)
        db.commit()
