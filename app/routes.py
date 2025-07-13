from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd
from app import models, services

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
def draft_player(team_name: str, player_id: int, db: Session = Depends(get_db)):
  return services.assign_player_to_team(team_name, player_id, db)

