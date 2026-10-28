from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.presupuesto_dto import PresupuestoCreate, PresupuestoRead
from app.services.presupuesto_service import PresupuestoService

router = APIRouter(prefix="/api/presupuestos", tags=["presupuestos"])
service = PresupuestoService()


@router.post("", response_model=PresupuestoRead)
@router.post("/", response_model=PresupuestoRead, include_in_schema=False)
def presupuestar(datos: PresupuestoCreate, db: Session = Depends(get_db)) -> PresupuestoRead:
    return service.presupuestar(db, datos)
