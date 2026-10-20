from fastapi.testclient import TestClient

from tests.conftest import crear_cliente_payload


def _crear_cliente_hora(client: TestClient, nombre: str = "Clases de Ingles") -> int:
    payload = crear_cliente_payload(nombre, tipo="hora", tarifa="25.00", descuento_repeticion="0.00")
    respuesta = client.post("/api/clientes/", json=payload)
    assert respuesta.status_code == 201
    return respuesta.json()["id"]


def _payload_hora(cliente_id: int, **overrides) -> dict:
    payload = {
        "cliente_id": cliente_id,
        "fecha": "2026-05-10",
        "minutos": 60,
        "tipo": "facturable",
    }
    payload.update(overrides)
    return payload


def test_crear_hora(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)

    respuesta = client.post("/api/horas/", json=_payload_hora(cliente_id))

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["cliente_id"] == cliente_id
    assert cuerpo["fecha"] == "2026-05-10"
    assert cuerpo["minutos"] == 60
    assert cuerpo["tipo"] == "facturable"


def test_crear_hora_de_planificacion(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)

    respuesta = client.post(
        "/api/horas/", json=_payload_hora(cliente_id, tipo="planificacion")
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["tipo"] == "planificacion"


def test_crear_hora_con_cliente_inexistente_devuelve_404(client: TestClient) -> None:
    respuesta = client.post("/api/horas/", json=_payload_hora(999))

    assert respuesta.status_code == 404
    assert client.get("/api/horas/").json() == []


def test_crear_hora_con_cliente_palabra_devuelve_422(client: TestClient) -> None:
    cliente = client.post("/api/clientes/", json=crear_cliente_payload()).json()

    respuesta = client.post("/api/horas/", json=_payload_hora(cliente["id"]))

    assert respuesta.status_code == 422
    assert client.get("/api/horas/").json() == []


def test_crear_hora_con_minutos_en_cero_devuelve_422(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)

    respuesta = client.post("/api/horas/", json=_payload_hora(cliente_id, minutos=0))

    assert respuesta.status_code == 422


def test_crear_hora_con_minutos_negativos_devuelve_422(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)

    respuesta = client.post("/api/horas/", json=_payload_hora(cliente_id, minutos=-15))

    assert respuesta.status_code == 422


def test_crear_hora_con_minutos_no_enteros_devuelve_422(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)

    respuesta = client.post("/api/horas/", json=_payload_hora(cliente_id, minutos=90.5))

    assert respuesta.status_code == 422


def test_crear_hora_con_tipo_invalido_devuelve_422(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)

    respuesta = client.post("/api/horas/", json=_payload_hora(cliente_id, tipo="media"))

    assert respuesta.status_code == 422


def test_listar_horas(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)
    client.post("/api/horas/", json=_payload_hora(cliente_id))
    client.post("/api/horas/", json=_payload_hora(cliente_id, minutos=45))

    respuesta = client.get("/api/horas/")

    assert respuesta.status_code == 200
    assert [h["minutos"] for h in respuesta.json()] == [60, 45]


def test_listar_horas_filtrado_por_cliente(client: TestClient) -> None:
    primero = _crear_cliente_hora(client, "Clases A")
    segundo = _crear_cliente_hora(client, "Clases B")
    client.post("/api/horas/", json=_payload_hora(primero, minutos=30))
    client.post("/api/horas/", json=_payload_hora(segundo, minutos=90))

    respuesta = client.get(f"/api/horas/?cliente_id={primero}")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["minutos"] == 30


def test_obtener_hora(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)
    creado = client.post("/api/horas/", json=_payload_hora(cliente_id)).json()

    respuesta = client.get(f"/api/horas/{creado['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == creado["id"]


def test_obtener_hora_inexistente_devuelve_404(client: TestClient) -> None:
    respuesta = client.get("/api/horas/999")

    assert respuesta.status_code == 404


def test_eliminar_hora(client: TestClient) -> None:
    cliente_id = _crear_cliente_hora(client)
    creado = client.post("/api/horas/", json=_payload_hora(cliente_id)).json()

    respuesta = client.delete(f"/api/horas/{creado['id']}")

    assert respuesta.status_code == 204
    assert client.get(f"/api/horas/{creado['id']}").status_code == 404


def test_eliminar_hora_inexistente_devuelve_404(client: TestClient) -> None:
    respuesta = client.delete("/api/horas/999")

    assert respuesta.status_code == 404
