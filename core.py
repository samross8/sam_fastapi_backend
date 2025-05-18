from models import Pick
from scrapers.games import fetch_today_matchups

def generate_cheatsheet(day: str):
    matchups = fetch_today_matchups()

    # Quick example confidence logic — replace with full model scoring later
    cheat_sheet = {
        "Moneyline": [],
        "RunLine": [],
        "NRFI": [],
        "Hits": [],
        "HR": []
    }

    for game in matchups:
        home = game["matchup"].split("@")[1].strip()
        away = game["matchup"].split("@")[0].strip()
        home_team = home.split()[0]
        away_team = away.split()[0]

        # Sample logic — inject your model logic here
        cheat_sheet["Moneyline"].append(Pick(label=f"{home_team} ML", confidence=8.7))
        cheat_sheet["RunLine"].append(Pick(label=f"{away_team} +1.5", confidence=9.1))
        cheat_sheet["NRFI"].append(Pick(label=f"NRFI – {game['matchup']}", confidence=8.9))
        cheat_sheet["Hits"].append(Pick(label="Luis Arraez 1+ Hit", confidence=9.3))
        cheat_sheet["HR"].append(Pick(label="Aaron Judge HR", confidence=8.2))

    # Flatten and rank all picks
    all_picks = sorted(
        [(cat, p) for cat, plist in cheat_sheet.items() for p in plist],
        key=lambda x: x[1].confidence,
        reverse=True
    )

    def tier(start, end):
        return [p.dict() for _, p in all_picks if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [all_picks[0][1].dict()] if all_picks else [],
        "doubloon_doubler_1": tier(9.0, 9.3),
        "doubloon_doubler_2": tier(8.7, 9.0),
        "mini_lotto": tier(8.4, 8.7),
        "lotto_play": tier(0.0, 8.4)
    }

    for tier_name, picks in parlay_suite.items():
        wager = {
            "best_bet": "3 units",
            "doubloon_doubler_1": "2.5 units",
            "doubloon_doubler_2": "2 units",
            "mini_lotto": "1 unit",
            "lotto_play": "0.5 units"
        }[tier_name]
        for pick in picks:
            pick["recommended_wager"] = wager

    return {
        "slate_summary": matchups,
        "cheatsheet": {k: [p.dict() for p in v] for k, v in cheat_sheet.items()},
        "parlay_suite": parlay_suite
    }
