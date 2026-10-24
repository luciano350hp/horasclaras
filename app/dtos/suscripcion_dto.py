import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_email(valor: str) -> str:
    valor = valor.strip().lower()
    if len(valor) > 254 or not EMAIL_RE.match(valor):
        raise ValueError("Email con formato invalido")
    return valor


class SuscripcionCreate(BaseModel):
    email: str

    _email = field_validator("email")(validar_email)


class SuscripcionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    creada_en: datetime
