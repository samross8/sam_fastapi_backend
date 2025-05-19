from models import Pick, FullCheatSheetResponse
from datetime import datetime
import pytz
from scrapers.games import fetch_today_matchups

def generate_cheatsheet(day: str) -> FullCheatSheetResponse:
    sample_picks = [
        Pick(label="Astros ML", confidence=9.2, recommended_wager="3 units"),
        Pick(label="Phillies ML", confidence=8.8, recommended_wager="2 units"),
        Pick(label="Guardians ML", confidence=8.7, recommended_wager="2 units"),
        Pick(label="Rangers ML", confidence=8.5, recommended_wager="2 units"),
        Pick(label="Tigers ML", confidence=8.3, recommended_wager="1 unit"),
        Pick(label="Mariners ML", confidence=8.1, recommended_wager="1 unit"),
    ]

    sorted_picks = sorted(sample_picks, key=lambda p: p.confidence, reverse=True)

    def slice_conf(start, end):
        return [p for p in sorted_picks if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [sorted_picks[0]],
        "doubloon_doubler_1": slice_conf(9.0, 9.3),
        "doubloon_doubler_2": slice_conf(8.7, 9.0),
        "mini_lotto": slice_conf(8.4, 8.7),
        "lotto_play": slice_conf(0, 8.4)
    }

    matchups = fetch_today_matchups()

    return FullCheatSheetResponse(
        slate_summary=matchups,
        cheatsheet={
            "Moneyline": sample_picks,
            "RunLine": [],
            "NRFI": [],
            "Hits": [],
            "HR": []
        },
        parlay_suite=parlay_suite
    )

def generate_kbo_cheatsheet() -> FullCheatSheetResponse:
    picks = [
        Pick(label="Doosan Bears ML", confidence=8.9, recommended_wager="2 units"),
        Pick(label="Samsung Lions ML", confidence=8.6, recommended_wager="2 units"),
        Pick(label="LG Twins ML", confidence=8.4, recommended_wager="2 units"),
    ]

    kbo_summary = [
        {
            "matchup": "Doosan Bears @ Kia Tigers",
            "pitchers": "R. Alcantara vs Y. Lee",
            "start_time_et": "5:30 AM ET"
        },
        {
            "matchup": "Samsung Lions @ SSG Landers",
            "pitchers": "D. Buchanan vs W. Kim",
            "start_time_et": "5:30 AM ET"
        },
        {
            "matchup": "LG Twins @ NC Dinos",
            "pitchers": "C. Kelly vs S. Chang",
            "start_time_et": "5:30 AM ET"
        },
    ]

    return FullCheatSheetResponse(
        slate_summary=kbo_summary,
        cheatsheet={
            "Moneyline": picks,
            "RunLine": [],
            "NRFI": [],
            "Hits": [],
            "HR": []
        },
        parlay_suite={
            "best_bet": [],
            "doubloon_doubler_1": [],
            "doubloon_doubler_2": [],
            "mini_lotto": [],
            "lotto_play": []
        }
    )
