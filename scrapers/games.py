import requests
from datetime import datetime
import pytz

def fetch_today_matchups():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=" + datetime.now().strftime("%Y-%m-%d")
    resp = requests.get(url)
    data = resp.json()

    games = []

    for date in data.get("dates", []):
        for game in date.get("games", []):
            teams = game.get("teams", {})
            home = teams.get("home", {}).get("team", {}).get("name", "TBD")
            away = teams.get("away", {}).get("team", {}).get("name", "TBD")

            home_pitcher = teams.get("home", {}).get("probablePitcher", {}).get("fullName", "TBD")
            away_pitcher = teams.get("away", {}).get("probablePitcher", {}).get("fullName", "TBD")

            start_time_utc = game.get("gameDate")
            start_time_et = "TBD"
            if start_time_utc:
                try:
                    dt = datetime.strptime(start_time_utc, "%Y-%m-%dT%H:%M:%SZ")
                    et = pytz.utc.localize(dt).astimezone(pytz.timezone("US/Eastern"))
                    start_time_et = et.strftime("%-I:%M %p ET")
                except:
                    pass

            games.append({
                "matchup": f"{away} @ {home}",
                "pitchers": f"{away_pitcher} vs {home_pitcher}",
                "start_time_et": start_time_et
            })

    return games
import requests
from datetime import datetime
import pytz

def fetch_today_matchups(debug=False):
    eastern = pytz.timezone("US/Eastern")
    now_et = datetime.now(eastern)
    today_str = now_et.strftime("%Y-%m-%d")

    # Pull start times from MLB schedule
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}"
    schedule_resp = requests.get(schedule_url)
    schedule_data = schedule_resp.json()

    game_times = {}
    for date_block in schedule_data.get("dates", []):
        for game in date_block.get("games", []):
            game_id = game.get("gamePk")
            home_team = game["teams"]["home"]["team"]["name"]
            away_team = game["teams"]["away"]["team"]["name"]
            raw_time = game["gameDate"]
            game_dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
            game_dt_et = pytz.utc.localize(game_dt).astimezone(eastern)
            game_times[(away_team, home_team)] = game_dt_et.strftime("%-I:%M %p ET")

    # Pull pitcher info from Baseball Savant
    savant_url = "https://baseballsavant.mlb.com/probable-pitchers.json"
    savant_resp = requests.get(savant_url)
    savant_data = savant_resp.json()

    games = []
    for entry in savant_data:
        if entry.get("game_date") != today_str:
            continue

        away = entry.get("away_team", "")
        home = entry.get("home_team", "")
        away_pitcher = entry.get("away_probable_pitcher", "TBD")
        home_pitcher = entry.get("home_probable_pitcher", "TBD")

        matchup = f"{away} @ {home}"
        pitchers = f"{away_pitcher} vs {home_pitcher}"
        start_time_et = game_times.get((away, home), "TBD")

        games.append({
            "matchup": matchup,
            "pitchers": pitchers,
            "start_time_et": start_time_et
        })

    if debug:
        print(f"✅ Fetched {len(games)} live MLB matchups")
        for g in games:
            print(g)

    return games
