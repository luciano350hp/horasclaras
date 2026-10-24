from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.calculo_dto import CalculoMensual, Dashboard
from app.services.calculo_service import CalculoService

router = APIRouter(prefix="/api", tags=["calculos y dashboard"])
service = CalculoService()


@router.get("/calculos/{anio_mes}", response_model=CalculoMensual)
def calcular_mes(
    anio_mes: str, cliente_id: int | None = Query(default=None), db: Session = Depends(get_db)
) -> CalculoMensual:
    return service.calcular(db, anio_mes, cliente_id)


@router.get("/dashboard/{anio_mes}", response_model=Dashboard)
def dashboard(anio_mes: str, db: Session = Depends(get_db)) -> Dashboard:
    return service.dashboard(db, anio_mes)
