import requests
import streamlit as st

API_KEY = st.secrets["API_FOOTBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.hockey.api-sports.io"

def get_hockey_games():

    url = f"{BASE_URL}/games"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {}
