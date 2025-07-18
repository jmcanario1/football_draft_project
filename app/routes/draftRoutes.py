from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import draftServices
from database import get_db
from app.schemas import DraftRequest


router = APIRouter(
  prefix="/draft",
  tags=["Draft"]
)

@router.get("/grid")
def get_grid(db: Session = Depends(get_db)):
  return draftServices.get_grid_data(db)

@router.post("/draft")
def draft_player(payload: DraftRequest, db: Session = Depends(get_db)):
  return draftServices.assign_player_to_team(payload.team_name, payload.player_id, db)

@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    return draftServices.get_teams(db)

@router.post("/reset-draft")
def reset_draft_endpoint(db: Session = Depends(get_db)):
    return draftServices.reset_draft(db)