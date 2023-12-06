from typing import List
from sqlalchemy.orm import Session, joinedload
from api.models import Checker, Flag, Team


def get_checkers(db: Session) -> List[Checker]:
    return db.query(Checker).all()


def get_teams(db: Session) -> List[Team]:
    return db.query(Team).all()


def delete_teams(db: Session):
    db.query(Team).delete()
    db.commit()


def get_checker_by_id(db: Session, checker_id: int) -> List[Checker]:
    return db.query(Checker).filter(Checker.id == checker_id).first()


def delete_checkers(db: Session):
    db.query(Checker).delete()
    db.commit()


def add_checker(db: Session, checker: Checker):
    db.add(checker)
    db.commit()
    db.refresh(checker)
    return checker


def add_team(db: Session, team: Team):
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def add_flag(db: Session, flag: Flag) -> Flag:
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return flag


def add_public_flag_data(db: Session, flag: Flag, data: str):
    flag = db.query(Flag).filter(Flag.id == flag.id).first()
    flag.public_flag_data = data
    db.commit()
    db.refresh(flag)


def get_flags_by_checker_and_team(db: Session, checker_id: int, team_id: int) -> List[Flag]:
    return db.query(Flag).filter(Flag.checker_id == checker_id and
                                 Flag.team_id == team_id).all()


def get_all_flags(db: Session):
    return db.query(Flag).all()


def get_teams_info(db: Session):
    teams_info = (
        db.query(Team)
        .options(joinedload(Team.flag))
        .all()
    )
    return teams_info
