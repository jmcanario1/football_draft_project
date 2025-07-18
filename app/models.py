from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
  __tablename__ = 'players'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(60), nullable=False)
  pot = Column(Integer, nullable=False)
  position = Column(Integer, nullable=False)
  image = Column(String(255), nullable=True)
  drafted_by = Column(String, ForeignKey("teams_id"), nullable=True)
  team = relationship("Team", back_populates="players")

class Team(Base):
  __tablename__ = 'teams'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(60), nullable=False)
  image = Column(String(255), nullable=True)
  players = relationship("Player", back_populates="team")