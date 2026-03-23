from fastapi import FastAPI
from Backend.FastAPI.routers.blackjack.blackjack_v1 import router as blackjack_v1_router
from Backend.FastAPI.routers.blackjack.blackjack_v2 import router as blackjack_v2_router
from Backend.FastAPI.routers.dataBase.users_db import router as users_db

app = FastAPI()

app.include_router(blackjack_v1_router)
app.include_router(blackjack_v2_router)
app.include_router(users_db)