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
