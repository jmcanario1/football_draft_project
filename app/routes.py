from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd
from app import models, services
from pydantic import BaseModel

class DraftRequest(BaseModel):
  team_name: str
  player_id: int

router = APIRouter(
  prefix="/api",
  tags=["Draft"]
)

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
  return await services.process_csv(file, db)

@router.get("/grid")
def get_grid(db: Session = Depends(get_db)):
  return services.get_grid_data(db)

@router.post("/draft")
def draft_player(payload: DraftRequest, db: Session = Depends(get_db)):
  return services.assign_player_to_team(payload.team_name, payload.player_id, db)

@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    return services.get_teams(db)

@router.post("/reset-draft")
def reset_draft_endpoint(db: Session = Depends(get_db)):
    return services.reset_draft(db)
