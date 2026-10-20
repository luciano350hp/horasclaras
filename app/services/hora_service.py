from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos.hora_dto import HoraCreate, HoraRead
from app.entities.cliente import TipoCliente
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.hora_repository import HoraRepository


class HoraService:
    def __init__(
        self,
        repository: HoraRepository | None = None,
        cliente_repository: ClienteRepository | None = None,
    ) -> None:
        self.repository = repository or HoraRepository()
        self.cliente_repository = cliente_repository or ClienteRepository()

    def listar(
        self,
        db: Session,
        cliente_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[HoraRead]:
        horas = self.repository.listar(db, cliente_id=cliente_id, skip=skip, limit=limit)
        return [HoraRead.model_validate(hora) for hora in horas]

    def obtener(self, db: Session, hora_id: int) -> HoraRead:
        hora = self.repository.obtener_por_id(db, hora_id)
        if hora is None:
            raise self._no_encontrada(hora_id)
        return HoraRead.model_validate(hora)

    def crear(self, db: Session, datos: HoraCreate) -> HoraRead:
        cliente = self.cliente_repository.obtener_por_id(db, datos.cliente_id)
        if cliente is None:
            raise HTTPException(
                status_code=404, detail=f"Cliente {datos.cliente_id} no encontrado"
            )
        if cliente.tipo != TipoCliente.HORA:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"El cliente '{cliente.nombre}' no es de tipo 'hora': "
                    "solo se registran horas en clientes por hora"
                ),
            )
        hora = self.repository.crear(db, datos.model_dump())
        return HoraRead.model_validate(hora)

    def eliminar(self, db: Session, hora_id: int) -> None:
        hora = self.repository.obtener_por_id(db, hora_id)
        if hora is None:
            raise self._no_encontrada(hora_id)
        self.repository.eliminar(db, hora)

    @staticmethod
    def _no_encontrada(hora_id: int) -> HTTPException:
        return HTTPException(status_code=404, detail=f"Hora {hora_id} no encontrada")
