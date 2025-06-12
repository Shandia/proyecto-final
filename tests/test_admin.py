from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import crud, schemas

client = TestClient(app)

# Datos Admin por defecto
admin_email = "admin@example.com"
admin_password = "admin123"

# Datos para test de new user
test_user_data = {
    "email": "nuevo@example.com",
    "password": "test12345",
    "first_name": "Nuevo",
    "last_name": "Usuario"
}

def get_admin_token():
    response = client.post("/login", data ={
        "username": admin_email,
        "password": admin_password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def get_non_admin_token():
    # Registramos un nuevo usuario
    response = client.post("/register", json={
        "email": "normal@example.com",
        "password": "normal123",
        "first_name": "Normal",
        "last_name": "User"
    })
    assert response.status_code == 200

def test_admin_can_create_user():
    token = get_admin_token()
    response = client.post("/admin/create-user", json=test_user_data, headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == test_user_data["email"]

def test_non_admin_cannot_view_users():
    token = get_non_admin_token()
    response = client.get("/users", header={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_non_admin_cannot_create_user():
    token = get_non_admin_token()
    response = client.post("/admin/create-user", json={
        "email": "otro@example.com",
        "password": "otro123",
        "first_name": "Otro",
        "last_name": "Usuario"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403