from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    mensaje: str = Field(min_length=1, max_length=1000)
    conversation_id: str | None = Field(default=None, max_length=64)


class ChatResponse(BaseModel):
    conversation_id: str
    respuesta: str
    fuentes: list[str]


class MensajeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rol: str
    contenido: str
