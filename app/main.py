from fastapi import FastAPI
from app.api.prices import router as prices_router

app = FastAPI(title="Crypto Price API")
app.include_router(prices_router)