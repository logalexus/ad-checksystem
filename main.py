import json
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from api.database import SessionLocal
from api import repository

app = FastAPI()


@app.get("/api/attack_data/")
async def get_attack_data(service_id: int):
    with SessionLocal() as db:
        teams_info = repository.get_teams_info(db)
        attack_data = {}
        for team in teams_info:
            team_data = {
                "name": team.name,
                "host": team.ip,
                "flag_ids": [json.loads(flag.public_flag_data)["public_flag_id"] for flag in team.flag if flag.checker_id == service_id]
            }
            attack_data[team.id] = team_data
        attack_data = {"flag_ids": attack_data}
    return attack_data


@app.put("/api/submit")
async def submit_flags(submit_flags: List[str]):
    with SessionLocal() as db:
        flags = repository.get_all_flags(db)
        submit_result = []
        for submit_flag in submit_flags:
            real_flag = next(
                filter(lambda flag: flag.flag == submit_flag, flags), None)
            if real_flag:
                msg = "Accepted"
                status = True
            else:
                msg = "Wrong"
                status = False

            submit_flag_result = {
                "status": status,
                "flag": submit_flag,
                "msg": msg
            }
            submit_result.append(submit_flag_result)

    return submit_result
