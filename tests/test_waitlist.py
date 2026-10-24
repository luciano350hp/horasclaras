from fastapi.testclient import TestClient


def test_anotarse_ok(client: TestClient) -> None:
    r = client.post("/api/waitlist", json={"email": "Ana@Mail.com "})
    assert r.status_code == 201
    assert r.json()["email"] == "ana@mail.com"


def test_email_invalido_422(client: TestClient) -> None:
    assert client.post("/api/waitlist", json={"email": "no-es-email"}).status_code == 422


def test_email_duplicado_409(client: TestClient) -> None:
    client.post("/api/waitlist", json={"email": "ana@mail.com"})
    assert client.post("/api/waitlist", json={"email": "ANA@mail.com"}).status_code == 409


def test_listar(client: TestClient) -> None:
    client.post("/api/waitlist", json={"email": "a@b.com"})
    assert len(client.get("/api/waitlist").json()) == 1
