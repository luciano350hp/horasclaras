from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = f"sqlite:///{BASE_DIR / 'horasclaras.db'}"

    @property
    def database_url_resuelta(self) -> str:
        """Ancla las rutas SQLite relativas a BASE_DIR, no al cwd.

        "sqlite:///./x.db" y "sqlite:////abs/x.db" no se distinguen por numero de
        barras: la diferencia es si el path es absoluto. as_posix() porque en
        Windows str(Path) devuelve backslashes y SQLite no los acepta en la URL.
        """
        url = self.database_url
        if not url.startswith("sqlite:///"):
            return url
        ruta = Path(url.removeprefix("sqlite:///"))
        if not ruta.is_absolute():
            ruta = BASE_DIR / ruta
        return f"sqlite:///{ruta.as_posix()}"


settings = Settings()