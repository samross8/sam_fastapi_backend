from models import Pick, CheatSheetResponse, FullCheatSheetResponse
from scrapers.games import fetch_today_matchups
from datetime import datetime
import pytz
import hashlib

def hash_confidence(base: str, offset: float = 0.0) -> float:
    # Use a consistent hash to generate a float between 0.0 and 1.0
    h = int(hashlib.sha256(base.encode()).hexdigest(), 16)
    return round(8.0 + (h % 100) / 100.0 + offset, 2)

def generate_cheatsheet(day: str) -> FullCheatSheetResponse:
    matchups = fetch_today_matchups()
    now = datetime.now(pytz.timezone("US/Eastern"))

    ml_picks = []
    runline_picks = []
    nrfi_picks = []
    hit_picks = []
    hr_picks = []

    for game in matchups:
        matchup = game.get("matchup", "")
        pitchers = game.get("pitchers", "TBD vs TBD")
        start_time = game.get("start_time_et", "TBD")

        if "@" not in matchup or "vs" not in pitchers:
            continue

        away_team, home_team = matchup.split("@")[0].strip(), matchup.split("@")[1].strip()
        away_pitcher, home_pitcher = pitchers.split("vs")[0].strip(), pitchers.split("vs")[1].strip()

        # --- Moneyline ---
        ml_score = hash_confidence(home_team + home_pitcher, 0.0)
        ml_picks.append(Pick(label=f"{home_team} ML", confidence=ml_score,
                             recommended_wager="3 units" if ml_score >= 9.0 else
                                                "2 units" if ml_score >= 8.5 else "1 unit"))

        # --- Run Line ---
        rl_score = hash_confidence(away_team + away_pitcher, -0.15)
        runline_picks.append(Pick(label=f"{away_team} +1.5", confidence=rl_score,
                                  recommended_wager="2 units" if rl_score >= 8.5 else "1 unit"))

        # --- NRFI ---
        nrfi_score = hash_confidence(matchup + pitchers, 0.05)
        nrfi_picks.append(Pick(label=f"NRFI – {matchup}", confidence=nrfi_score,
                               recommended_wager="2 units" if nrfi_score >= 8.5 else "1 unit"))

        # --- 1+ Hit ---
        hit_score = hash_confidence(home_pitcher + "hit", 0.12)
        hit_picks.append(Pick(label=f"{home_team} #3 hitter 1+ Hit", confidence=hit_score,
                              recommended_wager="2 units" if hit_score >= 8.5 else "1 unit"))

        # --- HR Prop ---
        hr_score = hash_confidence(home_pitcher + "HR", -0.05)
        hr_picks.append(Pick(label=f"{away_team} slugger HR", confidence=hr_score,
                             recommended_wager="1 unit" if hr_score >= 8.5 else "0.5 units"))

    # --- Sort for Parlay Suite ---
    all_picks = ml_picks + runline_picks + nrfi_picks + hit_picks + hr_picks
    all_picks.sort(key=lambda p: p.confidence, reverse=True)

    def slice_conf(start, end):
        return [p for p in all_picks if start <= p.confidence < end]

    parlay_suite = {
        "best_bet": [all_picks[0]] if all_picks else [],
        "doubloon_doubler_1": slice_conf(9.0, 9.3),
        "doubloon_doubler_2": slice_conf(8.7, 9.0),
        "mini_lotto": slice_conf(8.4, 8.7),
        "lotto_play": slice_conf(0, 8.4),
    }

    return FullCheatSheetResponse(
        slate_summary=matchups,
        cheatsheet=CheatSheetResponse(
            Moneyline=ml_picks,
            RunLine=runline_picks,
            NRFI=nrfi_picks,
            Hits=hit_picks,
            HR=hr_picks
        ),
        parlay_suite=parlay_suite
    )
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
