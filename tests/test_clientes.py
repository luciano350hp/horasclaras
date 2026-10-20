from unittest.mock import patch

from fastapi.testclient import TestClient

from app.repositories.cliente_repository import ClienteRepository
from tests.conftest import crear_cliente_payload


def test_crear_cliente(client: TestClient) -> None:
    respuesta = client.post("/api/clientes/", json=crear_cliente_payload())

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Traducciones SA"
    assert cuerpo["tipo"] == "palabra"
    assert cuerpo["tarifa"] == "0.12"
    assert cuerpo["descuento_repeticion"] == "10.00"


def test_crear_cliente_por_hora(client: TestClient) -> None:
    respuesta = client.post(
        "/api/clientes/", json=crear_cliente_payload("Clases de Ingles", tipo="hora", tarifa="25.00")
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["tipo"] == "hora"


def test_nombre_duplicado_devuelve_409(client: TestClient) -> None:
    cliente = crear_cliente_payload()
    assert client.post("/api/clientes/", json=cliente).status_code == 201

    repetido = crear_cliente_payload(descuento_repeticion="0.00")
    respuesta = client.post("/api/clientes/", json=repetido)

    assert respuesta.status_code == 409


def test_duplicado_por_carrera_devuelve_409(client: TestClient) -> None:
    assert client.post("/api/clientes/", json=crear_cliente_payload()).status_code == 201

    # Simula el TOCTOU: el chequeo previo pasa limpio y el INSERT choca con el UNIQUE.
    with patch.object(ClienteRepository, "obtener_por_nombre", return_value=None):
        respuesta = client.post(
            "/api/clientes/", json=crear_cliente_payload(descuento_repeticion="0.00")
        )

    assert respuesta.status_code == 409
    assert len(client.get("/api/clientes/").json()) == 1


def test_duplicado_por_carrera_en_patch_devuelve_409(client: TestClient) -> None:
    assert client.post("/api/clientes/", json=crear_cliente_payload("Cliente A")).status_code == 201
    segundo = client.post("/api/clientes/", json=crear_cliente_payload("Cliente B")).json()

    with patch.object(ClienteRepository, "obtener_por_nombre", return_value=None):
        respuesta = client.patch(f"/api/clientes/{segundo['id']}", json={"nombre": "Cliente A"})

    assert respuesta.status_code == 409
    assert client.get(f"/api/clientes/{segundo['id']}").json()["nombre"] == "Cliente B"


def test_nombre_se_normaliza(client: TestClient) -> None:
    respuesta = client.post("/api/clientes/", json=crear_cliente_payload("  Escuela Norte  "))

    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "Escuela Norte"


def test_nombre_solo_espacios_devuelve_422(client: TestClient) -> None:
    respuesta = client.post("/api/clientes/", json=crear_cliente_payload("   "))

    assert respuesta.status_code == 422


def test_nombre_solo_espacios_no_persiste_fila(client: TestClient) -> None:
    client.post("/api/clientes/", json=crear_cliente_payload("   "))

    assert client.get("/api/clientes/").json() == []


def test_patch_nombre_solo_espacios_devuelve_422(client: TestClient) -> None:
    creado = client.post("/api/clientes/", json=crear_cliente_payload()).json()

    respuesta = client.patch(f"/api/clientes/{creado['id']}", json={"nombre": "   "})

    assert respuesta.status_code == 422
    assert client.get(f"/api/clientes/{creado['id']}").json()["nombre"] == "Traducciones SA"


def test_listar_clientes(client: TestClient) -> None:
    client.post("/api/clientes/", json=crear_cliente_payload("Cliente A"))
    client.post("/api/clientes/", json=crear_cliente_payload("Cliente B", tipo="hora"))

    respuesta = client.get("/api/clientes/")

    assert respuesta.status_code == 200
    assert [c["nombre"] for c in respuesta.json()] == ["Cliente A", "Cliente B"]


def test_obtener_cliente_inexistente_devuelve_404(client: TestClient) -> None:
    respuesta = client.get("/api/clientes/999")

    assert respuesta.status_code == 404


def test_actualizar_cliente_parcial(client: TestClient) -> None:
    creado = client.post("/api/clientes/", json=crear_cliente_payload()).json()

    respuesta = client.patch(f"/api/clientes/{creado['id']}", json={"tarifa": "0.15"})

    assert respuesta.status_code == 200
    assert respuesta.json()["tarifa"] == "0.15"
    assert respuesta.json()["nombre"] == "Traducciones SA"


def test_actualizar_cliente_a_nombre_duplicado_devuelve_409(client: TestClient) -> None:
    client.post("/api/clientes/", json=crear_cliente_payload("Cliente A"))
    segundo = client.post("/api/clientes/", json=crear_cliente_payload("Cliente B")).json()

    respuesta = client.patch(f"/api/clientes/{segundo['id']}", json={"nombre": "Cliente A"})

    assert respuesta.status_code == 409


def test_actualizar_cliente_inexistente_devuelve_404(client: TestClient) -> None:
    respuesta = client.patch("/api/clientes/999", json={"tarifa": "1.00"})

    assert respuesta.status_code == 404


def test_eliminar_cliente(client: TestClient) -> None:
    creado = client.post("/api/clientes/", json=crear_cliente_payload()).json()

    respuesta = client.delete(f"/api/clientes/{creado['id']}")
    despues = client.get(f"/api/clientes/{creado['id']}")

    assert respuesta.status_code == 204
    assert despues.status_code == 404


def test_eliminar_cliente_inexistente_devuelve_404(client: TestClient) -> None:
    respuesta = client.delete("/api/clientes/999")

    assert respuesta.status_code == 404


def test_tipo_invalido_devuelve_422(client: TestClient) -> None:
    respuesta = client.post("/api/clientes/", json=crear_cliente_payload(tipo="frase"))

    assert respuesta.status_code == 422


def test_tarifa_negativa_devuelve_422(client: TestClient) -> None:
    respuesta = client.post("/api/clientes/", json=crear_cliente_payload(tarifa="-5.00"))

    assert respuesta.status_code == 422


def test_descuento_fuera_de_rango_devuelve_422(client: TestClient) -> None:
    respuesta = client.post(
        "/api/clientes/", json=crear_cliente_payload(descuento_repeticion="120.00")
    )

    assert respuesta.status_code == 422


def test_health(client: TestClient) -> None:
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}