from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Definición del motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Generamos la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para definir modelos
Base = declarative_base()