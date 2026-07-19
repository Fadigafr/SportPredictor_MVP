import requests
import streamlit as st
from datetime import datetime

API_KEY = st.secrets["API_FOOTBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.basketball.api-sports.io"


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

def get_team_statistics(team_id, season):

    url = (
        f"{BASE_URL}/teams/statistics"
        f"?id={team_id}"
        f"&season={season}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return None
