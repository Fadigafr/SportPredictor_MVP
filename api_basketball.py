import requests
import streamlit as st
from datetime import datetime

API_KEY = st.secrets["API_FOOTBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.basketball.api-sports.io"

print("✅ api_basketball chargé")


def basketball_calendar_page():

    st.title("🏀 Calendrier Basketball")

    games = get_basketball_fixtures()

    if not games:

        st.warning(
            "⚠️ Aucun match Basketball disponible"
        )
        return

    for game in games:

        try:

            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]

            st.success(
                f"🏀 {home} vs {away}"
            )

        except Exception:

            st.write(game)
        
def get_games_today():

    today = datetime.utcnow().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/games?date={today}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    data = response.json()

    return data.get("response", [])

def get_standings(league_id, season):

    url = (
        f"{BASE_URL}/standings"
        f"?league={league_id}"
        f"&season={season}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return None

def get_team_statistics(
    team_id,
    league_id,
    season
):

    url = (
        f"{BASE_URL}/statistics"
        f"?team={team_id}"
        f"&league={league_id}"
        f"&season={season}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return None

def get_basketball_fixtures():

    try:

        return get_games_today()

    except Exception:

        return []

def get_basketball_games_by_date(
    selected_date
):

    url = (
        f"{BASE_URL}/games"
        f"?date={selected_date}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    return response.json()

   print("✅ get_basketball_games_by_date disponible")
