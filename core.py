from models import Pick
from datetime import datetime

def get_today_matchups():
    return [
        {
            "matchup": "Guardians @ Twins",
            "pitchers": "T. Bibee vs J. Ryan",
            "start_time_et": "2:10 PM ET",
            "projected_flow": "Twins lead early. Guardians rally midgame. Bullpen edge Cleveland."
        },
        {
            "matchup": "Phillies @ Nationals",
            "pitchers": "Z. Wheeler vs M. Gore",
            "start_time_et": "4:05 PM ET",
            "projected_flow": "Wheeler dominant early. Game slows late. Low total expected."
        },
        {
            "matchup": "Rays @ Blue Jays",
            "pitchers": "Z. Eflin vs K. Gausman",
            "start_time_et": "3:07 PM ET",
            "projected_flow": "Strong SPs cancel out early scoring. Jays likely break through 6th+."
        },
        {
            "matchup": "Padres @ Braves",
            "pitchers": "D. Cease vs C. Morton",
            "start_time_et": "7:20 PM ET",
            "projected_flow": "Early runs both sides. Braves close stronger late behind pen."
        }
    ]

def generate_cheatsheet(day: str):
    matchups = get_today_matchups()

    cheat_sheet = {
        "Moneyline": [
            Pick(label="Guardians ML", confidence=9.2),
            Pick(label="Padres ML", confidence=8.85),
            Pick(label="Rays ML", confidence=8.4),
        ],
        "RunLine": [
            Pick(label="Phillies +1.5", confidence=9.35),
            Pick(label="Twins +1.5", confidence=8.85),
        ],
        "NRFI": [
            Pick(label="NRFI – Rays vs Blue Jays", confidence=9.15),
            Pick(label="NRFI – Padres vs Braves", confidence=8.6),
        ],
        "Hits": [
            Pick(label="Luis Arraez 1+ Hit", confidence=9.3),
            Pick(label="Juan Soto 1+ Hit", confidence=8.95),
        ],
        "HR": [
            Pick(label="Aaron Judge HR", confidence=8.55),
            Pick(label="Matt Olson HR", confidence=8.15),
        ]
    }

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

def generate_preakness():
    horses = [
        {"name": "Mugatu", "post": 1, "win_conf": 2.1, "top3_conf": 4.8},
        {"name": "Uncle Heavy", "post": 2, "win_conf": 4.0, "top3_conf": 7.2},
        {"name": "Catching Freedom", "post": 3, "win_conf": 7.6, "top3_conf": 9.0},
        {"name": "Muth (SCR)", "post": 4, "win_conf": 0.0, "top3_conf": 0.0},
        {"name": "Mystik Dan", "post": 5, "win_conf": 9.4, "top3_conf": 9.8},
        {"name": "Seize the Grey", "post": 6, "win_conf": 5.9, "top3_conf": 8.0},
        {"name": "Just Steel", "post": 7, "win_conf": 4.8, "top3_conf": 7.1},
        {"name": "Tuscan Gold", "post": 8, "win_conf": 6.5, "top3_conf": 8.6},
        {"name": "Imagination", "post": 9, "win_conf": 8.4, "top3_conf": 9.2}
    ]

    projected_flow = "Sharp early pace from posts 1, 3, 6. Sets up for mid-pack stalkers like Mystik Dan and Imagination. Off-track experience could be key."

    return {
        "race": "Preakness Stakes – May 18",
        "projected_flow": projected_flow,
        "entries": horses
    }
