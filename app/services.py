import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app import models

async def process_csv(file: UploadFile, db: Session):
  try:
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
  
  except Exception as e:
    return(e)


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
  try:
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    if player.drafted_by is None:
      player.drafted_by = team_name
      db.commit()
      return {"message": f"Player {player.name} drafted by {team_name}"}
    else:
      return {"message": f"Player {player.name} is already drafted by {player.drafted_by}"}
    
  except Exception as e:
    return(e)


def get_teams(db: Session):
  players = db.query(models.Player).filter(models.Player.drafted_by.isnot(None)).all()

  teams = {}

  for player in players:
    team = player.drafted_by

    if team not in teams:
      teams[team] = []
    teams[team].append({
      "id": player.id,
      "name": player.name,
      "pot": player.pot,
      "position": player.position
    })

  return teams