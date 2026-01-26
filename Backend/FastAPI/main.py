from fastapi import FastAPI
from routers.blackjack.blackjack import router as blackjack_router

app = FastAPI()

app.include_router(blackjack_router)