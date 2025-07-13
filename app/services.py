import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app import models

def process_csv(file: UploadFile, db: Session):
  df = pd.read_csv(file.file)

  db.query(models.Player).delete()
  db.commit()

  for _, row in df.iterrows():
    player = models.Player(
      name=row['name'],
      pot=row['pot'],
      position=row.get("position")
    )
    db.add(player)
  db.commit()

  return {"message": "CSV processed successfully"}


def get_grid_data(db: Session):
  players = db.query(models.Player).all()
  grid = {}

  for p in players:
    grid.setdefault(p.pot, []).append({
      "id": p.id,
      "name": p.name,
      "position": p.position
    })
  return grid


def assign_player_to_team(team_name: str, player_id: int, db: Session):
  player = db.query(models.Player).filter(models.Player.id == player_id).first()

  player.drafted_by = team_name
  db.commit()
  return