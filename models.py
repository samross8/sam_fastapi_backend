from pydantic import BaseModel
from typing import Optional  # ⬅️ make sure this is imported too

class Pick(BaseModel):
    label: str
    confidence: float
    recommended_wager: Optional[str] = None  # ✅ make it optional

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
