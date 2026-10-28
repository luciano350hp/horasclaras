from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.auth_controller import router as auth_router
from app.controllers.calculo_controller import router as calculo_router
from app.controllers.presupuesto_controller import router as presupuesto_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.cliente_controller import router as cliente_router
from app.controllers.hora_controller import router as hora_router
from app.controllers.suscripcion_controller import router as suscripcion_router
from app.controllers.tarifario_controller import router as tarifario_router
from app.controllers.traduccion_controller import router as traduccion_router
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    from app.entities import cliente as _cliente  # noqa: F401
    from app.entities import hora as _hora  # noqa: F401

    from app.entities import mensaje_chat as _m, suscripcion as _s, traduccion as _t, usuario as _u  # noqa: F401

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="HorasClaras",
    description="Gestion de horas y tarifas para profesionales freelance",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente_router)
app.include_router(hora_router)
app.include_router(traduccion_router)
app.include_router(calculo_router)
app.include_router(presupuesto_router)
app.include_router(tarifario_router)
app.include_router(suscripcion_router)
app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    return {"estado": "ok"}