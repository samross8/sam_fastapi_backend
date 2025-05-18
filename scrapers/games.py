import requests
from datetime import datetime
import pytz

def fetch_today_matchups():
    url = "https://baseballsavant.mlb.com/probable-pitchers.json"
    response = requests.get(url)
    data = response.json()

    # Get current date in US/Eastern to match the format in JSON
    eastern = pytz.timezone("US/Eastern")
    today_et = datetime.now(eastern).strftime("%Y-%m-%d")

    matchups = []

    for game in data.get("matchups", []):
        game_date = game.get("gameDate", "").split("T")[0]
        if game_date != today_et:
            continue  # skip non-today games

        away = game["awayProbablePitcher"]
        home = game["homeProbablePitcher"]

        matchup = {
            "matchup": f'{game["awayTeamName"]} @ {game["homeTeamName"]}',
            "pitchers": f'{away["firstName"][0]}. {away["lastName"]} vs {home["firstName"][0]}. {home["lastName"]}',
            "start_time_et": game["gameDateEasternTimeString"].replace(" ET", " ET"),
            "projected_flow": "Starting pitchers locked in. Flow projection pending full stack integration."
        }

        matchups.append(matchup)

    return matchups
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def fetch_today_matchups():
    url = "https://baseballsavant.mlb.com/probable-pitchers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    today = datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d")
    games = []

    rows = soup.find_all("div", class_="probable-pitcher-row")
    for row in rows:
        game_date = row.find("div", class_="probable-date-time").text.strip().split("•")[0].strip()
        if today not in game_date:
            continue

        teams = row.find("div", class_="probable-teams").text.strip().split("@")
        if len(teams) != 2:
            continue

        away_team = teams[0].strip()
        home_team = teams[1].strip()

        pitcher_blocks = row.find_all("div", class_="probable-pitcher")
        if len(pitcher_blocks) != 2:
            continue

        away_pitcher = pitcher_blocks[0].find("a").text.strip()
        home_pitcher = pitcher_blocks[1].find("a").text.strip()

        try:
            time_block = row.find("div", class_="probable-date-time").text.strip()
            time_str = time_block.split("•")[1].strip()
        except:
            time_str = "TBD"

        games.append({
            "matchup": f"{away_team} @ {home_team}",
            "pitchers": f"{away_pitcher} vs {home_pitcher}",
            "start_time_et": time_str
        })

    return games

