import base64
import hashlib
import hmac
import secrets
import time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dtos.auth_dto import Credenciales, TokenRead, UsuarioRead
from app.repositories.usuario_repository import UsuarioRepository

ITERACIONES = 120_000


def hashear(password: str) -> str:
    sal = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), sal.encode(), ITERACIONES).hex()
    return f"{sal}${h}"


def verificar(password: str, guardado: str) -> bool:
    sal, h = guardado.split("$", 1)
    calc = hashlib.pbkdf2_hmac("sha256", password.encode(), sal.encode(), ITERACIONES).hex()
    return hmac.compare_digest(calc, h)


def _firmar(cuerpo: str) -> str:
    return hmac.new(settings.secret_key.encode(), cuerpo.encode(), hashlib.sha256).hexdigest()


def crear_token(usuario_id: int) -> str:
    vence = int(time.time()) + settings.token_horas_validez * 3600
    cuerpo = f"{usuario_id}.{vence}"
    return base64.urlsafe_b64encode(f"{cuerpo}.{_firmar(cuerpo)}".encode()).decode()


def leer_token(token: str) -> int | None:
    try:
        uid, vence, firma = base64.urlsafe_b64decode(token.encode()).decode().split(".")
    except Exception:
        return None
    if not hmac.compare_digest(firma, _firmar(f"{uid}.{vence}")) or int(vence) < time.time():
        return None
    return int(uid)


class AuthService:
    def __init__(self, repository: UsuarioRepository | None = None) -> None:
        self.repository = repository or UsuarioRepository()

    def registrar(self, db: Session, datos: Credenciales) -> UsuarioRead:
        if self.repository.obtener_por_email(db, datos.email) is not None:
            raise HTTPException(status_code=409, detail="Ese email ya esta registrado")
        return UsuarioRead.model_validate(
            self.repository.crear(db, datos.email, hashear(datos.password))
        )

    def login(self, db: Session, datos: Credenciales) -> TokenRead:
        u = self.repository.obtener_por_email(db, datos.email)
        if u is None or not verificar(datos.password, u.password_hash):
            raise HTTPException(status_code=401, detail="Email o contrasena incorrectos")
        return TokenRead(access_token=crear_token(u.id))

    def usuario_actual(self, db: Session, token: str) -> UsuarioRead:
        uid = leer_token(token)
        u = self.repository.obtener_por_id(db, uid) if uid else None
        if u is None:
            raise HTTPException(status_code=401, detail="Token invalido o vencido")
        return UsuarioRead.model_validate(u)
