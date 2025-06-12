from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import crud, schemas, models
import uuid

client = TestClient(app)

# Crear admin si no existe
def ensure_admin_user():
    db = SessionLocal()
    email = "admin@example.com"
    user = crud.get_user_by_email(db, email)
    if not user:
        user_data = schemas.UserCreate(
            email=email,
            password="admin123",
            first_name="Admin",
            last_name="User"
        )
        crud.create_user(db, user_data, is_admin=True)
    db.close()

# Genera un token para el admin
def get_admin_token():
    ensure_admin_user()
    response = client.post("/login", data={
        "username": "admin@example.com",
        "password": "admin123"
    })
    print("Admin login:", response.status_code, response.json())
    assert response.status_code == 200
    return response.json()["access_token"]

# Genera usuario normal y token
def get_non_admin_token():
    email = f"normal_{uuid.uuid4().hex}@example.com"
    response = client.post("/register", json={
        "email": email,
        "password": "normal123",
        "first_name": "Normal",
        "last_name": "User"
    })
    print("Register non-admin:", response.status_code, response.json())
    assert response.status_code == 200

    response = client.post("/login", data={
        "username": email,
        "password": "normal123"
    })
    print("Login non-admin:", response.status_code, response.json())
    assert response.status_code == 200
    return response.json()["access_token"]

# Función que comprueba si el usuario Admin puede usar el ENDPOINT /admin/create-user
def test_admin_can_create_user():
    token = get_admin_token()
    email = f"nuevo_{uuid.uuid4().hex}@example.com"
    response = client.post("/admin/create-user", json={
        "email": email,
        "password": "test12345",
        "first_name": "Nuevo",
        "last_name": "Usuario"
    }, headers={"Authorization": f"Bearer {token}"})
    print("Admin create user:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["email"] == email

# Función que comprueba que no podemos acceder al ENDPOINT /users sin ser admin
def test_non_admin_cannot_view_users():
    token = get_non_admin_token()
    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    print("Non-admin view users:", response.status_code)
    assert response.status_code == 403

# Función que comprueba que no podemos crear usuarios ni acceder a /admin/create-user sin admin
def test_non_admin_cannot_create_user():
    token = get_non_admin_token()
    email = f"otro_{uuid.uuid4().hex}@example.com"
    response = client.post("/admin/create-user", json={
        "email": email,
        "password": "otro123",
        "first_name": "Otro",
        "last_name": "Usuario"
    }, headers={"Authorization": f"Bearer {token}"})
    print("Non-admin create user:", response.status_code)
    assert response.status_code == 403
