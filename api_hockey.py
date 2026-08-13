import requests
import streamlit as st
from datetime import datetime

API_KEY = st.secrets["API_FOOTBALL_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v1.hockey.api-sports.io"

def api_get_hockey(endpoint):

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    return response.json()

def get_hockey_games_by_date(
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

def get_hockey_games():

    today = datetime.now().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/games?date={today}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    return response.json()

def get_games_today():

    data = get_hockey_games()

    if "response" in data:
        return data["response"]

    return []

def get_hockey_fixtures():

    try:

        return get_games_today()

    except Exception:

        return []

def get_hockey_fixture_by_id(
    fixture_id
):

    data = api_get_hockey(
        f"/games?id={fixture_id}"
    )

    if not data:
        return None

    response = data.get(
        "response",
        []
    )

    if not response:
        return None

    return response[0]
