import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]

def api_get(url):

    headers = {
        "x-apisports-key": API_KEY
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    return response.json()
st.write(response.status_code)
st.write(response.text[:500])
