import streamlit as st
import pandas as pd
import os

from auth import login
from admin import admin_page
from predictions import predictions_page
from predictions import (
    predictions_page,
    basketball_page,
    tennis_page,
    hockey_page
)
from api_football import api_get
from database import init_db
from api_basketball import get_basketball_games_today
from predictions import dashboard_global_page
from results_db import (
    validate_football_results,
    validate_hockey_results,
    validate_basketball_results,
    validate_football_results_bet365
)
from predictions import tennis_calendar_page
from predictions import basketball_calendar_page
from predictions import hockey_calendar_page
from api_bet365 import get_soccer_live
from api_bet365 import (
    get_live_events_sports
)
from api_bet365 import (
    get_soccer_live,
    get_basketball_live,
    get_hockey_live,
    get_tennis_live,
    get_soccer_calendar,
    get_soccer_event
)
from api_bet365 import get_match_odds
from datetime import datetime

if st.button("TEST VALIDATION BET365"):

    result = validate_football_results_bet365()

    st.success(
        f"Validation exécutée : {result}"
    )

if st.button("TEST EVENT"):

    st.json(
        get_soccer_event(
            "198646827"
        )
    )

init_db()

validate_football_results()
validate_hockey_results()
validate_basketball_results()

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
        "Dashboard IA Global",
        "Admin"
    ]
)

sport = st.sidebar.selectbox(
    "Sport",
    [
        "Football",
        "Basketball",
        "Tennis",
        "Hockey"
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

    if sport == "Football":
        matches = get_soccer_live()

    elif sport == "Basketball":
        matches = get_basketball_live()

    elif sport == "Tennis":
        matches = get_tennis_live()

    elif sport == "Hockey":
        matches = get_hockey_live()

    else:
        matches = []

    rows = []

    for m in matches:

        rows.append({

            "Match":
            f"{m['home']} vs {m['away']}",

            "Score":
            m["score"],

            "Statut":
            m["status"],

            "Compétition":
            m["league"]

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
# CALENDRIER & COMPÉTITIONS
# =====================================================

elif menu == "Calendrier":

    if sport == "Football":

        st.title("📅 Calendrier")

        fixtures = get_soccer_calendar()

        leagues = sorted(
            list(
                set(
                    f["league"]
                    for f in fixtures
                )
            )
        )

        league_filter = st.selectbox(
            "🏆 Compétition",
            ["Toutes"] + leagues
        )

        search_team = st.text_input(
            "🔍 Rechercher une équipe",
            placeholder="Ex: Botafogo, Arsenal, Lazio..."
        )
        
        if league_filter != "Toutes":

            fixtures = [

                f for f in fixtures

                if f["league"] == league_filter

            ]

        st.metric(
            "Matchs affichés",
            len(fixtures)
        )

        if search_team:

            fixtures = [

                f for f in fixtures

                if search_team.lower()
                in (
                    f["home"] +
                    " " +
                    f["away"]
                ).lower()

            ]

        fixtures.sort(
            key=lambda x: x["date"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Matchs",
                len(fixtures)
            )

        with col2:

            st.metric(
                "Compétitions",
                len(leagues)
            )

        if not fixtures:

            st.warning(
                "Aucun match trouvé."
            )

        else:

            for match in fixtures[:20]:

                fixture_id = match["fixture_id"]

                home = match["home"]

                away = match["away"]

                league = match["league"]

                raw_date = match["date"]

                try:

                    date_match = datetime.strptime(
                        raw_date,
                        "%Y%m%d%H%M%S"
                    ).strftime("%d/%m/%Y %H:%M")

                except:

                    date_match = raw_date


            with st.container():

        st.markdown(
            f"""
### ⚽ {home}

### 🆚

### ⚽ {away}

🏆 {league}

📅 {date_match}
"""
    )

    st.write(
        f"🏠 {odd_home}   "
        f"🤝 {odd_draw}   "
        f"🚩 {odd_away}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏠 1", odd_home)

    with col2:
        st.metric("🤝 N", odd_draw)

    with col3:
        st.metric("🚩 2", odd_away)

    if odd_home < 2:

        badge = "🔥 FAVORI"

    elif odd_home < 3:

        badge = "⭐ ÉQUILIBRÉ"

    else:

        badge = "⚠️ OUVERT"

    st.info(badge)

    if st.button(
        "🔍 Analyser",
        key=f"fixture_{fixture_id}"
    ):

        st.session_state["fixture_id"] = fixture_id

        st.session_state["home_team"] = home

        st.session_state["away_team"] = away

        st.session_state["league"] = league

        st.session_state["match_date"] = date_match

        st.session_state["selected_league"] = league

        st.session_state["selected_home"] = home

        st.session_state["selected_away"] = away

        st.session_state["selected_date"] = date_match

        st.success(
            f"Match sélectionné : {home} vs {away}"
        )

    st.divider()

    elif sport == "Tennis":

        tennis_calendar_page()

    elif sport == "Basketball":

        basketball_calendar_page()

    elif sport == "Hockey":

        hockey_calendar_page()

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

    st.title("🏆 Classements")

    st.info(
        "Le classement détaillé sera intégré à la V3."
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

    st.title("Historique H2H")

    st.info(
        "Le module H2H sera intégré dans predictions.py V3."
    )
    
# =====================================================
# PREDICTIONS
# =====================================================

elif menu == "Prédictions":

    if sport == "Football":

        predictions_page()

    elif sport == "Basketball":

        basketball_page()

    elif sport == "Tennis":

        tennis_page()

    elif sport == "Hockey":

        hockey_page()

# =====================================================
# ADMIN
# =====================================================

elif menu == "Admin":

    admin_page()

# =====================================================
# DASHBOARD IA GLOBAL
# =====================================================

elif menu == "Dashboard IA Global":
    dashboard_global_page()
