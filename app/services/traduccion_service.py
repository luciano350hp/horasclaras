from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos.traduccion_dto import TraduccionCreate, TraduccionRead
from app.entities.cliente import TipoCliente
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.traduccion_repository import TraduccionRepository


class TraduccionService:
    def __init__(
        self,
        repository: TraduccionRepository | None = None,
        cliente_repository: ClienteRepository | None = None,
    ) -> None:
        self.repository = repository or TraduccionRepository()
        self.cliente_repository = cliente_repository or ClienteRepository()

    def listar(self, db: Session, cliente_id: int | None = None, skip: int = 0, limit: int = 100):
        items = self.repository.listar(db, cliente_id=cliente_id, skip=skip, limit=limit)
        return [TraduccionRead.model_validate(t) for t in items]

    def obtener(self, db: Session, traduccion_id: int) -> TraduccionRead:
        t = self.repository.obtener_por_id(db, traduccion_id)
        if t is None:
            raise self._no_encontrada(traduccion_id)
        return TraduccionRead.model_validate(t)

    def crear(self, db: Session, datos: TraduccionCreate) -> TraduccionRead:
        cliente = self.cliente_repository.obtener_por_id(db, datos.cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail=f"Cliente {datos.cliente_id} no encontrado")
        if cliente.tipo != TipoCliente.PALABRA:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"El cliente '{cliente.nombre}' no es de tipo 'palabra': "
                    "solo se registran traducciones en clientes por palabra"
                ),
            )
        return TraduccionRead.model_validate(self.repository.crear(db, datos.model_dump()))

    def eliminar(self, db: Session, traduccion_id: int) -> None:
        t = self.repository.obtener_por_id(db, traduccion_id)
        if t is None:
            raise self._no_encontrada(traduccion_id)
        self.repository.eliminar(db, t)

    @staticmethod
    def _no_encontrada(traduccion_id: int) -> HTTPException:
        return HTTPException(status_code=404, detail=f"Traduccion {traduccion_id} no encontrada")
