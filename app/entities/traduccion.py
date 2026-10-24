from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Traduccion(Base):
    __tablename__ = "traducciones"
    __table_args__ = (
        CheckConstraint("palabras_totales > 0", name="ck_traducciones_totales_positivas"),
        CheckConstraint("palabras_repetidas >= 0", name="ck_traducciones_repetidas_no_negativas"),
        CheckConstraint(
            "palabras_repetidas <= palabras_totales", name="ck_traducciones_repetidas_le_totales"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    palabras_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    palabras_repetidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
