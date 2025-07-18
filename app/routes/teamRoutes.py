from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services import teamServices
from database import get_db
from app.schemas import TeamCreate


router = APIRouter(
  prefix="/team",
  tags=["Team"]
)

@router.post("/create-team")
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
  return teamServices.create_team(team, db)

@router.get("/get-team/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
  return teamServices.get_team(team_id, db)

@router.delete("/delete-team/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
  return teamServices.delete_team(team_id, db)

@router.post("/upload-team-image/{team_id}")
def upload_team_image(team_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
  return teamServices.upload_team_image(team_id, file, db)