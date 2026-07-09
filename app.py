import streamlit as st
import pandas as pd

from database import init_db
from auth import login
from api_football import api_get
from predictions import predictions_page
from admin import admin_page

import time
import streamlit as st

placeholder = st.empty()

placeholder.markdown("""
<div style="
text-align:center;
padding-top:180px;
">
assets/logo.png
<h1 style='color:#FFD700;'>
SPORT PREDICTOR ULTRA PRO IA
</h1>
<p style='color:white;'>
Chargement de l'Intelligence Artificielle...
</p>
</div>
""", unsafe_allow_html=True)

time.sleep(3)

placeholder.empty()

st.markdown("""
<style>

@keyframes zoomLogo {
    0%{
        transform:scale(0.5);
        opacity:0;
    }

    100%{
        transform:scale(1);
        opacity:1;
    }
}

.logo-animation{
    animation:zoomLogo 2s ease-in-out;
}

</style>
""", unsafe_allow_html=True)
placeholder.markdown(f"""
<div align="center">

assets/logo.png

<h1 style="color:#FFD700;">
SPORT PREDICTOR ULTRA PRO IA
</h1>

</div>
""",
unsafe_allow_html=True)

st.markdown("""
<style>

.stApp{

background:
linear-gradient(
135deg,
#0D1117,
#0F172A,
#111827
);

color:white;

}

</style>
""",
unsafe_allow_html=True)
st.markdown("""
<div style="
text-align:center;
color:#00E5FF;
font-size:18px;
">

⚽ Football • 📊 Statistiques • 🤖 IA

</div>
""",
unsafe_allow_html=True)

progress = st.progress(0)

for i in range(100):
    time.sleep(0.02)
    progress.progress(i + 1)

progress.empty()

# =====================================================
# INITIALISATION
# =====================================================

init_db()

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO IA",
    page_icon="assets/logo.png",
    layout="wide"
)
# =====================================================
# SESSION
# =====================================================

if "user" not in st.session_state:
    st.session_state.user = None

# =====================================================
# AUTHENTIFICATION
# =====================================================

login()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🏆 SPORT PREDICTOR")

if st.session_state.user:

    st.sidebar.success(
        f"✅ {st.session_state.user}"
    )

    if st.sidebar.button("🚪 Déconnexion"):

        st.session_state.user = None
        st.rerun()

# =====================================================
# MENU
# =====================================================

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
        "🤖 Analyse IA du Jour",
        "🔔 Notifications",
        "👑 Admin"
    ]
)

# =====================================================
# ACCUEIL
# =====================================================

if menu == "🏠 Accueil":

    st.title("🏆 SPORT PREDICTOR ULTRA PRO 2026")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Précision IA", "78%")
    c2.metric("Matchs analysés", "3 250")
    c3.metric("Prédictions", "18 750")
    c4.metric("Ligues", "500+")

    st.markdown("---")

    st.subheader("🔥 Top fonctionnalités")

    st.write("""
    ✅ Matchs Live

    ✅ Calendrier intelligent

    ✅ H2H automatique

    ✅ Cotes Bookmakers

    ✅ BTTS

    ✅ Over/Under

    ✅ Score Exact Poisson

    ✅ Analyse IA
    """)

# =====================================================
# LIVE
# =====================================================

elif menu == "🔴 Matchs Live":

    st.title("🔴 Matchs Live")

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

        st.info("Aucun match en direct.")

# =====================================================
# CALENDRIER
# =====================================================

elif menu == "📅 Calendrier":

    st.title("📅 Calendrier")

    fixtures = api_get(
        "https://v3.football.api-sports.io/fixtures?next=50"
    )

    matchs = {}
    rows = []

    for m in fixtures.get("response", []):

        match = (
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}"
        )

        matchs[match] = m["fixture"]["id"]

        rows.append({
            "Date":
                m["fixture"]["date"][:16],

            "Compétition":
                m["league"]["name"],

            "Match":
                match
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

    if matchs:

        match_name = st.selectbox(
            "⚽ Sélection du match",
            list(matchs.keys())
        )

        fixture_id = matchs[match_name]

        st.success(
            f"Match sélectionné : {match_name}"
        )

# =====================================================
# COMPÉTITIONS
# =====================================================

elif menu == "🏆 Compétitions":

    st.title("🏆 Compétitions")

    leagues = api_get(
        "https://v3.football.api-sports.io/leagues"
    )

    rows = []

    for l in leagues.get("response", []):

        rows.append({
            "Compétition":
                l["league"]["name"],

            "Pays":
                l["country"]["name"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# =====================================================
# CLASSEMENTS
# =====================================================

elif menu == "📊 Classements":

    st.title("📊 Classements")

    st.info(
        "Module standings prêt à connecter."
    )

# =====================================================
# JOUEURS
# =====================================================

elif menu == "👥 Joueurs":

    st.title("👥 Joueurs")

    st.info(
        "Module players prêt."
    )

# =====================================================
# BUTEURS
# =====================================================

elif menu == "🎯 Top Buteurs":

    st.title("🎯 Top Buteurs")

    st.info(
        "Module topscorers prêt."
    )

# =====================================================
# H2H
# =====================================================

elif menu == "⚔️ H2H":

    st.title("⚔️ Historique H2H")

    st.info(
        "Module face-à-face dynamique."
    )

# =====================================================
# PREDICTIONS
# =====================================================

elif menu == "📈 Prédictions":

    predictions_page()

# =====================================================
# IA DU JOUR
# =====================================================

elif menu == "🤖 Analyse IA du Jour":

    st.title("🤖 Top 5 Prédictions IA")

    analyses = [
        ["PSG vs Monaco", "71%", "2-1"],
        ["Liverpool vs Arsenal", "68%", "2-1"],
        ["Real Madrid vs Bilbao", "54%", "3-1"],
        ["Bayern vs Leverkusen", "73%", "2-2"],
        ["Inter vs Milan", "66%", "1-1"]
    ]

    for match, btts, score in analyses:

        st.subheader(match)

        c1, c2 = st.columns(2)

        c1.metric(
            "BTTS",
            btts
        )

        c2.metric(
            "Score Exact",
            score
        )

        st.divider()

# =====================================================
# NOTIFICATIONS
# =====================================================

elif menu == "🔔 Notifications":

    st.title("🔔 Notifications")

    st.checkbox("🔴 Début match")
    st.checkbox("⚽ But")
    st.checkbox("🟥 Carton rouge")
    st.checkbox("💰 Changement cote")
    st.checkbox("🤖 Nouvelle analyse IA")

# =====================================================
# ADMIN
# =====================================================

elif menu == "👑 Admin":

    admin_page()
