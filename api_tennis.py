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
