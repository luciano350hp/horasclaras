from fastapi.testclient import TestClient

from tests.conftest import crear_cliente_payload


def test_pdf_con_clientes(client: TestClient) -> None:
    client.post("/api/clientes/", json=crear_cliente_payload())
    r = client.get("/api/tarifario/pdf?profesional=Luciano")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content.startswith(b"%PDF")


def test_pdf_sin_clientes(client: TestClient) -> None:
    assert client.get("/api/tarifario/pdf").content.startswith(b"%PDF")
