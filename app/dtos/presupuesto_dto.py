from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class PresupuestoCreate(BaseModel):
    texto: str = Field(max_length=200_000)
    cliente_id: int

    @field_validator("texto")
    @classmethod
    def texto_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El texto no puede estar vacio")
        return v


class PresupuestoRead(BaseModel):
    cliente_id: int
    cliente: str
    tarifa: Decimal
    descuento_repeticion: Decimal
    palabras_totales: int
    palabras_repetidas: int
    palabras_nuevas: int
    monto_sin_descuento: Decimal
    monto: Decimal
    segmentos_repetidos: list[str]
