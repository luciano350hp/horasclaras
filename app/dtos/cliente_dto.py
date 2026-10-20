from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.entities.cliente import TipoCliente

# strip_whitespace va antes que min_length: "   " tiene 3 caracteres, no 0.
SinEspacios = StringConstraints(strip_whitespace=True)


class ClienteBase(BaseModel):
    nombre: Annotated[str, SinEspacios] = Field(min_length=1, max_length=150)
    tipo: TipoCliente
    tarifa: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    descuento_repeticion: Decimal = Field(
        default=Decimal("0.00"), ge=0, le=100, max_digits=5, decimal_places=2
    )


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Annotated[str, SinEspacios] | None = Field(
        default=None, min_length=1, max_length=150
    )
    tipo: TipoCliente | None = None
    tarifa: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    descuento_repeticion: Decimal | None = Field(
        default=None, ge=0, le=100, max_digits=5, decimal_places=2
    )


class ClienteRead(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int