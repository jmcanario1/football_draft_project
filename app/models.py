from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Player(Base):
  __tablename__ = 'players'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(60), nullable=False)
  pot = Column(Integer, nullable=False)
  position = Column(Integer, nullable=False)
  drafted_by = Column(String, nullable=True)

