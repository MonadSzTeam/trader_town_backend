from fastapi import FastAPI

from app.api import api_router


app = FastAPI(title="Trader Town Backend")

app.include_router(api_router)

