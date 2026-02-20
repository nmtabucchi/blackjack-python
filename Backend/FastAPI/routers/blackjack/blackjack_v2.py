from fastapi import APIRouter, status
from uuid import uuid4
import random
from routers.dataBase.users_db import search_uuid

router = APIRouter(
    prefix="/v2/blackjack",
    tags=["Black Jack v2"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

#Version v2
#Se ejecuta una partida por usuario + base de datos

# Cartas
valores = {
    "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10
}

palos = ["Corazones", "Diamantes", "Tréboles", "Picas"]

# Memoria de partidas
partidas = {}

def calcular_puntos(cartas):
    #param cartas: son las cartas que estan la partida Jugador o Crupier 

    #Suma los puntos de todas las cartas
    total = sum(c["puntos"] for c in cartas)
    """
    # Equivale a:
    total = 0
    for c in cartas:
        total += c["puntos"]
    """

    #Cuenta cuántos Ases hay en la mano. Cada vez que encuentra un As: suma 1
    ases = sum(1 for c in cartas if c["valor"] == "A")
    """
    # Equivale a:
    ases = 0
    for c in cartas:
        if c["valor"] == "A":
            ases += 1
    """

    #Por cada As: resta 10 (11 → 1) hasta que no se pase de 21
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    
    return total

@router.post("/new-game")
async def new_game(dni: int):
    user_id = search_uuid(dni)
    
    mazo = [
        {"valor": v, "palo": p, "puntos": pts}
        #Recorre cada valor de carta:
        for v, pts in valores.items()
        #Por cada valor, recorre cada palo.
        for p in palos
    ]

    """
    #random.shuffle: cambia el orden de los elementos de una lista
    """
    random.shuffle(mazo)

    partidas[user_id] = {
        "mazo": mazo,
        "jugador": [],
        "crupier": [],
        "estado": "jugando"
    }

    return {
        "user_id": user_id,
        "mensaje": "Partida creada"
    }

@router.post("/hit/{user_id}")
#Solicita carta
async def hit(user_id: str):
    partida = partidas.get(user_id)

    if not partida:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    puntos_i = calcular_puntos(partida["jugador"])
    if puntos_i == 21:
        return {
            "mensaje": "No se puede solicitar más cartas"         
        }

    carta = partida["mazo"].pop()
    partida["jugador"].append(carta)

    puntos = calcular_puntos(partida["jugador"])

    if puntos > 21:
        partida["estado"] = "bust"
        return{
            "mensaje": "Jugador se pasó",
            "puntos": puntos,
            "cartas": partida["jugador"]            
        }

    return {
        "puntos": puntos,
        "carta": partida["jugador"]        
    }

@router.post("/stand/{user_id}")
#Plantarse
async def stand(user_id: str):
    partida = partidas.get(user_id)

    if not partida:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    if (partida["estado"] != "jugando"):
        return {
            "mensaje": "Jugador se pasó"
        }

    while calcular_puntos(partida["crupier"]) < 17:
        partida["crupier"].append(partida["mazo"].pop())

    puntos_jugador = calcular_puntos(partida["jugador"])
    puntos_crupier = calcular_puntos(partida["crupier"])

    if(puntos_crupier > 21 or puntos_jugador > puntos_crupier):
        resultado = "Jugador gana"
    elif puntos_jugador == puntos_crupier:
        resultado = "Empate"
    else:
        resultado = "Crupier gana"

    partida["estado"] = "finalizada"

    return {
        "resultado": resultado,
        "jugador": {
            "puntos": puntos_jugador,
            "cartas": partida["jugador"]            
        },
        "crupier": {
            "puntos": puntos_crupier,
            "cartas": partida["crupier"]            
        }        
    }