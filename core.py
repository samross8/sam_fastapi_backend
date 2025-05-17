from models import CheatSheetResponse, Pick

def generate_cheatsheet(day: str) -> CheatSheetResponse:
    return CheatSheetResponse(
        Moneyline=[
            Pick(label="TEST Team ML", confidence=9.1),
        ],
        RunLine=[],
        NRFI=[],
        Hits=[],
        HR=[]
    )
# Placeholder for core.py
