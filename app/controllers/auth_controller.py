from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dtos.auth_dto import Credenciales, TokenRead, UsuarioRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["autenticacion"])
service = AuthService()


@router.post("/registro", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def registro(datos: Credenciales, db: Session = Depends(get_db)) -> UsuarioRead:
    return service.registrar(db, datos)


@router.post("/login", response_model=TokenRead)
def login(datos: Credenciales, db: Session = Depends(get_db)) -> TokenRead:
    return service.login(db, datos)


@router.get("/me", response_model=UsuarioRead)
def me(authorization: str = Header(default=""), db: Session = Depends(get_db)) -> UsuarioRead:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta el token")
    return service.usuario_actual(db, authorization.removeprefix("Bearer "))
