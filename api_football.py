import requests
import streamlit as st

API_KEY = "VOTRE_CLE"

def api_get(url):

    headers = {
        "x-apisports-key": API_KEY
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    return r.json()

    except:

        return {
            "response":[]
        }
