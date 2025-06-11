from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    # Datos para el testing inicial
    user_data = {
        "email": "jaume.example@example.com",
        "password": "12345678",
        "first_name": "Jaume",
        "last_name": "Florit"
    }

    # Petición POST dirigida al ENDPOINT /register
    response = client.post("/register", json=user_data)

    # Comprobaciones iniciales
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["is_admin"] is False
    assert "id" in data

def test_register_duplicate_email():
    # Misma petición con el mismo email que antes
    user_data = {
        "email": "jaume.example@example.com",
        "password": "12345678",
        "first_name": "Jaume",
        "last_name": "Florit"
    }

    # Tendríamos que obtener un error al entrar email duplicado
    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered, try another or log in"