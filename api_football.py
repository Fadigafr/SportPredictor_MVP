import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]

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

        st.error(str(e))

        return {"response": []}
