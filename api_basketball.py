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
