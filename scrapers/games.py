import requests
from datetime import datetime
import pytz

def fetch_today_matchups(debug=False):
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        if debug:
            print("❌ Error fetching ESPN data:", e)
        return []

    games = []
    eastern = pytz.timezone("US/Eastern")
    today = datetime.now(eastern).date()

    for event in data.get("events", []):
        try:
            competitions = event.get("competitions", [])[0]
            competitors = competitions.get("competitors", [])

            away_team = next((c for c in competitors if c["homeAway"] == "away"), {})
            home_team = next((c for c in competitors if c["homeAway"] == "home"), {})

            away_name = away_team.get("team", {}).get("displayName", "")
            home_name = home_team.get("team", {}).get("displayName", "")

            away_pitcher = away_team.get("probables", [{}])[0].get("fullName", "TBD")
            home_pitcher = home_team.get("probables", [{}])[0].get("fullName", "TBD")

            game_time_raw = competitions.get("date")
            dt = datetime.fromisoformat(game_time_raw.replace("Z", "+00:00"))
            dt_et = dt.astimezone(eastern)
            if dt_et.date() != today:
                continue

            games.append({
                "matchup": f"{away_name} @ {home_name}",
                "pitchers": f"{away_pitcher} vs {home_pitcher}",
                "start_time_et": dt_et.strftime("%-I:%M %p ET")
            })
        except Exception as e:
            if debug:
                print("⚠️ Error parsing game:", e)
            continue

    if debug:
        print(f"✅ Found {len(games)} games on ESPN")
        for g in games:
            print(g)

    return games
