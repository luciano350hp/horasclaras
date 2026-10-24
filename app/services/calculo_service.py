import re
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos.calculo_dto import CalculoCliente, CalculoMensual, Dashboard
from app.entities.cliente import TipoCliente
from app.entities.hora import TipoHora
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.hora_repository import HoraRepository
from app.repositories.traduccion_repository import TraduccionRepository

CENT = Decimal("0.01")


def redondear(valor: Decimal) -> Decimal:
    return valor.quantize(CENT, rounding=ROUND_HALF_UP)


def monto_por_horas(minutos_facturables: int, tarifa: Decimal) -> Decimal:
    """minutos/60 x tarifa. Las horas de planificacion nunca llegan aca."""
    return redondear(Decimal(minutos_facturables) / Decimal(60) * tarifa)


def monto_por_palabras(totales: int, repetidas: int, tarifa: Decimal, descuento: Decimal) -> Decimal:
    """(total - repetidas) x tarifa + repetidas x tarifa x (1 - descuento/100)."""
    nuevas = Decimal(totales - repetidas) * tarifa
    repe = Decimal(repetidas) * tarifa * (Decimal(1) - descuento / Decimal(100))
    return redondear(nuevas + repe)


def rango_mes(anio_mes: str) -> tuple[date, date]:
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", anio_mes):
        raise HTTPException(status_code=422, detail="El mes debe tener formato YYYY-MM")
    anio, mes = int(anio_mes[:4]), int(anio_mes[5:])
    desde = date(anio, mes, 1)
    hasta = date(anio + 1, 1, 1) if mes == 12 else date(anio, mes + 1, 1)
    return desde, hasta


class CalculoService:
    def __init__(self) -> None:
        self.clientes = ClienteRepository()
        self.horas = HoraRepository()
        self.traducciones = TraduccionRepository()

    def calcular(self, db: Session, anio_mes: str, cliente_id: int | None = None) -> CalculoMensual:
        desde, hasta = rango_mes(anio_mes)
        clientes = self.clientes.listar(db, skip=0, limit=1000)
        if cliente_id is not None:
            clientes = [c for c in clientes if c.id == cliente_id]
            if not clientes:
                raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
        horas = self.horas.listar_del_mes(db, desde, hasta)
        trads = self.traducciones.listar_del_mes(db, desde, hasta)

        filas: list[CalculoCliente] = []
        for c in clientes:
            fila = CalculoCliente(
                cliente_id=c.id, cliente=c.nombre, tipo=c.tipo.value, tarifa=c.tarifa, monto=Decimal("0.00")
            )
            if c.tipo == TipoCliente.HORA:
                mios = [h for h in horas if h.cliente_id == c.id]
                fila.minutos_facturables = sum(h.minutos for h in mios if h.tipo == TipoHora.FACTURABLE.value)
                fila.minutos_no_facturables = sum(
                    h.minutos for h in mios if h.tipo == TipoHora.PLANIFICACION.value
                )
                fila.monto = monto_por_horas(fila.minutos_facturables, c.tarifa)
            else:
                mias = [t for t in trads if t.cliente_id == c.id]
                fila.palabras_totales = sum(t.palabras_totales for t in mias)
                fila.palabras_repetidas = sum(t.palabras_repetidas for t in mias)
                fila.monto = monto_por_palabras(
                    fila.palabras_totales, fila.palabras_repetidas, c.tarifa, c.descuento_repeticion
                )
            filas.append(fila)
        total = redondear(sum((f.monto for f in filas), Decimal("0")))
        return CalculoMensual(mes=anio_mes, clientes=filas, total=total)

    def dashboard(self, db: Session, anio_mes: str) -> Dashboard:
        calc = self.calcular(db, anio_mes)
        activos = [
            f for f in calc.clientes
            if f.minutos_facturables or f.minutos_no_facturables or f.palabras_totales
        ]
        mejor = max(activos, key=lambda f: f.monto).cliente if activos else None
        return Dashboard(
            mes=anio_mes,
            total_facturado=calc.total,
            horas_facturables=redondear(Decimal(sum(f.minutos_facturables for f in calc.clientes)) / 60),
            horas_no_facturables=redondear(
                Decimal(sum(f.minutos_no_facturables for f in calc.clientes)) / 60
            ),
            palabras_traducidas=sum(f.palabras_totales for f in calc.clientes),
            cantidad_clientes_activos=len(activos),
            mejor_cliente=mejor,
            clientes=calc.clientes,
        )
