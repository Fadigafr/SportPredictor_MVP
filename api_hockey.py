import requests
import streamlit as st
from datetime import datetime

API_KEY = st.secrets["API_FOOTBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.hockey.api-sports.io"

def get_hockey_games():

    today = datetime.now().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/games?date={today}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    return response.json()

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

    return response.json()

def get_games_today():

    data = get_hockey_games()

    if "response" in data:
        return data["response"]

    return []
