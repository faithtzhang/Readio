from fastapi import FastAPI
from app.api.router import router

app = FastAPI(title="Readio")
app.include_router(router)