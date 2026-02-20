### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from negocio.models.user import User
from negocio.dto.user_dto import UserResponseDTO
from dataBase.client import db_client
from dataBase.schemas.user import user_schema
from uuid import uuid4

router = APIRouter(prefix="/user", tags=["Usuarios"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

def search_user(field: str, key) -> UserResponseDTO | None:
    try:
        user = db_client.users.find_one({field: key})
        user_data = user_schema(user)
        return UserResponseDTO(**user_data)
    except:
        return {"error": "Usuario no existe"}

def search_uuid(key):
    user = db_client.users.find_one({"dni": key})
    if not user:
        return {"error": "Usuario no existe"}
    return user.get("uuid")

@router.post("/new-user", response_model=User, status_code=status.HTTP_201_CREATED)
async def new_user(user: User):
    if type(search_user("dni", user.dni)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario ya existe")

    user_dict = dict(user)
    user_dict["uuid"] = str(uuid4())

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

@router.get("/info-user")
async def get_user(dni: int) -> UserResponseDTO | None:
    return search_user("dni", dni)