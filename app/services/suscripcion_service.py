from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos.suscripcion_dto import SuscripcionCreate, SuscripcionRead
from app.repositories.suscripcion_repository import SuscripcionRepository


class SuscripcionService:
    def __init__(self, repository: SuscripcionRepository | None = None) -> None:
        self.repository = repository or SuscripcionRepository()

    def crear(self, db: Session, datos: SuscripcionCreate) -> SuscripcionRead:
        if self.repository.obtener_por_email(db, datos.email) is not None:
            raise HTTPException(status_code=409, detail="Ese email ya esta en la lista de espera")
        return SuscripcionRead.model_validate(self.repository.crear(db, datos.email))

    def listar(self, db: Session) -> list[SuscripcionRead]:
        return [SuscripcionRead.model_validate(s) for s in self.repository.listar(db)]
