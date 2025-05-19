from models import Pick, CheatSheetResponse
from datetime import datetime
from scrapers.games import fetch_today_matchups

def generate_cheatsheet(day: str) -> CheatSheetResponse:
    matchups = fetch_today_matchups()

    now = datetime.now()

    # Fallback mock picks if no matchups
    if not matchups:
        return CheatSheetResponse(
            slate_summary=[],
            cheatsheet={"Moneyline": [], "RunLine": [], "NRFI": [], "Hits": [], "HR": []},
            parlay_suite={"best_bet": [], "doubloon_doubler_1": [], "doubloon_doubler_2": [],
                          "mini_lotto": [], "lotto_play": []}
        )

    # Example: basic pick generator from real matchups
    picks = {
        "Moneyline": [],
        "RunLine": [],
        "NRFI": [],
        "Hits": [],
        "HR": []
    }

    for game in matchups:
        matchup = game["matchup"]
        pitchers = game["pitchers"]
        start_time = game["start_time_et"]
        projected_flow = game["projected_flow"]

        # Simple logic (for now) — confidence seeded by keyword
        base_conf = 8.0
        if "control" in projected_flow or "edge" in projected_flow:
            confidence = base_conf + 1.0
        elif "early lead" in projected_flow:
            confidence = base_conf + 0.5
        else:
            confidence = base_conf

        picks["Moneyline"].append(Pick(label=f"{matchup.split('@')[1].strip()} ML", confidence=round(confidence, 2)))
        picks["RunLine"].append(Pick(label=f"{matchup.split('@')[0].strip()} +1.5", confidence=round(confidence - 0.2, 2)))
        picks["NRFI"].append(Pick(label=f"NRFI – {matchup}", confidence=round(confidence + 0.1, 2)))
        picks["Hits"].append(Pick(label=f"{pitchers.split('vs')[1].strip()} 1+ Hit", confidence=round(confidence + 0.3, 2)))
        picks["HR"].append(Pick(label=f"{pitchers.split('vs')[0].strip()} HR", confidence=round(confidence - 0.4, 2)))

    all_picks = [(cat, pick) for cat in picks for pick in picks[cat]]
    all_picks.sort(key=lambda x: x[1].confidence, reverse=True)

    def slice_confidence(start, end):
        return [p for _, p in all_picks if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [all_picks[0][1].dict()] if all_picks else [],
        "doubloon_doubler_1": [p.dict() for p in slice_confidence(9.0, 9.3)],
        "doubloon_doubler_2": [p.dict() for p in slice_confidence(8.7, 9.0)],
        "mini_lotto": [p.dict() for p in slice_confidence(8.4, 8.7)],
        "lotto_play": [p.dict() for p in slice_confidence(0, 8.4)]
    }

    return CheatSheetResponse(
        slate_summary=matchups,
        cheatsheet=picks,
        parlay_suite=parlay_suite
    )

from models import CheatSheetResponse, Pick

def generate_kbo_cheatsheet() -> CheatSheetResponse:
    # ✅ This is placeholder data used for testing
    picks = {
        "Moneyline": [
            Pick(label="Doosan Bears ML", confidence=8.9),
            Pick(label="NC Dinos ML", confidence=8.7),
            Pick(label="SSG Landers ML", confidence=8.6),
        ],
        "RunLine": [],
        "NRFI": [],
        "Hits": [],
        "HR": []
    }

    return CheatSheetResponse(
        slate_summary=[
            {
                "matchup": "Doosan Bears @ LG Twins",
                "pitchers": "R. Alcantara vs K. Young",
                "start_time_et": "5:30 AM ET",
                "projected_flow": "Doosan leads early. LG has bullpen edge late."
            },
            {
                "matchup": "NC Dinos @ Hanwha Eagles",
                "pitchers": "P. Krish vs J. Nam",
                "start_time_et": "5:30 AM ET",
                "projected_flow": "Low-scoring until 6th. NC offense wakes up mid-game."
            },
            {
                "matchup": "SSG Landers @ Kiwoom Heroes",
                "pitchers": "R. Wilkerson vs J. Hur",
                "start_time_et": "5:30 AM ET",
                "projected_flow": "SSG puts up runs early. Kiwoom keeps it close late."
            }
        ],
        cheatsheet=picks,
        parlay_suite={
            "best_bet": [Pick(label="Doosan Bears ML", confidence=8.9).dict()],
            "doubloon_doubler_1": [],
            "doubloon_doubler_2": [],
            "mini_lotto": [],
            "lotto_play": []
        }
    )
