from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.dtos.suscripcion_dto import validar_email


class Credenciales(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=100)

    _email = field_validator("email")(validar_email)


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"
