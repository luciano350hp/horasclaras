from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import crear_cliente_payload


def _escenario(client: TestClient) -> tuple[int, int]:
    h = client.post(
        "/api/clientes/",
        json=crear_cliente_payload("Escuela", tipo="hora", tarifa="30.00", descuento_repeticion="0"),
    ).json()["id"]
    p = client.post(
        "/api/clientes/", json=crear_cliente_payload("Editorial", tarifa="0.10", descuento_repeticion="50")
    ).json()["id"]
    for minutos, tipo in [(90, "facturable"), (30, "facturable"), (60, "planificacion")]:
        client.post("/api/horas/", json={"cliente_id": h, "fecha": "2026-05-10", "minutos": minutos, "tipo": tipo})
    client.post("/api/horas/", json={"cliente_id": h, "fecha": "2026-06-01", "minutos": 600, "tipo": "facturable"})
    client.post(
        "/api/traducciones/",
        json={"cliente_id": p, "fecha": "2026-05-20", "palabras_totales": 1000, "palabras_repetidas": 400},
    )
    return h, p


def test_calculo_mensual(client: TestClient) -> None:
    _escenario(client)
    cuerpo = client.get("/api/calculos/2026-05").json()
    por_nombre = {f["cliente"]: f for f in cuerpo["clientes"]}
    # 120 min facturables = 2 h x 30 = 60. La planificacion no se cobra.
    assert Decimal(por_nombre["Escuela"]["monto"]) == Decimal("60.00")
    assert por_nombre["Escuela"]["minutos_no_facturables"] == 60
    # 600 nuevas x 0.10 + 400 repetidas x 0.10 x 0.5 = 60 + 20 = 80
    assert Decimal(por_nombre["Editorial"]["monto"]) == Decimal("80.00")
    assert Decimal(cuerpo["total"]) == Decimal("140.00")


def test_mes_sin_datos_da_cero(client: TestClient) -> None:
    _escenario(client)
    assert Decimal(client.get("/api/calculos/2025-01").json()["total"]) == Decimal("0.00")


def test_filtrar_por_cliente(client: TestClient) -> None:
    h, _ = _escenario(client)
    cuerpo = client.get(f"/api/calculos/2026-05?cliente_id={h}").json()
    assert len(cuerpo["clientes"]) == 1


def test_mes_invalido_422(client: TestClient) -> None:
    assert client.get("/api/calculos/2026-13").status_code == 422
    assert client.get("/api/calculos/mayo").status_code == 422


def test_cliente_inexistente_404(client: TestClient) -> None:
    assert client.get("/api/calculos/2026-05?cliente_id=99").status_code == 404


def test_dashboard(client: TestClient) -> None:
    _escenario(client)
    d = client.get("/api/dashboard/2026-05").json()
    assert Decimal(d["total_facturado"]) == Decimal("140.00")
    assert Decimal(d["horas_facturables"]) == Decimal("2.00")
    assert Decimal(d["horas_no_facturables"]) == Decimal("1.00")
    assert d["palabras_traducidas"] == 1000
    assert d["cantidad_clientes_activos"] == 2
    assert d["mejor_cliente"] == "Editorial"


def test_dashboard_vacio(client: TestClient) -> None:
    d = client.get("/api/dashboard/2026-05").json()
    assert d["mejor_cliente"] is None and Decimal(d["total_facturado"]) == 0
