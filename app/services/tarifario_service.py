from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.orm import Session

from app.repositories.cliente_repository import ClienteRepository


class TarifarioService:
    def __init__(self) -> None:
        self.clientes = ClienteRepository()

    def generar_pdf(self, db: Session, nombre_profesional: str = "") -> bytes:
        """Genera el tarifario en memoria. No se guarda en disco ni en la base."""
        estilos = getSampleStyleSheet()
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, title="Tarifario")
        elementos = [Paragraph("Tarifario", estilos["Title"])]
        if nombre_profesional:
            elementos.append(Paragraph(nombre_profesional, estilos["Normal"]))
        elementos.append(Spacer(1, 16))

        filas = [["Cliente", "Modalidad", "Tarifa", "Desc. repeticion"]]
        for c in self.clientes.listar(db, skip=0, limit=1000):
            if c.tipo.value == "hora":
                filas.append([c.nombre, "Por hora", f"$ {c.tarifa:.2f} / hora", "-"])
            else:
                filas.append(
                    [c.nombre, "Por palabra", f"$ {c.tarifa:.2f} / palabra", f"{c.descuento_repeticion:.0f} %"]
                )
        if len(filas) == 1:
            filas.append(["(sin clientes cargados)", "", "", ""])
        tabla = Table(filas, colWidths=[180, 90, 110, 90], repeatRows=1)
        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f8")]),
                ]
            )
        )
        elementos.append(tabla)
        doc.build(elementos)
        return buffer.getvalue()
