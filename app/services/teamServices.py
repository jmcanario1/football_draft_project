from app import models
from sqlalchemy.orm import Session
from app.schemas import TeamCreate
from fastapi import UploadFile

def create_team(team: TeamCreate, db: Session):
  new_team = models.Team(
    name=team.name,
    image=team.image
  )
  db.add(new_team)
  db.commit()

def get_team(team_id: int, db: Session):
  team = db.query(models.Team).filter(models.Team.id == team_id).first()
  if team_id:
    return {
      "id": team.id,
      "name": team.name,
      "pot": team.pot,
      "position": team.position,
      "image": team.image
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
        file_location = f"images/{file.filename}"
        with open(file_location, "wb") as image_file:
            image_file.write(await file.read())

        player.image = file_location
        db.commit()
        return {"message": "Image uploaded successfully", "image_path": file_location}
    except Exception as e:
        return {"error": str(e)}