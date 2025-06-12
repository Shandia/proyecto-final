# Este archivo define cómo deben estar los datos que se reciben y se devuelven en la API.
from pydantic import BaseModel, EmailStr

# Entrada de registro
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

# Respuesta de salida de usuario
class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_admin: bool

    class Config:
        from_attributes = True

# Entrada de login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Respuesta de login con Token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"