from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.cliente_dto import ClienteCreate, ClienteRead, ClienteUpdate
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/api/clientes", tags=["clientes"])

service = ClienteService()


@router.get("/", response_model=list[ClienteRead])
def listar_clientes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[ClienteRead]:
    return service.listar(db, skip=skip, limit=limit)


@router.post("/", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)) -> ClienteRead:
    return service.crear(db, datos)


@router.get("/{cliente_id}", response_model=ClienteRead)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)) -> ClienteRead:
    return service.obtener(db, cliente_id)


@router.patch("/{cliente_id}", response_model=ClienteRead)
def actualizar_cliente(
    cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)
) -> ClienteRead:
    return service.actualizar(db, cliente_id, datos)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)) -> None:
    service.eliminar(db, cliente_id)