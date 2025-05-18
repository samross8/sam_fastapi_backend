from models import CheatSheetResponse, Pick
from scrapers.games import fetch_today_matchups

# --- Moneyline Confidence Model ---
def score_moneyline(game):
    matchup = game.get("matchup", "")
    pitchers = game.get("pitchers", "")
    
    try:
        away_team, home_team = [t.strip() for t in matchup.split("@")]
        sp_away, sp_home = [p.strip() for p in pitchers.split("vs")]
    except:
        return None  # Skip invalid format

    score = 8.0

    # Example scoring logic (replace with deeper stats later)
    score += 0.2  # Home field advantage
    score += 0.3  # Placeholder SP edge
    score += 0.3  # Placeholder matchup edge

    return {
        "label": f"{home_team} ML",
        "confidence": round(score, 2)
    }

# --- Main generator ---
def generate_cheatsheet(day: str) -> CheatSheetResponse:
    matchups = fetch_today_matchups()
    moneyline_picks = []

    for game in matchups:
        ml_pick = score_moneyline(game)
        if ml_pick and ml_pick["confidence"] >= 8.0:
            moneyline_picks.append(Pick(**ml_pick))

    picks = {
        "Moneyline": moneyline_picks,
        "RunLine": [],
        "NRFI": [],
        "Hits": [],
        "HR": []
    }

    all_picks = []
    for cat, plist in picks.items():
        for p in plist:
            all_picks.append((cat, p))

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
