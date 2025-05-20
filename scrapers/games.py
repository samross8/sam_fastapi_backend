import requests
from datetime import datetime
import pytz

def fetch_today_matchups(debug=False):
    eastern = pytz.timezone("US/Eastern")
    now_et = datetime.now(eastern)
    today_str = now_et.strftime("%Y-%m-%d")

    # Pull start times from MLB schedule
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}"
    try:
        schedule_resp = requests.get(schedule_url)
        schedule_data = schedule_resp.json()
    except Exception as e:
        if debug:
            print("❌ Error fetching schedule:", e)
        return []

    game_times = {}
    for date_block in schedule_data.get("dates", []):
        for game in date_block.get("games", []):
            home_team = game["teams"]["home"]["team"]["name"]
            away_team = game["teams"]["away"]["team"]["name"]
            raw_time = game["gameDate"]
            try:
                game_dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
                game_dt_et = pytz.utc.localize(game_dt).astimezone(eastern)
                game_times[(away_team, home_team)] = game_dt_et.strftime("%-I:%M %p ET")
            except Exception as e:
                if debug:
                    print("⚠️ Error parsing time:", e)

    # Pull pitcher info from Baseball Savant
    savant_url = "https://baseballsavant.mlb.com/probable-pitchers.json"
    try:
        savant_resp = requests.get(savant_url)
        savant_data = savant_resp.json()
    except Exception as e:
        if debug:
            print("❌ Error fetching savant data:", e)
        return []

    games = []
    for entry in savant_data:
        game_date = entry.get("game_date", "")
        try:
            parsed_date = datetime.strptime(game_date, "%Y-%m-%d").date()
            if abs((parsed_date - now_et.date()).days) > 1:
                continue
        except:
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
        print(f"✅ Fetched {len(games)} matchups for ±1 day of {today_str}")
        for g in games:
            print(g)

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
    try:
        schedule_resp = requests.get(schedule_url)
        schedule_data = schedule_resp.json()
    except Exception as e:
        if debug:
            print("❌ Error fetching schedule:", e)
        return []

    game_times = {}
    for date_block in schedule_data.get("dates", []):
        for game in date_block.get("games", []):
            home_team = game["teams"]["home"]["team"]["name"]
            away_team = game["teams"]["away"]["team"]["name"]
            raw_time = game["gameDate"]
            try:
                game_dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
                game_dt_et = pytz.utc.localize(game_dt).astimezone(eastern)
                game_times[(away_team, home_team)] = game_dt_et.strftime("%-I:%M %p ET")
            except Exception as e:
                if debug:
                    print("⚠️ Error parsing time:", e)

    # Pull pitcher info from Baseball Savant
    savant_url = "https://baseballsavant.mlb.com/probable-pitchers.json"
    try:
        savant_resp = requests.get(savant_url)
        savant_data = savant_resp.json()
    except Exception as e:
        if debug:
            print("❌ Error fetching savant data:", e)
        return []

    games = []
    for entry in savant_data:
        game_date = entry.get("game_date", "")
        try:
            parsed_date = datetime.strptime(game_date, "%Y-%m-%d").date()
            if abs((parsed_date - now_et.date()).days) > 1:
                continue
        except:
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
        print(f"✅ Fetched {len(games)} matchups for ±1 day of {today_str}")
        for g in games:
            print(g)

    return games
