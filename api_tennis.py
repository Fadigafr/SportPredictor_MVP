import requests
import streamlit as st

API_KEY = st.secrets["API_FOOTBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.tennis.api-sports.io"

def get_tennis_fixtures():

    url = f"{BASE_URL}/fixtures"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {}
