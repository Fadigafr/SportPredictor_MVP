import streamlit as st
import pandas as pd
import os

from auth import login
from admin import admin_page
from predictions import predictions_page
from api_football import api_get
from database import init_db

init_db()

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO IA",
    page_icon="🏆",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0D1117,
        #111827,
        #0F172A
    );
}

h1,h2,h3{
    color:#FFD700;
}

</style>
""", unsafe_allow_html=True)

login()

# =====================================================
# SIDEBAR
# =====================================================

logo_path = "assets/logo.png"

if os.path.exists(logo_path):
    st.sidebar.image(
        logo_path,
        width=180
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image(
            logo_path,
            width=220
        )

st.sidebar.title("SPORT PREDICTOR")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Accueil",
        "Matchs Live",
        "Calendrier",
        "Analyse IA du Jour",
        "Classements",
        "Joueurs",
        "Top Buteurs",
        "H2H",
        "Prédictions",
        "Admin"
    ]
)

# =====================================================
# ACCUEIL
# =====================================================

if menu == "Accueil":

    st.title(
        "SPORT PREDICTOR ULTRA PRO IA"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Précision IA", "78%")
    c2.metric("Ligues", "500+")
    c3.metric("Matchs", "10 000+")
    c4.metric("Prédictions", "24 000+")

    st.markdown("---")

    st.subheader(
        "Bienvenue"
    )

    st.info("""
Analyse avancée :

• H2H

• BTTS

• Over/Under

• Score Exact

• Buteurs

• Cotes Bookmakers

• Intelligence Artificielle
""")

# =====================================================
# MATCHS LIVE
# =====================================================

elif menu == "Matchs Live":

    st.title("Matchs Live")

    data = api_get(
        "https://v3.football.api-sports.io/fixtures?live=all"
    )

    rows = []

    for m in data.get("response", []):

        rows.append({
            "Match":
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}",

            "Score":
            f"{m['goals']['home']} - "
            f"{m['goals']['away']}",

            "Minute":
            m["fixture"]["status"]["elapsed"],

            "Compétition":
            m["league"]["name"]
        })

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch"
        )

    else:

        st.warning(
            "Aucun match en direct."
        )

# =====================================================
# CALENDRIER ET COMPÉTITIONS
# =====================================================

elif menu == "Calendrier":

    st.title("📅 Calendrier")

    competitions = {

    # ANGLETERRE
    "England - Premier League": 39,
    "England - Championship": 40,
    "England - FA Cup": 45,
    "England - EFL Cup": 48,

    # ESPAGNE
    "Spain - La Liga": 140,
    "Spain - Segunda": 141,
    "Spain - Copa del Rey": 143,

    # ITALIE
    "Italy - Serie A": 135,
    "Italy - Serie B": 136,
    "Italy - Coppa Italia": 137,

    # ALLEMAGNE
    "Germany - Bundesliga": 78,
    "Germany - Bundesliga 2": 79,
    "Germany - DFB Pokal": 81,

    # FRANCE
    "France - Ligue 1": 61,
    "France - Ligue 2": 62,
    "France - Coupe de France": 66,

    # PORTUGAL
    "Portugal - Primeira Liga": 94,

    # PAYS-BAS
    "Netherlands - Eredivisie": 88,

    # BELGIQUE
    "Belgium - Jupiler Pro League": 144,

    # TURQUIE
    "Turkey - Super Lig": 203,

    # ECOSSE
    "Scotland - Premiership": 179,

    # SUISSE
    "Switzerland - Super League": 207,

    # AUTRICHE
    "Austria - Bundesliga": 218,

    # DANEMARK
    "Denmark - Superliga": 119,

    # NORVEGE
    "Norway - Eliteserien": 103,

    # SUEDE
    "Sweden - Allsvenskan": 113,

    # BRESIL
    "Brazil - Serie A": 71,
    "Brazil - Serie B": 72,
    "Brazil - Copa do Brasil": 76,

    # ARGENTINE
    "Argentina - Liga Profesional": 128,

    # MLS
    "USA - Major League Soccer": 253,

    # ARABIE SAOUDITE
    "Saudi Arabia - Pro League": 307,

    # AFRIQUE
    "CAF Champions League": 12,
    "CAF Confederation Cup": 20,
    "Africa Cup of Nations": 6,

    # INTERNATIONAL
    "UEFA Champions League": 2,
    "UEFA Europa League": 3,
    "UEFA Conference League": 848,
    "UEFA Nations League": 5,
    "Euro Championship": 4,
    "FIFA World Cup": 1,
    "World Cup Qualification Europe": 32,

    # AMERIQUE DU SUD
    "Copa Libertadores": 13,
    "Copa Sudamericana": 11,
    "Copa America": 9
}

    competition = st.selectbox(
    "🏆 Compétition",
    sorted(competitions.keys())
)


    league_id = competitions[competition]

    fixtures = api_get(
        f"https://v3.football.api-sports.io/fixtures?league={league_id}&next=50"
    )

    response = fixtures.get("response", [])

    if response:

        matchs = {}

        for match in response:

            fixture_id = match["fixture"]["id"]

            match_name = (
                f"{match['fixture']['date'][:16]} | "
                f"{match['teams']['home']['name']} vs "
                f"{match['teams']['away']['name']}"
            )

            matchs[match_name] = fixture_id

        selected_match = st.selectbox(
            "⚽ Match",
            list(matchs.keys())
        )

        if st.button("Analyser"):

            st.session_state["fixture_id"] = matchs[selected_match]

            st.success(
                f"Match sélectionné : {selected_match}"
            )

    else:

        st.warning(
            "Aucun match trouvé."
        )
        
# =====================================================
# ANALYSE IA DU JOUR
# =====================================================

elif menu == "Analyse IA du Jour":

    st.title("Top 5 Analyses IA")

    analyses = [

        {
            "match": "Liverpool vs Arsenal",
            "confidence": 82,
            "score": "2-1"
        },

        {
            "match": "Real Madrid vs Atletico",
            "confidence": 80,
            "score": "2-0"
        },

        {
            "match": "Bayern vs Dortmund",
            "confidence": 79,
            "score": "3-1"
        },

        {
            "match": "PSG vs Marseille",
            "confidence": 78,
            "score": "2-1"
        },

        {
            "match": "Inter vs Milan",
            "confidence": 76,
            "score": "1-1"
        }

    ]

    for a in analyses:

        st.markdown("---")

        st.subheader(
            a["match"]
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Confiance",
            f"{a['confidence']}%"
        )

        c2.metric(
            "Score IA",
            a["score"]
        )
# =====================================================
# CLASSEMENTS
# =====================================================

elif menu == "Classements":

    st.title(
        "Classements"
    )

    st.info(
        "Module standings à connecter."
    )

# =====================================================
# JOUEURS
# =====================================================

elif menu == "Joueurs":

    st.title("Joueurs")

    st.info(
        "Module joueurs."
    )

# =====================================================
# BUTEURS
# =====================================================

elif menu == "Top Buteurs":

    st.title("Top Buteurs")

    st.info(
        "Module buteurs."
    )

# =====================================================
# H2H
# =====================================================

elif menu == "H2H":

    st.title(
        "Historique H2H"
    )

    st.info(
        "Module H2H."
    )

# =====================================================
# PREDICTIONS
# =====================================================

elif menu == "Prédictions":

    predictions_page()

# =====================================================
# ADMIN
# =====================================================

elif menu == "Admin":

    admin_page()
