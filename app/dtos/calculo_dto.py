from decimal import Decimal

from pydantic import BaseModel


class CalculoCliente(BaseModel):
    cliente_id: int
    cliente: str
    tipo: str
    tarifa: Decimal
    minutos_facturables: int = 0
    minutos_no_facturables: int = 0
    palabras_totales: int = 0
    palabras_repetidas: int = 0
    monto: Decimal


class CalculoMensual(BaseModel):
    mes: str
    clientes: list[CalculoCliente]
    total: Decimal


class Dashboard(BaseModel):
    mes: str
    total_facturado: Decimal
    horas_facturables: Decimal
    horas_no_facturables: Decimal
    palabras_traducidas: int
    cantidad_clientes_activos: int
    mejor_cliente: str | None
    clientes: list[CalculoCliente]
