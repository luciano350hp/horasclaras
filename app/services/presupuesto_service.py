import re
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos.presupuesto_dto import PresupuestoCreate, PresupuestoRead
from app.entities.cliente import TipoCliente
from app.repositories.cliente_repository import ClienteRepository
from app.services.calculo_service import monto_por_palabras, redondear

PALABRA = re.compile(r"\w+(?:['’]\w+)*", re.UNICODE)
SEGMENTOS = re.compile(r"(?<=[.!?])\s+|\n+")


def contar_palabras(texto: str) -> int:
    return len(PALABRA.findall(texto))


def analizar(texto: str) -> tuple[int, int, list[str]]:
    """Devuelve (palabras totales, palabras repetidas, segmentos repetidos).

    Un segmento (frase o linea) es repetido si, ignorando mayusculas y espacios
    extra, ya aparecio antes. Se cuentan como repetidas las palabras de las
    apariciones posteriores a la primera.
    """
    vistos: set[str] = set()
    repetidos: list[str] = []
    totales = 0
    repetidas = 0
    for seg in SEGMENTOS.split(texto):
        seg = seg.strip()
        n = contar_palabras(seg)
        if n == 0:
            continue
        totales += n
        clave = " ".join(seg.lower().split())
        if clave in vistos:
            repetidas += n
            if seg not in repetidos:
                repetidos.append(seg)
        else:
            vistos.add(clave)
    return totales, repetidas, repetidos


class PresupuestoService:
    def __init__(self, cliente_repository: ClienteRepository | None = None) -> None:
        self.clientes = cliente_repository or ClienteRepository()

    def presupuestar(self, db: Session, datos: PresupuestoCreate) -> PresupuestoRead:
        cliente = self.clientes.obtener_por_id(db, datos.cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail=f"Cliente {datos.cliente_id} no encontrado")
        if cliente.tipo != TipoCliente.PALABRA:
            raise HTTPException(
                status_code=422,
                detail=f"El cliente '{cliente.nombre}' no es de tipo 'palabra': el presupuesto es solo para clientes por palabra",
            )
        totales, repetidas, segmentos = analizar(datos.texto)
        if totales == 0:
            raise HTTPException(status_code=422, detail="El texto no tiene palabras")
        return PresupuestoRead(
            cliente_id=cliente.id,
            cliente=cliente.nombre,
            tarifa=cliente.tarifa,
            descuento_repeticion=cliente.descuento_repeticion,
            palabras_totales=totales,
            palabras_repetidas=repetidas,
            palabras_nuevas=totales - repetidas,
            monto_sin_descuento=redondear(Decimal(totales) * cliente.tarifa),
            monto=monto_por_palabras(totales, repetidas, cliente.tarifa, cliente.descuento_repeticion),
            segmentos_repetidos=segmentos,
        )
