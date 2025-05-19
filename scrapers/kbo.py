import requests
from bs4 import BeautifulSoup

def fetch_kbo_matchups():
    url = "https://mykbostats.com/schedule"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []

    rows = soup.select("table tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        matchup = cells[0].text.strip()
        pitchers = cells[2].text.strip()

        if "vs" not in pitchers or "TBD" in pitchers:
            continue

        try:
            start_time = cells[1].text.strip()
        except:
            start_time = "TBD"

        games.append({
            "matchup": matchup,
            "pitchers": pitchers,
            "start_time_et": start_time,
            "projected_flow": "Even early. Edge to bullpen depth late."
        })

    return games

