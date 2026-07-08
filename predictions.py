import streamlit as st
import pandas as pd

from api_football import api_get

def predictions_page():

    st.header("📈 Centre de Prédictions")

    module = st.selectbox(
        "Module",
        [
            "🏆 Sélection Match",
            "💰 Cotes",
            "📊 Statistiques",
            "⚽ Over/Under",
            "✅ BTTS",
            "🎲 Score Exact",
            "🤖 Analyse IA"
        ]
    )

    if module == "🏆 Sélection Match":

        leagues = api_get(
            "https://v3.football.api-sports.io/leagues"
        )

        st.write(
            f"{len(leagues.get('response',[]))} compétitions trouvées"
        )

    elif module == "💰 Cotes":

        st.subheader("💰 Cotes Bookmakers")

    elif module == "📊 Statistiques":

        st.subheader("📊 Statistiques Match")

    elif module == "⚽ Over/Under":

        st.subheader("⚽ Over / Under")

    elif module == "✅ BTTS":

        st.subheader("✅ BTTS")

    elif module == "🎲 Score Exact":

        st.subheader("🎲 Score Exact Poisson")

    elif module == "🤖 Analyse IA":

        st.subheader("🤖 Analyse IA")
