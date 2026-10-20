from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.entities.hora import TipoHora


class HoraBase(BaseModel):
    cliente_id: int = Field(gt=0)
    fecha: date
    minutos: int = Field(gt=0)
    tipo: TipoHora
    observacion: str | None = Field(default=None, max_length=255)


class HoraCreate(HoraBase):
    pass


class HoraRead(HoraBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
