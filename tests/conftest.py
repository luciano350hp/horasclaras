from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.entities import cliente as _cliente  # noqa: F401
from app.entities import hora as _hora  # noqa: F401
from app.entities import mensaje_chat as _m, suscripcion as _s, traduccion as _t, usuario as _u  # noqa: F401
from app.main import app


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def crear_cliente_payload(nombre: str = "Traducciones SA", **overrides) -> dict:
    payload = {
        "nombre": nombre,
        "tipo": "palabra",
        "tarifa": "0.12",
        "descuento_repeticion": "10.00",
    }
    payload.update(overrides)
    return payload