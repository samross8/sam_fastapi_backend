from pydantic import BaseModel
from typing import List

class Pick(BaseModel):
    label: str
    confidence: float

class CheatSheetResponse(BaseModel):
    Moneyline: List[Pick]
    RunLine: List[Pick]
    NRFI: List[Pick]
    Hits: List[Pick]
    HR: List[Pick]

