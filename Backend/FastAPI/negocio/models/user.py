### User model ###

from pydantic import BaseModel

class User(BaseModel):
    uuid: str = None
    dni: int
    username: str
    saldo: float = 20000.0
