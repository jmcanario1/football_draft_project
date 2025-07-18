from sqlalchemy.orm import Session
from app import models


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
  VALID_TEAMS = ["Time A", "Time B", "Time C", "Time D", "Time E", "Time F", "Time G", "Time H"]
  try:
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player.drafted_by is None:
      if team_name not in VALID_TEAMS:
          return {"error": f"Time '{team_name}' não é um time permitido."}
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


def reset_draft(db: Session):
    try:
        players = db.query(models.Player).all()
        for player in players:
            player.drafted_by = None
        db.commit()
        return {"message": "Draft resetado com sucesso"}
    except Exception as e:
        return {"error": str(e)}
