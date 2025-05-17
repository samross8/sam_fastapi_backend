from fastapi import FastAPI
from core import generate_cheatsheet

app = FastAPI()

@app.get("/cheatsheet/today")
def get_today_cheatsheet():
    return generate_cheatsheet(day="today")

@app.get("/cheatsheet/tomorrow")
def get_tomorrow_cheatsheet():
    return generate_cheatsheet(day="tomorrow")
