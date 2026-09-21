import requests
import streamlit as st

BASE_URL = "https://api.pulsescore.net/api/v3/bet365"

API_KEY = st.secrets["PULSESCORE_API_KEY"]


def get_live_soccer_events(limit=10):

    headers = {
        "X-Secret": API_KEY,
        "Accept-Encoding": "gzip"
    }

    url = (
        f"{BASE_URL}/live-events"
        f"?page=1&limit={limit}&sport=soccer"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    if response.status_code == 200:

        data = response.json()

        return data.get(
            "events",
            []
        )

    return []

def get_event_details(event_id):

    headers = {
        "X-Secret": API_KEY,
        "Accept-Encoding": "gzip"
    }

    url = (
        f"{BASE_URL}"
        f"/live-events/events/{event_id}"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    if response.status_code == 200:

        return response.json()

    return {}
