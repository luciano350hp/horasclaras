from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dtos.cliente_dto import ClienteCreate, ClienteRead, ClienteUpdate
from app.repositories.cliente_repository import ClienteRepository

MAXIMO_CLIENTES = 10


class ClienteService:
    def __init__(self, repository: ClienteRepository | None = None) -> None:
        self.repository = repository or ClienteRepository()

    def listar(self, db: Session, skip: int = 0, limit: int = 100) -> list[ClienteRead]:
        return [ClienteRead.model_validate(c) for c in self.repository.listar(db, skip, limit)]

    def obtener(self, db: Session, cliente_id: int) -> ClienteRead:
        cliente = self.repository.obtener_por_id(db, cliente_id)
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} no encontrado",
            )
        return ClienteRead.model_validate(cliente)

    def crear(self, db: Session, datos: ClienteCreate) -> ClienteRead:
        nombre = self._normalizar(datos.nombre)
        if self.repository.obtener_por_nombre(db, nombre) is not None:
            raise self._duplicado(nombre)
        if self.repository.contar(db) >= MAXIMO_CLIENTES:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se pueden tener mas de {MAXIMO_CLIENTES} clientes",
            )
        try:
            creado = self.repository.crear(db, {**datos.model_dump(), "nombre": nombre})
        except IntegrityError:
            db.rollback()
            raise self._duplicado(nombre) from None
        return ClienteRead.model_validate(creado)

    def actualizar(self, db: Session, cliente_id: int, datos: ClienteUpdate) -> ClienteRead:
        cliente = self.repository.obtener_por_id(db, cliente_id)
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} no encontrado",
            )
        cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
        if "nombre" in cambios:
            cambios["nombre"] = self._normalizar(cambios["nombre"])
            existente = self.repository.obtener_por_nombre(db, cambios["nombre"])
            if existente is not None and existente.id != cliente.id:
                raise self._duplicado(cambios["nombre"])
        try:
            actualizado = self.repository.actualizar(db, cliente, cambios)
        except IntegrityError:
            db.rollback()
            raise self._duplicado(cambios.get("nombre", cliente.nombre)) from None
        return ClienteRead.model_validate(actualizado)

    def eliminar(self, db: Session, cliente_id: int) -> None:
        cliente = self.repository.obtener_por_id(db, cliente_id)
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} no encontrado",
            )
        self.repository.eliminar(db, cliente)

    @staticmethod
    def _normalizar(nombre: str) -> str:
        return nombre.strip()

    @staticmethod
    def _duplicado(nombre: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un cliente con el nombre '{nombre}'",
        )