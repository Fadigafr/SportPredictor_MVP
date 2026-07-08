import streamlit as st
import pandas as pd

from database import init_db
from auth import login
from admin import admin_page
from predictions import predictions_page
from api_football import api_get

init_db()

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

if "user" not in st.session_state:
    st.session_state.user = None

login()

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🔴 Matchs Live",
        "📅 Calendrier",
        "🏆 Compétitions",
        "📊 Classements",
        "👥 Joueurs",
        "🎯 Top Buteurs",
        "⚔️ H2H",
        "📈 Prédictions",
        "👑 Admin"
    ]
)

if menu == "🏠 Accueil":

    st.title(
        "🏆 SPORT PREDICTOR ULTRA PRO 2026"
    )

elif menu == "🔴 Matchs Live":

    st.title("🔴 Matchs Live")

    data = api_get(
        "https://v3.football.api-sports.io/fixtures?live=all"
    )

    rows=[]

    for m in data.get("response",[]):

        rows.append({
            "Match":
            f"{m['teams']['home']['name']} vs {m['teams']['away']['name']}",

            "Score":
            f"{m['goals']['home']}-{m['goals']['away']}"
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

elif menu == "📅 Calendrier":

    st.title("📅 Calendrier")

elif menu == "🏆 Compétitions":

    st.title("🏆 Compétitions")

elif menu == "📊 Classements":

    st.title("📊 Classements")

elif menu == "👥 Joueurs":

    st.title("👥 Joueurs")

elif menu == "🎯 Top Buteurs":

    st.title("🎯 Top Buteurs")

elif menu == "⚔️ H2H":

    st.title("⚔️ H2H")

elif menu == "📈 Prédictions":

    predictions_page()

elif menu == "👑 Admin":

    admin_page()
