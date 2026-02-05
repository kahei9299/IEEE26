from fastapi import FastAPI
from app.api.ws import router as ws_router

app = FastAPI(title="SignCall Overlay Backend")
app.include_router(ws_router)
