from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.usuario import Usuario


class UsuarioRepository:
    def obtener_por_email(self, db: Session, email: str) -> Usuario | None:
        return db.execute(select(Usuario).where(Usuario.email == email)).scalar_one_or_none()

    def obtener_por_id(self, db: Session, usuario_id: int) -> Usuario | None:
        return db.get(Usuario, usuario_id)

    def crear(self, db: Session, email: str, password_hash: str) -> Usuario:
        u = Usuario(email=email, password_hash=password_hash)
        db.add(u)
        db.commit()
        db.refresh(u)
        return u
