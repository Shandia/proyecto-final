# Inicialización de Repositorio incial
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

# Creación de las tablas en la base de datos si no existen, en nuestro caso User
Base.metadata.create_all(bind=engine)

# Instancia de la aplicación
app = FastAPI()

# Dependency para crear/cerrar la sesión de la BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Definición del ENDPOINT /register
@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered, try another or log in")
    return crud.create_user(db=db, user=user)