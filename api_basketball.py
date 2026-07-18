import requests
import streamlit as st

API_KEY = st.secrets["API_BASKETBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.basketball.api-sports.io"

def get_games_today():

    url = f"{BASE_URL}/games"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        data = response.json()

        return data.get("response", [])

    return []

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
