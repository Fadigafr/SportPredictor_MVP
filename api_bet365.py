import requests
import streamlit as st

# =====================================
# CONFIGURATION
# =====================================

API_KEY = st.secrets["RAPIDAPI_KEY"]

BASE_URL = "https://bet365data.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "bet365data.p.rapidapi.com"
}

# =====================================
# REQUETE GENERIQUE
# =====================================

def api_get(endpoint):

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:

        return {
            "status": response.status_code,
            "body": response.text
        }

    return response.json()

def get_live_events_sports():

    return api_get(
        "/live-events/sports"
    )

# =====================================
# NORMALISATION STATUT
# =====================================

def get_status(event):

    live = str(
        event.get("live", "0")
    )

    su = str(
        event.get("SU", "0")
    )

    if live == "0":

        return "NS"

    if su == "1":

        return "FT"

    return "LIVE"


# =====================================
# NORMALISATION FOOTBALL
# =====================================

def normalize_soccer_event(event):

    return {

        "sport": "Football",

        "fixture_id":
        event.get("fi"),

        "home":
        event.get("home"),

        "away":
        event.get("away"),

        "league":
        event.get("league"),

        "score":
        event.get("SS", "0-0"),

        "status":
        get_status(event),

        "raw":
        event
    }


# =====================================
# NORMALISATION HOCKEY
# =====================================

def normalize_hockey_event(event):

    return {

        "sport": "Hockey",

        "fixture_id":
        event.get("fi"),

        "home":
        event.get("home"),

        "away":
        event.get("away"),

        "league":
        event.get("league"),

        "score":
        event.get("SS", "0-0"),

        "status":
        get_status(event),

        "raw":
        event
    }


# =====================================
# NORMALISATION BASKETBALL
# =====================================

def normalize_basketball_event(event):

    return {

        "sport": "Basketball",

        "fixture_id":
        event.get("fi"),

        "home":
        event.get("home"),

        "away":
        event.get("away"),

        "league":
        event.get("league"),

        "score":
        event.get("SS", "0-0"),

        "status":
        get_status(event),

        "raw":
        event
    }


# =====================================
# NORMALISATION TENNIS
# =====================================

def normalize_tennis_event(event):

    return {

        "sport": "Tennis",

        "fixture_id":
        event.get("fi"),

        "player_1":
        event.get("home"),

        "player_2":
        event.get("away"),

        "tournament":
        event.get("league"),

        "sets":
        event.get("SS", ""),

        "status":
        get_status(event),

        "raw":
        event
    }


# =====================================
# FOOTBALL LIVE
# =====================================

def get_soccer_live():

    data = api_get(
        "/live-events?sport=soccer"
    )

    if "data" not in data:

        return []

    events = data["data"]["events"]

    return [
        normalize_soccer_event(e)
        for e in events
    ]

# =====================================
# HOCKEY LIVE
# =====================================

def get_hockey_live():

    data = api_get(
        "/live-events?sport=ice hockey"
    )

    if not data.get("data"):
        return []

    events = data["data"]["events"]

    return [
        normalize_hockey_event(e)
        for e in events
    ]

# =====================================
# BASKETBALL LIVE
# =====================================

def get_basketball_live():

    data = api_get(
        "/live-events?sport=basketball"
    )

    if not data.get("data"):
        return []

    events = data["data"]["events"]

    return [
        normalize_basketball_event(e)
        for e in events
    ]

# =====================================
# TENNIS LIVE
# =====================================

def normalize_tennis_event(event):

    return {

        "sport": "Tennis",

        "fixture_id":
        event.get("fi"),

        "home":
        event.get("home"),

        "away":
        event.get("away"),

        "league":
        event.get("league"),

        "score":
        event.get("SS", ""),

        "status":
        get_status(event),

        "raw":
        event
    }

def get_tennis_live():

    data = api_get(
        "/live-events?sport=tennis"
    )

    if not data.get("data"):
        return []

    events = data["data"]["events"]

    return [
        normalize_tennis_event(e)
        for e in events
    ]

# =====================================
# MATCH TERMINE ?
# =====================================

def is_finished(event):

    return (
        str(
            event.get("raw", {})
            .get("SU", "0")
        ) == "1"
    )


# =====================================
# SCORE FOOTBALL
# =====================================

def get_score(event):

    score = event.get(
        "score",
        "0-0"
    )

    try:

        home_score = int(
            score.split("-")[0]
        )

        away_score = int(
            score.split("-")[1]
        )

        return (
            home_score,
            away_score
        )

    except:

        return (
            0,
            0
        )

# =====================================
# CALENDRIER ET COMPÉTITIONS
# =====================================

def get_soccer_leagues():

    return api_get(
        "/leagues?take=1000&from=0&sport=soccer"
    )


def normalize_soccer_fixture(
    event,
    league_name
):

    return {

        "fixture_id":
        event.get("fi"),

        "home":
        event.get("home"),

        "away":
        event.get("away"),

        "league":
        league_name,

        "date":
        event.get("bc"),

        "odds":
        event.get("outcomes", []),

        "raw":
        event

    }


def get_soccer_calendar():

    data = get_soccer_leagues()

    fixtures = []

    for league in data.get(
        "leagues",
        []
    ):

        league_name = league.get(
            "leagueName",
            "Unknown"
        )

        for event in league.get(
            "events",
            []
        ):

            fixtures.append(

                normalize_soccer_fixture(
                    event,
                    league_name
                )

            )

    return fixtures
