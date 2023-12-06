import random
import subprocess
import uuid
import yaml
import repository
from time import sleep
from api.utils import generate_flag
from api.models import Checker, Flag, Team
from api.database import SessionLocal, create_db

ROUND_TIME = 15
PYTHON_PATH = ".venv/Scripts/python.exe"


def check(checker: Checker, team: Team):
    command = [
        PYTHON_PATH,
        checker.path,
        "check",
        team.ip
    ]

    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30
    )

    return process.returncode


def put(checker: Checker, team: Team):
    flag = Flag(
        id=str(uuid.uuid4()),
        flag=generate_flag(),
        lifetime=3,
        public_flag_data="None",
        checker_id=checker.id,
        team_id=team.id
    )

    with SessionLocal() as db:
        flag = repository.add_flag(db, flag)

        command = [
            PYTHON_PATH,
            checker.path,
            "put",
            team.ip,
            flag.id,
            flag.flag,
            "1"
        ]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output, error = process.communicate()

        repository.add_public_flag_data(db, flag, output.decode())

    return output, error


def get(checker: Checker, team: Team):
    with SessionLocal() as db:
        flags = repository.get_flags_by_checker_and_team(
            db, checker.id, team.id)

    flag = random.choice(flags)

    command = [
        PYTHON_PATH,
        checker.path,
        "get",
        team.ip,
        flag.public_flag_data,
        flag.flag,
        "1"
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return process.communicate()


def round(counter: int, checker: Checker, team: Team):
    code = check(checker, team)
    if code == 104 or code == 110:
        print("Service is DOWN")
        return

    output, error = put(checker, team)
    print(output.decode(errors="ignore"))
    print(error.decode(errors="ignore"))

    if counter % 3 == 0:
        output, error = get(checker, team)
        print(output.decode(errors="ignore"))
        print(error.decode(errors="ignore"))


def run():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    with SessionLocal() as db:
        repository.delete_teams(db)
        repository.delete_checkers(db)

        for team in config.get("teams", []):
            name = team.get("name")
            ip = team.get("ip")
            repository.add_team(db, Team(name=name, ip=ip))

        for checker in config.get("checkers", []):
            name = checker.get("name")
            path = checker.get("path")
            repository.add_checker(db, Checker(name=name, path=path))

    with SessionLocal() as db:
        checkers = repository.get_checkers(db)
        teams = repository.get_teams(db)

    counter = 0
    while True:
        for checker in checkers:
            for team in teams:
                round(counter, checker, team)
                sleep(ROUND_TIME)
        counter += 1


if __name__ == "__main__":
    create_db()
    run()
