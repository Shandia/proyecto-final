from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from .auth import get_current_user, require_admin
from .startup import create_default_admin

from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Creación de las tablas en la base de datos si no existen, en nuestro caso User
Base.metadata.create_all(bind=engine)

# Creación de un usuario default admin para hacer pruebas en fase de desarrollo
create_default_admin()

# Instancia de la aplicación
app = FastAPI()

# Dependency para crear/cerrar la sesión de la BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINT: Registro de usuario
@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered, try another or log in")
    return crud.create_user(db=db, user=user)

# ENDPOINT: Login de usuario
@app.post("/login", response_model=schemas.TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="User not found or invalid credentials")
    
    # Generamos JWT
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user.email, "exp": expire}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}

# ENDPOINT: Obtener todos los usuarios (rol: admin)
@app.get("/users", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(require_admin)):
    return db.query(models.User).all()

# ENDPOINT: Crear usuarios desde el panel administrador
@app.post("/admin/create-user", response_model=schemas.UserOut)
def admin_create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)