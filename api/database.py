from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

DATABASE_URL = "sqlite:///./db.sqlite"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db():
    inspector = inspect(engine)
    if (not inspector.has_table("teams") or
        not inspector.has_table("checkers") or
            not inspector.has_table("flags")):
        Base.metadata.create_all(bind=engine)
