from pydantic import BaseModel
from typing import List, Optional

class Pick(BaseModel):
    label: str
    confidence: float
    recommended_wager: Optional[str] = None

class CheatSheetResponse(BaseModel):
    Moneyline: Optional[List[Pick]] = []
    RunLine: Optional[List[Pick]] = []
    NRFI: Optional[List[Pick]] = []
    Hits: Optional[List[Pick]] = []
    HR: Optional[List[Pick]] = []

class FullCheatSheetResponse(BaseModel):
    slate_summary: List[dict]
    cheatsheet: CheatSheetResponse
    parlay_suite: dict
