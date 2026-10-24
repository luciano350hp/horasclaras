from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.tarifario_service import TarifarioService

router = APIRouter(prefix="/api/tarifario", tags=["tarifario"])
service = TarifarioService()


@router.get("/pdf")
def tarifario_pdf(
    profesional: str = Query(default="", max_length=100), db: Session = Depends(get_db)
) -> Response:
    pdf = service.generar_pdf(db, profesional)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="tarifario.pdf"'},
    )
