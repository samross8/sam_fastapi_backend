from models import Pick, CheatSheetResponse, FullCheatSheetResponse
from scrapers.games import fetch_today_matchups
from datetime import datetime
import pytz


def generate_cheatsheet(day: str) -> FullCheatSheetResponse:
    matchups = fetch_today_matchups()
    now = datetime.now(pytz.timezone("US/Eastern"))

    moneyline_picks = []

    for game in matchups:
        try:
            matchup = game["matchup"]
            pitchers = game["pitchers"]
            home_team = matchup.split("@")[1].strip()
            away_team = matchup.split("@")[0].strip()

            # Use a consistent string hash to seed confidence
            seed = sum(ord(c) for c in home_team + pitchers)
            score = 8.0 + (seed % 12) * 0.1  # Range ~8.0–9.1
            confidence = round(score, 2)

            wager = (
                "3 units" if confidence >= 9.0 else
                "2 units" if confidence >= 8.5 else
                "1 unit"
            )

            moneyline_picks.append(
                Pick(label=f"{home_team} ML", confidence=confidence, recommended_wager=wager)
            )
        except Exception:
            continue

    # Sort by confidence and slice into parlay suite
    moneyline_picks.sort(key=lambda x: x.confidence, reverse=True)

    def slice_conf(start, end):
        return [p for p in moneyline_picks if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [moneyline_picks[0]] if moneyline_picks else [],
        "doubloon_doubler_1": slice_conf(9.0, 9.3),
        "doubloon_doubler_2": slice_conf(8.7, 9.0),
        "mini_lotto": slice_conf(8.4, 8.7),
        "lotto_play": slice_conf(0, 8.4)
    }

    return FullCheatSheetResponse(
        slate_summary=matchups,
        cheatsheet=CheatSheetResponse(
            Moneyline=moneyline_picks,
            RunLine=[], NRFI=[], Hits=[], HR=[]
        ),
        parlay_suite=parlay_suite
    )
