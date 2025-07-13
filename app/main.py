from fastapi import FastAPI
from app.routes import router as draft_router

app = FastAPI()

app.include_router(draft_router)