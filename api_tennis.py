import requests
import streamlit as st

API_KEY = st.secrets["RAPIDAPI_KEY"]

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "tennis-api-atp-wta-itf.p.rapidapi.com"
}

BASE_URL = "https://tennis-api-atp-wta-itf.p.rapidapi.com"

def get_all_fixtures():

    url = (
        f"{BASE_URL}/tennis/v2/atp/fixtures"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }

def tennis_calendar_page():

    st.title("📅 Calendrier Tennis")

    tennis_data = get_all_fixtures()

    if "error" in tennis_data:

        st.warning(
            "⚠️ Calendrier Tennis indisponible"
        )

        return

    matches = tennis_data.get("data", [])

    if not matches:

        st.info(
            "Aucun match disponible"
        )

        return

    for match in matches:

        player1 = match["player1"]["name"]
        player2 = match["player2"]["name"]

        st.info(
            f"🎾 {player1} vs {player2}"
        )
        
def get_tournament_fixtures():

    url = (
        f"{BASE_URL}/tennis/v2/atp/"
        "fixtures/tournament/19358"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }

def get_date_fixtures():

    url = (
        f"{BASE_URL}/tennis/v2/atp/"
        "fixtures/2024-02-07"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }

def get_h2h_fixtures(
    player1_id,
    player2_id
):

    url = (
        f"{BASE_URL}/tennis/v2/atp/"
        f"fixtures/h2h/"
        f"{player1_id}/"
        f"{player2_id}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }

def get_match_prediction(
    player1_name,
    player2_name
):

    player1_name = (
        player1_name
        .replace(" ", "")
        .replace("/", "")
    )

    player2_name = (
        player2_name
        .replace(" ", "")
        .replace("/", "")
    )

    url = (
        f"{BASE_URL}/tennis/v2/ms-api/"
        f"upcoming/match-prediction/atp/"
        f"{player1_name}/"
        f"{player2_name}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }

def get_singles_ranking():

    url = (
        f"{BASE_URL}/tennis/v2/atp/"
        "ranking/singles/"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }


def get_doubles_ranking():

    url = (
        f"{BASE_URL}/tennis/v2/atp/"
        "ranking/doubles/"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }

def get_player_profile(player_id):

    url = (
        f"{BASE_URL}/tennis/v2/player/"
        f"{player_id}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code == 200:

        return response.json()

    return {
        "error": response.text
    }
    
def get_player_recent_matches(player_id):

    url = (
        f"{BASE_URL}/getFixtures"
        f"?playerId={player_id}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    st.write("URL TEST :", url)
    st.write("STATUS :", response.status_code)

    if response.status_code == 200:
        return response.json()

    st.error(response.text)

    return {}

def calculate_form_stats(matches_data):

    matches = matches_data.get("data", [])

    wins = 0
    losses = 0
    form_sequence = []

    for match in matches[:5]:

        winner_id = match.get("winnerId")

        if winner_id:

            if winner_id == match.get("player1Id"):
                wins += 1
                form_sequence.append("W")
            else:
                losses += 1
                form_sequence.append("L")

    total = wins + losses

    win_rate = (
        round((wins / total) * 100, 1)
        if total > 0
        else 0
    )

    return {
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "form": "-".join(form_sequence)
    }
