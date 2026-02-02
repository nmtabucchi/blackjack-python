from fastapi import APIRouter, status
import random

router = APIRouter(
    prefix="/blackjack",
    tags=["blackjack"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

# Estructura de estado (memoria)
partida = {
    "mazo": [],
    "jugador": [],
    "crupier": [],
    "terminada": False
}

def crear_mazo():
    valores = {
        "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 10, "Q": 10, "K": 10
    }
    palos = ["Corazones", "Diamantes", "Tréboles", "Picas"]

    return [
        {"valor": v, "palo": p, "puntos": pts}
        #Recorre cada valor de carta:
        for v, pts in valores.items()
        #Por cada valor, recorre cada palo.
        for p in palos
    ]

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

@router.get("/repartir")
async def repartir():
    partida["mazo"] = crear_mazo()
    """
    random.shuffle: cambia el orden de los elementos de una lista
    """
    random.shuffle(partida["mazo"])

    partida["jugador"] = [partida["mazo"].pop(), partida["mazo"].pop()]
    partida["crupier"] = [partida["mazo"].pop()]
    partida["terminada"] = False

    return {
        "jugador": {
            "cartas": partida["jugador"],
            "puntos": calcular_puntos(partida["jugador"])
        },
        "crupier": {
            "cartas": partida["crupier"],
            "puntos": calcular_puntos(partida["crupier"])
        }
    }

@router.get("/solicitar_carta")
async def solicitar_carta():
    if partida["terminada"]:
        return {"error": "La partida ya terminó"}    

    carta = partida["mazo"].pop()
    partida["jugador"].append(carta)

    puntos = calcular_puntos(partida["jugador"])

    if puntos > 21:
        partida["terminada"] = True
        return {
            "mensaje": "Jugador se pasó",
            "cartas": partida["jugador"],
            "puntos": puntos
        }

    return {
        "cartas": partida["jugador"],
        "puntos": puntos
    }

@router.get("/detener")
async def detener():
    partida["terminada"] = True

    # Crupier reparte hasta 17 o más
    while calcular_puntos(partida["crupier"]) < 17:
        partida["crupier"].append(partida["mazo"].pop())

    puntos_jugador = calcular_puntos(partida["jugador"])
    puntos_crupier = calcular_puntos(partida["crupier"])

    if puntos_crupier > 21 or puntos_jugador > puntos_crupier:
        resultado = "Jugador gana"
    elif puntos_jugador < puntos_crupier:
        resultado = "Crupier gana"
    else:
        resultado = "Empate"

    return {
        "resultado": resultado,
        "jugador": {
            "cartas": partida["jugador"],
            "puntos": puntos_jugador
        },
        "crupier": {
            "cartas": partida["crupier"],
            "puntos": puntos_crupier
        }
    }