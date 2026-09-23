import requests
import streamlit as st

BASE_URL = "https://api.pulsescore.net/api/v3/bet365"

API_KEY = st.secrets["PULSESCORE_API_KEY"]

def get_upcoming_soccer_events(
    page=1,
    limit=20
):

    headers = {
        "X-Secret": API_KEY
    }

    url = (
        f"{BASE_URL}/events"
        f"?page={page}"
        f"&limit={limit}"
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

    return {

        "status_code": response.status_code,

        "url": url,

        "json": response.json()

    }

    return {}

def get_first_live_event():

    events = get_live_soccer_events(1)

    if events:

        return events[0]

    return None

def extract_match_result(event):

    if not isinstance(event, dict):

        return None

    teams = event.get(
        "moreInfo",
        {}
    ).get(
        "teams",
        []
    )

    if len(teams) < 2:

        return None

    home_score = int(
        teams[0].get(
            "score",
            0
        )
    )

    away_score = int(
        teams[1].get(
            "score",
            0
        )
    )

    if home_score > away_score:

        return "1"

    elif away_score > home_score:

        return "2"

    else:

        return "X"

def generate_calendar_prediction(event):

    markets = event.get(
        "markets",
        []
    )

    for market in markets:

        if market.get(
            "canonicalMarket"
        ) == "MATCH_RESULT":

            selections = market.get(
                "selections",
                []
            )

            if len(selections) < 3:
                continue

            best = min(
                selections,
                key=lambda x: x.get(
                    "odds",
                    999
                )
            )

            outcome = best.get(
                "canonicalOutcome"
            )

            if outcome == "HOME":

                prediction = "1"

            elif outcome == "DRAW":

                prediction = "X"

            else:

                prediction = "2"

            confidence = max(
                60,
                min(
                    95,
                    int(
                        100 / best.get(
                            "odds",
                            2
                        )
                    )
                    * 2
                )
            )

            return {

                "prediction":
                prediction,

                "ai_index":
                confidence

            }

    return {

        "prediction": "X",

        "ai_index": 50
    }
