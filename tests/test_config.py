from pathlib import Path

from app.core.config import BASE_DIR, Settings


def test_ruta_relativa_se_ancla_a_base_dir() -> None:
    ajustes = Settings(database_url="sqlite:///./horasclaras.db")
    esperado = (BASE_DIR / "horasclaras.db").as_posix()

    assert ajustes.database_url_resuelta == f"sqlite:///{esperado}"


def test_ruta_relativa_sin_dot_se_ancla_a_base_dir() -> None:
    ajustes = Settings(database_url="sqlite:///data/horasclaras.db")
    esperado = (BASE_DIR / "data" / "horasclaras.db").as_posix()

    assert ajustes.database_url_resuelta == f"sqlite:///{esperado}"


def test_ruta_absoluta_se_deja_intacta() -> None:
    absoluta = (BASE_DIR / "ya_absoluta.db").as_posix()

    assert Settings(database_url=f"sqlite:///{absoluta}").database_url_resuelta == (
        f"sqlite:///{absoluta}"
    )


def test_url_no_sqlite_se_deja_intacta() -> None:
    url = "postgresql://user:pass@localhost:5432/horasclaras"

    assert Settings(database_url=url).database_url_resuelta == url


def test_sqlite_en_memoria_se_deja_intacto() -> None:
    assert Settings(database_url="sqlite://").database_url_resuelta == "sqlite://"


def test_url_resuelta_no_tiene_backslashes() -> None:
    resuelta = Settings(database_url="sqlite:///./horasclaras.db").database_url_resuelta

    assert "\\" not in resuelta


def test_url_resuelta_es_usable_por_sqlalchemy() -> None:
    from sqlalchemy import create_engine
    from sqlalchemy.engine import make_url

    from app.core.config import settings

    url = make_url(settings.database_url_resuelta)

    assert url.get_backend_name() == "sqlite"
    assert Path(str(url.database)).is_absolute()
    create_engine(settings.database_url_resuelta).dispose()
