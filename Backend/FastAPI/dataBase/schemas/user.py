### Tabla usuario ###

def user_schema(user) -> dict:
    return {"uuid": str(user["uuid"]),
            "dni": str(user["dni"]),
            "username": user["username"],
            "saldo": user["saldo"]
            }