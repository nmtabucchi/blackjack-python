from fastapi import FastAPI
from routers.blackjack.blackjack_v1 import router as blackjack_v1_router
from routers.blackjack.blackjack_v2 import router as blackjack_v2_router
from routers.dataBase.users_db import router as users_db

app = FastAPI()

app.include_router(blackjack_v1_router)
app.include_router(blackjack_v2_router)
app.include_router(users_db)