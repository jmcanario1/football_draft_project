from app import models
from sqlalchemy.orm import Session
from app.schemas import PlayerCreate
from fastapi import UploadFile
import uuid
import os


def create_player(player: PlayerCreate, db: Session):
  new_player = models.Player(
    name=player.name,
    pot=player.pot,
    position=player.position,
    image=player.image
  )
  db.add(new_player)
  db.commit()
  return {"message": "Player created successfully"}


def get_player(player_id: int, db: Session):
  player = db.query(models.Player).filter(models.Player.id == player_id).first()
  if player:
    return {
      "id": player.id,
      "name": player.name,
      "pot": player.pot,
      "position": player.position,
      "image": player.image
    }
  return {"error": "Player not found"}


async def delete_player(player_id: int, db: Session):
  player = db.query(models.Player).filter(models.Player.id == player_id).first()
  if player:
    db.delete(player)
    db.commit()
    return {"message": "Player deleted successfully"}
  return {"error": "Player not found"}


async def upload_player_image(player_id: int, file: UploadFile, db: Session):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        return {"error": "Player not found"}

    try:
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
        extension = file.filename.split(".")[-2].lower()
        if extension not in ALLOWED_EXTENSIONS:
          return {"error": "Invalid file type"}

        unique_filename = f"{uuid.uuid4()}.{extension}"
        file_location = os.path.join("images", unique_filename)

        with open(file_location, "wb") as image_file:
            image_file.write(await file.read())

        player.image = file_location
        db.commit()
        db.refresh(player)
        return {"message": "Image uploaded successfully", "image_path": file_location}
    except Exception as e:
        return {"error": str(e)}