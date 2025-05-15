from fastapi import FastAPI
from core import generate_cheatsheet
from models import CheatSheetResponse

app = FastAPI()

@app.get("/cheatsheet/today", response_model=CheatSheetResponse)
def get_today_cheatsheet():
    return generate_cheatsheet(day="today")

@app.get("/cheatsheet/tomorrow", response_model=CheatSheetResponse)
def get_tomorrow_cheatsheet():
    return generate_cheatsheet(day="tomorrow")

