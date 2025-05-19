import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

url = "https://www.mlb.com/probable-pitchers"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

games = soup.select("section.probable-pitchers__matchup")

now_et = datetime.now(pytz.timezone("US/Eastern"))

print("\nTarget Date:", now_et.strftime("%A, %B %d"))

for game in games:
    try:
        # Try direct header grab first
        header = game.find("h2")
        if header:
            date_header = header.text.strip()
        else:
            date_header = game.get("data-date", "Unknown Date").strip()

        # Check if date matches today
        if now_et.strftime("%B %d").lower() not in date_header.lower():
            continue

        teams = game.select_one(".probable-pitchers__matchup__team--desktop")
        if teams:
            teams = teams.text.strip()
        else:
            continue

        pitchers = game.select(".probable-pitchers__pitcher-name")
        pitcher_names = [p.text.strip() for p in pitchers if p.text.strip()]
        pitcher_str = " vs ".join(pitcher_names)

        game_time_raw = game.select_one(".probable-pitchers__game-time").text.strip()
        game_time = datetime.strptime(game_time_raw, "%I:%M %p")
        game_time = game_time.replace(year=now_et.year, month=now_et.month, day=now_et.day)
        game_time = pytz.timezone("US/Eastern").localize(game_time)

        status = "(LIVE or upcoming)" if game_time >= now_et else "(already started)"
        print(f"{teams} | {pitcher_str} | {game_time.strftime('%I:%M %p ET')} {status}")
    except Exception as e:
        print("Error parsing a matchup:", e)
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz

url = "https://www.lineups.com/mlb/lineups"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

games = soup.select(".lineup")

now_et = datetime.now(pytz.timezone("US/Eastern"))

for game in games:
    try:
        teams = game.select_one(".lineup__teams").text.strip()
        pitchers = game.select_one(".lineup__pitchers").text.strip()
        game_time_raw = game.select_one(".lineup__time").text.strip()

        game_time = datetime.strptime(game_time_raw, "%I:%M %p")
        game_time = game_time.replace(year=now_et.year, month=now_et.month, day=now_et.day)
        game_time = pytz.timezone("US/Eastern").localize(game_time)

        status = "(LIVE or upcoming)" if game_time >= now_et else "(already started)"

        print(f"{teams} | {pitchers} | {game_time.strftime('%I:%M %p ET')} {status}")

    except Exception as e:
        print(f"Error scraping game: {e}")
        continue
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz

url = "https://www.lineups.com/mlb/lineups"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

games = soup.select(".lineup")

now_et = datetime.now(pytz.timezone("US/Eastern"))

for game in games:
    try:
        date_header_el = game.find_previous("h2")
        if not date_header_el:
            print("⚠️  Skipping game – no date header found")
            continue

        date_header = date_header_el.text.strip()

        if "May 18" not in date_header:
            continue

        teams = game.select_one(".lineup__teams").text.strip()
        pitchers = game.select_one(".lineup__pitchers").text.strip()
        game_time_raw = game.select_one(".lineup__time").text.strip()

        game_time = datetime.strptime(game_time_raw, "%I:%M %p")
        game_time = game_time.replace(year=now_et.year, month=now_et.month, day=now_et.day)
        game_time = pytz.timezone("US/Eastern").localize(game_time)

        status = "(LIVE or upcoming)" if game_time >= now_et else "(already started)"

        print(f"{teams} | {pitchers} | {game_time.strftime('%I:%M %p ET')} {status}")

    except Exception as e:
        print(f"Error scraping game: {e}")
        continue
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup

url = "https://www.mlb.com/probable-pitchers"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

today = datetime.now(pytz.timezone("US/Eastern")).strftime("%A, %B %d")
print(f"🔍 Target Date: {today}")

games = []
for game in soup.select(".probable-pitchers__game"):
    date_header = game.find_previous("h2").text.strip()
    if date_header != today:
        continue

    teams = [el.text.strip() for el in game.select(".probable-pitchers__team-name")]
    pitchers = [el.text.strip() for el in game.select(".probable-pitchers__pitcher-name")]

    if len(teams) != 2 or len(pitchers) != 2:
        continue

    games.append({
        "matchup": f"{teams[0]} @ {teams[1]}",
        "pitchers": f"{pitchers[0]} vs {pitchers[1]}",
        "start_time_et": "TBD",
        "projected_flow": "Flow logic coming next"
    })

for g in games:
    print(f"{g['matchup']} | {g['pitchers']} | {g['start_time_et']}")
import requests
from bs4 import BeautifulSoup

url = "https://www.lineups.com/mlb/lineups"
res = requests.get(url)
html = res.text

print(html[:1000])  # First 1000 characters
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

url = "https://www.lineups.com/mlb/lineups"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

matchups = soup.select(".Row-dp6gg3-0.hVGHpz")
now_et = datetime.now(pytz.timezone("US/Eastern"))

for m in matchups:
    teams = m.select_one(".TeamContainer-dp6gg3-2").text.strip()
    pitchers = m.select_one(".Pitchers-dp6gg3-7").text.strip()
    time_tag = m.select_one(".MatchupInfo-dp6gg3-6")
    game_time_raw = time_tag.text.strip() if time_tag else "N/A"

    print(f"🟢 MATCHUP FOUND")
    print(f"Teams: {teams}")
    print(f"Pitchers: {pitchers}")
    print(f"Time Raw: {game_time_raw}")
    print("--------")
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

url = "https://www.lineups.com/mlb/lineups"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

games = soup.select(".game-card")

now_et = datetime.now(pytz.timezone("US/Eastern"))

for game in games:
    teams = game.select_one(".card-header").get_text(strip=True)
    pitchers_raw = game.select(".player-name")
    game_time_raw = game.select_one(".start-time").get_text(strip=True)

    try:
        game_time = datetime.strptime(game_time_raw, "%I:%M %p")
        game_time = game_time.replace(year=now_et.year, month=now_et.month, day=now_et.day)
        game_time = pytz.timezone("US/Eastern").localize(game_time)
    except Exception as e:
        print(f"Invalid time '{game_time_raw}' for {teams}")
        continue

    status = "(LIVE or upcoming)" if game_time >= now_et else "(already started)"

    pitchers = " vs ".join(p.get_text(strip=True) for p in pitchers_raw)
    print(f"{teams} | {pitchers} | {game_time.strftime('%I:%M %p ET')} {status}")

