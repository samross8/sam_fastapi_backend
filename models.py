from pydantic import BaseModel
from typing import List

class Pick(BaseModel):
    label: str
    confidence: float
    recommended_wager: str  # ✅ NEW FIELD

class CheatSheetResponse(BaseModel):
    Moneyline: List[Pick]
    RunLine: List[Pick]
    NRFI: List[Pick]
    Hits: List[Pick]
    HR: List[Pick]

class FullCheatSheetResponse(BaseModel):
    slate_summary: List[dict]
    cheatsheet: CheatSheetResponse
    parlay_suite: dict
