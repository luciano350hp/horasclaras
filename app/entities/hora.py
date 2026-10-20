from datetime import date
from enum import Enum

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TipoHora(str, Enum):
    FACTURABLE = "facturable"
    PLANIFICACION = "planificacion"


class Hora(Base):
    __tablename__ = "horas"
    __table_args__ = (
        CheckConstraint("minutos > 0", name="ck_horas_minutos_positivos"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[TipoHora] = mapped_column(String(12), nullable=False)
    observacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
