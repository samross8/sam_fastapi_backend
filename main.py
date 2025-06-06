from fastapi import FastAPI
from core import generate_cheatsheet
# from core import generate_kbo_cheatsheet  # Temporarily disabled
from models import FullCheatSheetResponse

app = FastAPI()

@app.get("/cheatsheet/today")
def get_today_cheatsheet():
    return generate_cheatsheet(day="today")

@app.get("/cheatsheet/tomorrow")
def get_tomorrow_cheatsheet():
    return generate_cheatsheet(day="tomorrow")

@app.get("/cheatsheet/preakness")
def get_preakness_cheatsheet():
    return generate_preakness()

# @app.get("/cheatsheet/kbo", response_model=CheatSheetResponse)
# def get_kbo_cheatsheet():
#     return generate_kbo_cheatsheet()

# from core import generate_kbo_cheatsheet  ← Comment this out

...

# @app.get("/cheatsheet/kbo", response_model=CheatSheetResponse)
# def get_kbo_cheatsheet():
#     return generate_kbo_cheatsheet()
