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

        if response.status_code != 200:

            st.error(
                f"Erreur API {response.status_code}"
            )

            return {
                "response": []
            }

        return response.json()

    except Exception as e:

        st.error(
            f"Erreur API : {e}"
        )

        return {
            "response": []
        }

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

st.write(response.status_code)
