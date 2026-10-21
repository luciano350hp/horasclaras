from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.entities.cliente import Cliente


class ClienteRepository:
    def listar(self, db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
        stmt = select(Cliente).order_by(Cliente.id).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def contar(self, db: Session) -> int:
        return db.execute(select(func.count()).select_from(Cliente)).scalar_one()

    def obtener_por_id(self, db: Session, cliente_id: int) -> Cliente | None:
        return db.get(Cliente, cliente_id)

    def obtener_por_nombre(self, db: Session, nombre: str) -> Cliente | None:
        stmt = select(Cliente).where(Cliente.nombre == nombre)
        return db.execute(stmt).scalars().first()

    def crear(self, db: Session, datos: dict) -> Cliente:
        cliente = Cliente(**datos)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    def actualizar(self, db: Session, cliente: Cliente, datos: dict) -> Cliente:
        for campo, valor in datos.items():
            setattr(cliente, campo, valor)
        db.commit()
        db.refresh(cliente)
        return cliente

    def eliminar(self, db: Session, cliente: Cliente) -> None:
        db.delete(cliente)
        db.commit()