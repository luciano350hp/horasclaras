from fastapi.testclient import TestClient

from tests.conftest import crear_cliente_payload


def _cliente_palabra(client: TestClient, **kw) -> int:
    return client.post("/api/clientes/", json=crear_cliente_payload(**kw)).json()["id"]


def _payload(cid: int, **kw) -> dict:
    p = {"cliente_id": cid, "fecha": "2026-05-10", "palabras_totales": 1000, "palabras_repetidas": 200}
    p.update(kw)
    return p


def test_crear_traduccion(client: TestClient) -> None:
    cid = _cliente_palabra(client)
    r = client.post("/api/traducciones/", json=_payload(cid))
    assert r.status_code == 201
    assert r.json()["palabras_repetidas"] == 200


def test_repetidas_mayores_que_totales_422(client: TestClient) -> None:
    cid = _cliente_palabra(client)
    r = client.post("/api/traducciones/", json=_payload(cid, palabras_repetidas=1001))
    assert r.status_code == 422


def test_cliente_inexistente_404(client: TestClient) -> None:
    assert client.post("/api/traducciones/", json=_payload(99)).status_code == 404


def test_cliente_por_hora_422(client: TestClient) -> None:
    cid = _cliente_palabra(client, nombre="Escuela", tipo="hora", tarifa="20.00")
    assert client.post("/api/traducciones/", json=_payload(cid)).status_code == 422


def test_listar_obtener_eliminar(client: TestClient) -> None:
    cid = _cliente_palabra(client)
    tid = client.post("/api/traducciones/", json=_payload(cid)).json()["id"]
    assert len(client.get("/api/traducciones/").json()) == 1
    assert client.get(f"/api/traducciones/{tid}").status_code == 200
    assert client.delete(f"/api/traducciones/{tid}").status_code == 204
    assert client.get(f"/api/traducciones/{tid}").status_code == 404
