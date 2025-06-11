# Este archivo define cómo deben estar los datos que se reciben y se devuelven en la API.
from pydantic import BaseModel

# Se utiliza para validar lo que el cliente envía al registrarse.
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

# Se utiliza para devolver datos del usuario sin mostrar la contraseña.
class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_admin: bool

    class Config:
        from_attributes = True
    