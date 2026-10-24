from fastapi.testclient import TestClient

CRED = {"email": "luciano@mail.com", "password": "secreto123"}


def test_registro_y_login(client: TestClient) -> None:
    assert client.post("/api/auth/registro", json=CRED).status_code == 201
    r = client.post("/api/auth/login", json=CRED)
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["email"] == "luciano@mail.com"


def test_no_devuelve_password(client: TestClient) -> None:
    assert "password" not in client.post("/api/auth/registro", json=CRED).json()


def test_registro_duplicado_409(client: TestClient) -> None:
    client.post("/api/auth/registro", json=CRED)
    assert client.post("/api/auth/registro", json=CRED).status_code == 409


def test_login_incorrecto_401(client: TestClient) -> None:
    client.post("/api/auth/registro", json=CRED)
    assert client.post("/api/auth/login", json={**CRED, "password": "otraotra"}).status_code == 401
    assert client.post("/api/auth/login", json={"email": "x@y.com", "password": "secreto123"}).status_code == 401


def test_password_corta_422(client: TestClient) -> None:
    assert client.post("/api/auth/registro", json={**CRED, "password": "123"}).status_code == 422


def test_me_sin_token_o_falso_401(client: TestClient) -> None:
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer falso"}).status_code == 401
