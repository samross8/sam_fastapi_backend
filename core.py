from models import Pick
from datetime import datetime

def get_may18_matchups():
    return [
        {
            "matchup": "Brewers @ Astros",
            "pitchers": "T. Megill vs J. Verlander",
            "start_time_et": "2:10 PM ET",
            "projected_flow": "Astros start fast. Brewers fight midgame. Slight edge Astros late."
        },
        {
            "matchup": "Rays @ Blue Jays",
            "pitchers": "T. Bradley vs Y. Kikuchi",
            "start_time_et": "1:37 PM ET",
            "projected_flow": "Rays pressure early. Jays strike late. Bullpen edge Tampa."
        },
        {
            "matchup": "Nationals @ Phillies",
            "pitchers": "T. Williams vs C. Sanchez",
            "start_time_et": "1:35 PM ET",
            "projected_flow": "Phillies control early. Nats surge in 6th+. Bullpen edge Philly."
        },
        {
            "matchup": "Mariners @ Orioles",
            "pitchers": "B. Woo vs C. Irvin",
            "start_time_et": "1:35 PM ET",
            "projected_flow": "Tight all game. Pitchers duel early. Extra-base edge Orioles."
        },
        {
            "matchup": "White Sox @ Yankees",
            "pitchers": "C. Flexen vs C. Rodón",
            "start_time_et": "1:35 PM ET",
            "projected_flow": "Yankees dominate early. White Sox unlikely to recover."
        },
        {
            "matchup": "Twins @ Guardians",
            "pitchers": "B. Ober vs B. Gaddis",
            "start_time_et": "1:40 PM ET",
            "projected_flow": "Guardians aggressive early. Twins take control midgame."
        },
        {
            "matchup": "Angels @ Rangers",
            "pitchers": "J. Soriano vs J. Gray",
            "start_time_et": "2:35 PM ET",
            "projected_flow": "Rangers build early lead. Angels rally 7th+. Edge Texas."
        },
        {
            "matchup": "Pirates @ Cubs",
            "pitchers": "J. Jones vs J. Taillon",
            "start_time_et": "2:20 PM ET",
            "projected_flow": "Pitchers solid. Late scoring decides it. Slight edge Cubs."
        }
    ]

def generate_cheatsheet(day: str):
    matchups = get_may18_matchups()

    cheat_sheet = {
        "Moneyline": [
            Pick(label="Astros ML", confidence=9.25),
            Pick(label="Phillies ML", confidence=8.90),
            Pick(label="Guardians ML", confidence=8.60),
        ],
        "RunLine": [
            Pick(label="Rays +1.5", confidence=9.30),
            Pick(label="Cubs +1.5", confidence=8.85),
        ],
        "NRFI": [
            Pick(label="NRFI – Brewers vs Astros", confidence=9.10),
            Pick(label="NRFI – Pirates vs Cubs", confidence=8.60),
        ],
        "Hits": [
            Pick(label="Luis Arraez 1+ Hit", confidence=9.35),
            Pick(label="Trea Turner 1+ Hit", confidence=8.95),
        ],
        "HR": [
            Pick(label="Aaron Judge HR", confidence=8.55),
            Pick(label="Kyle Tucker HR", confidence=8.20),
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
