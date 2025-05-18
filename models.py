from typing import List, Dict
from pydantic import BaseModel

class Pick(BaseModel):
    label: str
    confidence: float
    recommended_wager: str

class GameSummary(BaseModel):
    matchup: str
    pitchers: str
    start_time_et: str
    projected_flow: str

class CheatSheetResponse(BaseModel):
    slate_summary: List[GameSummary]
    cheatsheet: Dict[str, List[Pick]]
    parlay_suite: Dict[str, List[Pick]]
