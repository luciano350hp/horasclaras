from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TraduccionBase(BaseModel):
    cliente_id: int = Field(gt=0)
    fecha: date
    palabras_totales: int = Field(gt=0)
    palabras_repetidas: int = Field(default=0, ge=0)
    descripcion: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def repetidas_no_superan_totales(self) -> "TraduccionBase":
        if self.palabras_repetidas > self.palabras_totales:
            raise ValueError("Las palabras repetidas no pueden superar a las totales")
        return self


class TraduccionCreate(TraduccionBase):
    pass


class TraduccionRead(TraduccionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
