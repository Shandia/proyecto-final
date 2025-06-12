from fastapi.testclient import TestClient
from app.main import app

client = Testclient(app)

# Función que comprueba el login correcto
def test_login_success():
    response = client.post("/login", data={
        "username": "jaume.example@example.com",
        "password:": "12345678"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Función que comprueba contraseña incorrecta con usuario existente
def test_login_invalid_password():
    data = {
        "username": "jaume.example@example.com",
        "password": "wrongPassword"
    }

    response = client.post("/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

# Función que comprueba un login de un usuario que no existe
def test_login_nonexistent_user():
    data = {
        "username": "noexist@example.com",
        "password": "noexiste"
    }

    response = client.post("/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "User doesnt exist"