import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup

def fetch_today_matchups():
    url = "https://baseballsavant.mlb.com/probable-pitchers"
    response = requests.get(url)
    html = response.text

    games = []

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.probable-pitchers-table tbody tr")

    for row in rows:
        try:
            teams = row.select_one("td.colspan-td span.teams").get_text(strip=True)
            pitchers = row.select_one("td[data-stat='probable_pitchers']").get_text(strip=True)
            raw_time = row.select_one("td[data-stat='game_date']").get_text(strip=True)

            # Format game time into Eastern Time
            try:
                game_time = datetime.strptime(raw_time, "%I:%M %p")
                now = datetime.now(pytz.timezone("US/Eastern"))
                game_time = game_time.replace(year=now.year, month=now.month, day=now.day)
                start_time_et = game_time.strftime("%-I:%M %p ET")
            except:
                start_time_et = "TBD"

            games.append({
                "matchup": teams,
                "pitchers": pitchers,
                "start_time_et": start_time_et
            })

        except Exception:
            continue

    return games
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def fetch_today_matchups():
    url = "https://www.mlb.com/probable-pitchers"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    today = datetime.now(pytz.timezone("US/Eastern")).strftime("%A, %B %d")

    game_sections = soup.find_all("section", class_="p-pitcher-table__row")
    for game in game_sections:
        # Validate date header
        date_header = game.find_previous("h2")
        if not date_header or today not in date_header.text:
            continue

        # Extract teams
        teams = game.find_all("span", class_="team-name")
        if len(teams) != 2:
            continue
        away_team = teams[0].text.strip()
        home_team = teams[1].text.strip()
        matchup = f"{away_team} @ {home_team}"

        # Extract pitchers
        pitchers = game.find_all("span", class_="player-name")
        if len(pitchers) != 2:
            continue
        away_pitcher = pitchers[0].text.strip()
        home_pitcher = pitchers[1].text.strip()
        pitcher_text = f"{away_pitcher} vs {home_pitcher}"

        # Extract time (if available)
        time_cell = game.find("td", class_="probable-pitchers-table__time")
        if time_cell:
            raw_time = time_cell.text.strip()
            try:
                game_time = datetime.strptime(raw_time, "%I:%M %p")
                now = datetime.now(pytz.timezone("US/Eastern"))
                game_time = game_time.replace(year=now.year, month=now.month, day=now.day)
                start_time_et = game_time.strftime("%-I:%M %p ET")
            except:
                start_time_et = "TBD"
        else:
            start_time_et = "TBD"

        games.append({
            "matchup": matchup,
            "pitchers": pitcher_text,
            "start_time_et": start_time_et
        })

    return games
