from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Función que comprueba el login correcto
def test_login_success():
    response = client.post("/login", data={
        "username": "jaume.example@example.com",
        "password": "12345678"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Función que comprueba contraseña incorrecta con usuario que puede existir o no
def test_login_invalid_password():
    data = {
        "username": "jaume.example@example.com",
        "password": "wrongPassword"
    }

    response = client.post("/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "User not found or invalid credentials"