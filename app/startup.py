# Archivo provisional en fase desarrollo para tener un usuario admin y verificar el funcionamiento de los endpoints

from app.database import SessionLocal
from app import models
from passlib.hash import bcrypt

def create_default_admin():
    db = SessionLocal()
    email = "admin@example.com"
    password = "admin1234"

    existing = db.query(models.User).filter(models.User.email == email).first()
    if not existing:
        admin = models.User(
            email=email,
            hashed_password=bcrypt.hash(password),
            first_name="Admin",
            last_name="User",
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("Admin creado: ", email)
    else:
        print("Admin ya existe: ", email)
    db.close()