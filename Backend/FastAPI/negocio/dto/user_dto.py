### User DTO ###

from pydantic import BaseModel

class UserResponseDTO(BaseModel):
    dni: int
    saldo: float