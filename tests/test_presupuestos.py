from decimal import Decimal

from fastapi.testclient import TestClient

from app.services.presupuesto_service import analizar, contar_palabras
from tests.conftest import crear_cliente_payload


def _cliente(client: TestClient, **kw) -> int:
    return client.post("/api/clientes/", json=crear_cliente_payload(**kw)).json()["id"]


def _presupuesto(client: TestClient, cid: int, texto: str):
    return client.post("/api/presupuestos", json={"texto": texto, "cliente_id": cid})


def test_contar_palabras_ignora_puntuacion() -> None:
    assert contar_palabras("Hola, mundo! Don't stop... 2026") == 5


def test_analizar_detecta_frase_repetida_sin_importar_mayusculas() -> None:
    totales, repetidas, segmentos = analizar("Hola mundo. hola   MUNDO. Adios.")
    assert (totales, repetidas) == (5, 2)
    assert segmentos == ["hola   MUNDO."]


def test_presupuesto_sin_repeticiones(client: TestClient) -> None:
    cid = _cliente(client)
    r = _presupuesto(client, cid, "uno dos tres")
    assert r.status_code == 200
    d = r.json()
    assert d["palabras_totales"] == 3 and d["palabras_repetidas"] == 0
    assert Decimal(d["monto"]) == Decimal("0.36")


def test_presupuesto_con_repeticion_aplica_descuento(client: TestClient) -> None:
    cid = _cliente(client)  # tarifa 0.12, descuento 10 %
    d = _presupuesto(client, cid, "Hola mundo. Hola mundo. Adios.").json()
    assert d["palabras_totales"] == 5
    assert d["palabras_repetidas"] == 2
    assert d["palabras_nuevas"] == 3
    assert Decimal(d["monto_sin_descuento"]) == Decimal("0.60")
    assert Decimal(d["monto"]) == Decimal("0.58")  # 3 x 0.12 + 2 x 0.12 x 0.9 = 0.576


def test_cliente_por_hora_422(client: TestClient) -> None:
    cid = _cliente(client, nombre="Escuela", tipo="hora", tarifa="25.00")
    assert _presupuesto(client, cid, "hola mundo").status_code == 422


def test_cliente_inexistente_404(client: TestClient) -> None:
    assert _presupuesto(client, 999, "hola").status_code == 404


def test_texto_vacio_422(client: TestClient) -> None:
    cid = _cliente(client)
    assert _presupuesto(client, cid, "   ").status_code == 422
    assert _presupuesto(client, cid, "... !!!").status_code == 422


def test_no_guarda_nada(client: TestClient) -> None:
    cid = _cliente(client)
    _presupuesto(client, cid, "hola mundo")
    assert client.get("/api/traducciones/").json() == []
