import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

def api_get(url):

    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        return r.json()

    except:

        return {
            "response":[]
        }
