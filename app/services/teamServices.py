from app import models
from sqlalchemy.orm import Session
from app.schemas import TeamCreate
from fastapi import UploadFile
import uuid
import os


def create_team(team: TeamCreate, db: Session):
  new_team = models.Team(
    name=team.name,
    image=team.image
  )
  db.add(new_team)
  db.commit()
  return {"message": "Team created successfully"}


def get_team(team_id: int, db: Session):
  team = db.query(models.Team).filter(models.Team.id == team_id).first()
  if team_id:
    return {
      "id": team.id,
      "name": team.name,
      "image": team.image
    }
  return {"error": "Team not found"}


async def delete_team(team_id: int, db: Session):
  team = db.query(models.Team).filter(models.Team.id == team_id).first()
  if team:
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}
  return {"error": "Team not found"}


async def upload_team_image(team_id: int, file: UploadFile, db: Session):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        return {"error": "Team not found"}
    try:
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
        extension = file.filename.split(".")[-2].lower()
        if extension not in ALLOWED_EXTENSIONS:
          return {"error": "Invalid file type"}

        unique_filename = f"{uuid.uuid4()}.{extension}"
        file_location = os.path.join("images", unique_filename)

        with open(file_location, "wb") as image_file:
            image_file.write(await file.read())

        team.image = file_location
        db.commit()
        db.refresh(team)
        return {"message": "Image uploaded successfully", "image_path": file_location}
    except Exception as e:
        return {"error": str(e)}