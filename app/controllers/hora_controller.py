from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.hora_dto import HoraCreate, HoraRead
from app.services.hora_service import HoraService

router = APIRouter(prefix="/api/horas", tags=["horas"])

service = HoraService()


@router.get("/", response_model=list[HoraRead])
def listar_horas(
    cliente_id: int | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[HoraRead]:
    return service.listar(db, cliente_id=cliente_id, skip=skip, limit=limit)


@router.post("/", response_model=HoraRead, status_code=status.HTTP_201_CREATED)
def crear_hora(datos: HoraCreate, db: Session = Depends(get_db)) -> HoraRead:
    return service.crear(db, datos)


@router.get("/{hora_id}", response_model=HoraRead)
def obtener_hora(hora_id: int, db: Session = Depends(get_db)) -> HoraRead:
    return service.obtener(db, hora_id)


@router.delete("/{hora_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_hora(hora_id: int, db: Session = Depends(get_db)) -> None:
    service.eliminar(db, hora_id)
