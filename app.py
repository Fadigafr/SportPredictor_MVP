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

st.markdown("""
<style>

/* Boutons */

.stButton > button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #FFD700,
        #FFB800
    );
    color: black;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    padding: 12px;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #FFF176,
        #FFD700
    );
    transform: scale(1.02);
}

/* Carte Match */

.match-card {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,215,0,0.3);
}

.match-title {
    color: #FFD700;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.match-date {
    text-align: center;
    color: white;
}

</style>
""",
unsafe_allow_html=True)

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

        "England - Premier League": {
            "id": 39,
            "logo": "https://media.api-sports.io/football/leagues/39.png"
        },

        "Spain - La Liga": {
            "id": 140,
            "logo": "https://media.api-sports.io/football/leagues/140.png"
        },

        "Italy - Serie A": {
            "id": 135,
            "logo": "https://media.api-sports.io/football/leagues/135.png"
        },

        "Germany - Bundesliga": {
            "id": 78,
            "logo": "https://media.api-sports.io/football/leagues/78.png"
        },

        "France - Ligue 1": {
            "id": 61,
            "logo": "https://media.api-sports.io/football/leagues/61.png"
        },

        "UEFA Champions League": {
            "id": 2,
            "logo": "https://media.api-sports.io/football/leagues/2.png"
        }

    }

    competition = st.selectbox(
        "🏆 Compétition",
        sorted(competitions.keys())
    )

    league_id = competitions[competition]["id"]

    st.image(
        competitions[competition]["logo"],
        width=120
    )

    fixtures = api_get(
        f"https://v3.football.api-sports.io/fixtures?league={league_id}&next=50"
    )

    response = fixtures.get("response", [])

    if response:

    for match in response:

        fixture_id = match["fixture"]["id"]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        home_logo = match["teams"]["home"]["logo"]
        away_logo = match["teams"]["away"]["logo"]

        league_logo = match["league"]["logo"]
        league_name = match["league"]["name"]

        date_match = match["fixture"]["date"][:16]

        st.image(
            league_logo,
            width=80
        )

        st.markdown(
            f"<h4 style='color:#FFD700'>{league_name}</h4>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns([1, 4, 1])

        with c1:
            st.image(home_logo, width=70)

        with c2:

            st.markdown(
                f"""
<div class='match-card'>

<p class='match-title'>
{home} vs {away}
</p>

<p class='match-date'>
📅 {date_match}
</p>

</div>
""",
                unsafe_allow_html=True
            )

        with c3:
            st.image(away_logo, width=70)

        if st.button(
            f"🔍 Analyser {home} vs {away}",
            key=f"fixture_{fixture_id}"
        ):

            st.session_state["fixture_id"] = fixture_id

            st.success(
                f"Match sélectionné : {home} vs {away}"
            )

        st.divider()

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
