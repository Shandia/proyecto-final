from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función utilizada para evitar duplicados haciendo una búsqueda por email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Función utilizada para la creación de un nuevo usuario
def create_user(db: Session, user: schemas.UserCreate, is_admin: bool = False):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Función utilizada para hacer la validación de auth al login
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Función que devuelve todos los usuarios
def get_all_users(db: Session):
    return db.query(models.User).all()