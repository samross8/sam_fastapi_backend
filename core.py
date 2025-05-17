from models import Pick
from datetime import datetime

def generate_cheatsheet(day: str):
    # Simulated real matchups (normally pulled from Baseball Savant or Lineups.com)
    matchups = [
        {
            "matchup": "Rays @ Blue Jays",
            "pitchers": "Z. Eflin vs K. Gausman",
            "start_time_et": "1:07 PM ET",
            "projected_flow": "Tight early, Rays pull ahead mid-game. Bullpen edge Toronto."
        },
        {
            "matchup": "Guardians @ Twins",
            "pitchers": "T. Bibee vs J. Ryan",
            "start_time_et": "2:10 PM ET",
            "projected_flow": "Guardians start slow, Twins lead early. Cleveland rallies late with bullpen advantage."
        },
        {
            "matchup": "Phillies @ Nationals",
            "pitchers": "Z. Wheeler vs M. Gore",
            "start_time_et": "4:05 PM ET",
            "projected_flow": "Phils control early. Nationals show fight late but edge stays Philly."
        },
        {
            "matchup": "Padres @ Braves",
            "pitchers": "D. Cease vs C. Morton",
            "start_time_et": "7:20 PM ET",
            "projected_flow": "Early offense both sides. Game flips in bullpen innings. Slight edge Braves."
        }
    ]

    cheat_sheet = {
        "Moneyline": [
            Pick(label="Guardians ML", confidence=9.2),
            Pick(label="Padres ML", confidence=8.8),
            Pick(label="Rays ML", confidence=8.4),
        ],
        "RunLine": [
            Pick(label="Phillies +1.5", confidence=9.3),
            Pick(label="Twins +1.5", confidence=8.85),
            Pick(label="Cubs +1.5", confidence=8.5),
        ],
        "NRFI": [
            Pick(label="NRFI – Braves vs Padres", confidence=9.1),
            Pick(label="NRFI – Rays vs Blue Jays", confidence=8.6),
        ],
        "Hits": [
            Pick(label="Luis Arraez 1+ Hit", confidence=9.3),
            Pick(label="Bryce Harper 1+ Hit", confidence=8.95),
        ],
        "HR": [
            Pick(label="Kyle Schwarber HR", confidence=8.5),
            Pick(label="Aaron Judge HR", confidence=8.25),
        ]
    }

    # Flatten and rank all picks
    all_picks = sorted(
        [(cat, p) for cat, plist in cheat_sheet.items() for p in plist],
        key=lambda x: x[1].confidence,
        reverse=True
    )

    def tier(start, end):
        return [p.dict() for _, p in all_picks if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [all_picks[0][1].dict()],
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
