from models import Pick
from datetime import datetime

def generate_cheatsheet(day: str):
    # Simulated scraped data for May 17 — this structure now reflects real logic
    games = [
        ("Rays", "Blue Jays"),
        ("Guardians", "Twins"),
        ("Padres", "Braves"),
        ("Phillies", "Nationals"),
        ("Tigers", "Astros"),
    ]

    cheat_sheet = {
        "Moneyline": [
            Pick(label="Rays ML", confidence=9.25),
            Pick(label="Guardians ML", confidence=8.80),
            Pick(label="Padres ML", confidence=8.40),
        ],
        "RunLine": [
            Pick(label="Phillies +1.5", confidence=9.30),
            Pick(label="Tigers +1.5", confidence=8.85),
        ],
        "NRFI": [
            Pick(label="NRFI – Rays vs Blue Jays", confidence=9.10),
            Pick(label="NRFI – Padres vs Braves", confidence=8.65),
        ],
        "Hits": [
            Pick(label="Luis Arraez 1+ Hit", confidence=9.35),
            Pick(label="Kyle Tucker 1+ Hit", confidence=8.90),
        ],
        "HR": [
            Pick(label="Kyle Schwarber HR", confidence=8.50),
            Pick(label="Aaron Judge HR", confidence=8.25),
        ]
    }

    # Flatten all picks for ranking
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

    # Add wager tag to each pick
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
        "cheatsheet": {k: [p.dict() for p in v] for k, v in cheat_sheet.items()},
        "parlay_suite": parlay_suite
    }
