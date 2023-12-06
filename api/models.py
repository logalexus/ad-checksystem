import uuid
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base


class Flag(Base):
    __tablename__ = "flags"

    id = Column(String, primary_key=True, default=str(
        uuid.uuid4()), unique=True, nullable=False)
    flag = Column(String, unique=True)
    lifetime = Column(String)
    public_flag_data = Column(String)
    checker_id = Column(Integer, ForeignKey('checkers.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))

    checker = relationship("Checker", back_populates="flag")
    team = relationship("Team", back_populates="flag")


class Checker(Base):
    __tablename__ = "checkers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    path = Column(String, unique=True)
    flag = relationship("Flag", back_populates="checker")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    ip = Column(String, unique=True)
    flag = relationship("Flag", back_populates="team")
