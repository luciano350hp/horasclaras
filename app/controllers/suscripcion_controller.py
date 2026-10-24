from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.suscripcion_dto import SuscripcionCreate, SuscripcionRead
from app.services.suscripcion_service import SuscripcionService

router = APIRouter(prefix="/api/waitlist", tags=["lista de espera"])
service = SuscripcionService()


@router.post("", response_model=SuscripcionRead, status_code=status.HTTP_201_CREATED)
def anotarse(datos: SuscripcionCreate, db: Session = Depends(get_db)) -> SuscripcionRead:
    return service.crear(db, datos)


@router.get("", response_model=list[SuscripcionRead])
def listar(db: Session = Depends(get_db)) -> list[SuscripcionRead]:
    return service.listar(db)
