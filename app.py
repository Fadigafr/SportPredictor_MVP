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
# CALENDRIER + COMPETITIONS
# =====================================================

elif menu == "Calendrier":

    st.title("📅 Calendrier & Compétitions")

    competitions = {
        "Premier League": 39,
        "La Liga": 140,
        "Ligue 1": 61,
        "Bundesliga": 78,
        "Serie A": 135,
        "Champions League": 2
    }

    competition = st.selectbox(
        "🏆 Compétition",
        list(competitions.keys())
    )

    league_id = competitions[competition]

    fixtures = api_get(
        f"https://v3.football.api-sports.io/fixtures?league={league_id}&next=50"
    )

    response = fixtures.get("response", [])

    st.write(
        f"📊 Matchs trouvés : {len(response)}"
    )

    rows = []
    matchs = {}

    for m in response:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        match_name = f"{home} vs {away}"

        fixture_id = m["fixture"]["id"]

        matchs[match_name] = fixture_id

        rows.append({
            "Date": m["fixture"]["date"][:16],
            "Match": match_name
        })

    if rows:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            width="stretch"
        )

        selected_match = st.selectbox(
            "⚽ Choisir un match",
            list(matchs.keys())
        )

        if selected_match:

            st.session_state["fixture_id"] = (
                matchs[selected_match]
            )

            st.success(
                "✅ Match sélectionné"
            )

    else:

        st.warning(
            "Aucun match trouvé."
        )

    rows = []
    matchs = {}

    for m in response:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        fixture_id = m["fixture"]["id"]

        match_name = f"{home} vs {away}"

        matchs[match_name] = fixture_id

        rows.append({
            "Date": m["fixture"]["date"][:16],
            "Match": match_name
        })

    if len(rows) > 0:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            width="stretch"
        )

        if selected_match:

            st.session_state["fixture_id"] = (
                matchs[selected_match]
            )

            st.success(
                "✅ Match sélectionné"
            )

    else:

        st.warning(
            "Aucun match trouvé."
        )
    if "fixture_id" in st.session_state:

        st.info(
            "✅ Match sélectionné. Ouvrez maintenant le menu 'Prédictions'."
        )

    else:

        st.info(
            "Sélectionnez un match pour lancer l'analyse."
        )

    # =====================================================
    # MATCH SELECTIONNE
    # =====================================================

    if "fixture_id" in st.session_state:

        fixture_id = st.session_state["fixture_id"]

        fixture = api_get(
            f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
        )

        if fixture.get("response"):

            home_team = fixture["response"][0]["teams"]["home"]["name"]
            away_team = fixture["response"][0]["teams"]["away"]["name"]

            st.subheader(
                f"{home_team} vs {away_team}"
            )

            st.info(
                "✅ Match prêt pour l'analyse IA."
            )

    if "fixture_id" in st.session_state:

        fixture_id = st.session_state["fixture_id"]

        fixture = api_get(
            f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
        )

        if fixture.get("response"):

            home_team = fixture["response"][0]["teams"]["home"]["name"]
            away_team = fixture["response"][0]["teams"]["away"]["name"]

            st.subheader(
                f"{home_team} vs {away_team}"
            )

            st.info(
                "✅ Match prêt pour l'analyse IA.\n\n"
                "Ouvrez le menu 'Prédictions' pour lancer l'analyse complète."
            )

    else:

        st.info(
            "Sélectionnez un match pour lancer l'analyse."
        )

        # =====================================================
        # Statistiques
        # =====================================================

        # stats = api_get(...)

        # =====================================================
        # H2H
        # =====================================================

        # h2h = api_get(...)

        # =====================================================
        # Odds
        # =====================================================

        # odds = api_get(...)

        # =====================================================
        # Analyse IA
        # =====================================================
        
# =====================================================
# ANALYSE IA DU JOUR
# =====================================================

elif menu == "Analyse IA du Jour":

    st.title(
        "Top 5 Analyses IA"
    )

    analyses = [

        {
            "match":"Liverpool vs Arsenal",
            "confidence":82,
            "score":"2-1"
        },

        {
            "match":"Real Madrid vs Atletico",
            "confidence":80,
            "score":"2-0"
        },

        {
            "match":"Bayern vs Dortmund",
            "confidence":79,
            "score":"3-1"
        },

        {
            "match":"PSG vs Marseille",
            "confidence":78,
            "score":"2-1"
        },

        {
            "match":"Inter vs Milan",
            "confidence":76,
            "score":"1-1"
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
