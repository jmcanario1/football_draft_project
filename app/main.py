from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.draftRoutes import router as draft_router
from app.routes.playerRoutes import router as player_router
from app.routes.teamRoutes import router as team_router
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(draft_router)
app.include_router(player_router)
app.include_router(team_router)