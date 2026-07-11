import requests
import streamlit as st

API_KEY = st.secrets["5e4720fc37318c8dd95d856f2aaaebb1"]

def api_get(url):

    try:

        headers = {
            "x-apisports-key": API_KEY
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        return response.json()

    except Exception as e:

        st.error(f"Erreur API : {e}")

        return {
            "response": []
        }
