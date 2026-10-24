from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.traduccion_dto import TraduccionCreate, TraduccionRead
from app.services.traduccion_service import TraduccionService

router = APIRouter(prefix="/api/traducciones", tags=["traducciones"])
service = TraduccionService()


@router.get("/", response_model=list[TraduccionRead])
def listar(
    cliente_id: int | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[TraduccionRead]:
    return service.listar(db, cliente_id=cliente_id, skip=skip, limit=limit)


@router.post("/", response_model=TraduccionRead, status_code=status.HTTP_201_CREATED)
def crear(datos: TraduccionCreate, db: Session = Depends(get_db)) -> TraduccionRead:
    return service.crear(db, datos)


@router.get("/{traduccion_id}", response_model=TraduccionRead)
def obtener(traduccion_id: int, db: Session = Depends(get_db)) -> TraduccionRead:
    return service.obtener(db, traduccion_id)


@router.delete("/{traduccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(traduccion_id: int, db: Session = Depends(get_db)) -> None:
    service.eliminar(db, traduccion_id)
