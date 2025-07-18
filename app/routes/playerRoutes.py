from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services import playerServices
from database import get_db
from app.schemas import PlayerCreate


router = APIRouter(
  prefix="/player",
  tags=["Player"]
)

@router.post("/create-player")
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
  return playerServices.create_player(player, db)

@router.get("/get-player/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
  return playerServices.get_player(player_id, db)

@router.delete("/delete-player/{player_id}")
async def delete_player(player_id: int, db: Session = Depends(get_db)):
  return await playerServices.delete_player(player_id, db)

@router.post("/upload-player-image/{player_id}")
def upload_image(player_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return playerServices.upload_player_image(player_id, file, db)