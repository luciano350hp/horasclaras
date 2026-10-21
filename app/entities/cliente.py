from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TipoCliente(str, Enum):
    HORA = "hora"
    PALABRA = "palabra"


class Cliente(Base):
    __tablename__ = "clientes"
    __table_args__ = (
        CheckConstraint("descuento_repeticion >= 0", name="ck_clientes_descuento_no_negativo"),
        CheckConstraint("descuento_repeticion <= 100", name="ck_clientes_descuento_maximo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    tipo: Mapped[TipoCliente] = mapped_column(nullable=False)
    tarifa: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descuento_repeticion: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=Decimal("50.00")
    )