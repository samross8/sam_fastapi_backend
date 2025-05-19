import requests
from datetime import datetime
import pytz

def fetch_today_matchups(debug=False):
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date="
    now_et = datetime.now(pytz.timezone("US/Eastern"))
    today_str = now_et.strftime("%Y-%m-%d")
    full_url = f"{url}{today_str}"

    try:
        response = requests.get(full_url)
        data = response.json()
    except Exception as e:
        if debug:
            print("❌ Failed to fetch or parse MLB API JSON:", e)
        return []

    games = []
    for date_block in data.get("dates", []):
        for game in date_block.get("games", []):
            try:
                home_team = game["teams"]["home"]["team"]["name"]
                away_team = game["teams"]["away"]["team"]["name"]
                matchup = f"{away_team} @ {home_team}"

                # ✅ Safe fallback if pitcher data is missing
                away_pitcher = game["teams"]["away"].get("probablePitcher", {}).get("fullName") or "TBD"
                home_pitcher = game["teams"]["home"].get("probablePitcher", {}).get("fullName") or "TBD"
                pitchers = f"{away_pitcher} vs {home_pitcher}"

                raw_time = game["gameDate"]
                game_dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
                game_dt_et = pytz.utc.localize(game_dt).astimezone(pytz.timezone("US/Eastern"))
                start_time_et = game_dt_et.strftime("%-I:%M %p ET")

                games.append({
                    "matchup": matchup,
                    "pitchers": pitchers,
                    "start_time_et": start_time_et
                })

            except Exception as e:
                if debug:
                    print("⚠️ Error parsing game:", e)
                continue

    if debug:
        print(f"✅ Found {len(games)} MLB games on {today_str}")
        for g in games:
            print(g)

    return games
