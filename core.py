from models import Pick
from datetime import datetime

def generate_cheatsheet(day: str):
    # For demo purposes, this assumes it's for May 17
    # Replace this logic with scraper-driven inputs for future versions

    # --- Simulated Cheat Sheet Picks ---
    picks = {
        "Moneyline": [
            Pick(label="Rays ML", confidence=9.20),
            Pick(label="Blue Jays ML", confidence=8.85),
            Pick(label="Guardians ML", confidence=8.60),
        ],
        "RunLine": [
            Pick(label="Padres +1.5", confidence=9.35),
            Pick(label="Tigers +1.5", confidence=8.90),
            Pick(label="Nationals +1.5", confidence=8.70),
        ],
        "NRFI": [
            Pick(label="NRFI – Braves vs Padres", confidence=9.10),
            Pick(label="NRFI – Rays vs Blue Jays", confidence=8.60),
        ],
        "Hits": [
            Pick(label="Luis Arraez 1+ Hit", confidence=9.25),
            Pick(label="Bryce Harper 1+ Hit", confidence=8.95),
        ],
        "HR": [
            Pick(label="Kyle Schwarber HR", confidence=8.55),
            Pick(label="Aaron Judge HR", confidence=8.10),
        ]
    }

    # --- Parlay Suite Tier Logic ---
    all_picks = sorted(
        [(cat, pick) for cat, plist in picks.items() for pick in plist],
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

    # --- Final Output ---
    return {
        "cheatsheet": {cat: [p.dict() for p in plist] for cat, plist in picks.items()},
        "parlay_suite": parlay_suite
    }
