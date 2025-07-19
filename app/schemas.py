from pydantic import BaseModel

class PlayerCreate(BaseModel):
  name: str
  pot: int
  position: str
  image: str = None

class TeamCreate(BaseModel):
  name: str
  image: str = None
  
class DraftRequest(BaseModel):
  team_name: str
  player_id: int

class TeamResponse(BaseModel):
  id: int
  name: str
  image: str | None = None