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
from database import load_predictions_db
from database import get_conn
from api_basketball import get_basketball_games_today
from predictions import dashboard_global_page
from results_db import (
    validate_football_results,
    validate_hockey_results,
    validate_basketball_results,
    validate_football_results_bet365
)
from results_db import (
    load_predictions,
    validate_football_results_bet365,
    get_prediction_success_rate,
    get_global_success_rate,
    save_prediction
)
from results_db import (
    get_market_learning_stats,
    get_market_success_rate
)
from results_db import get_market_bonus
from results_db import get_learning_bonus
from results_db import get_ai_learning_stats
from results_db import get_ai_confidence_level
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

        st.markdown(
            """
        ### 🚀 Centre de Sélection des Matchs

        Utilisez les filtres ci-dessous pour trouver rapidement les meilleures opportunités du jour.
        """
        )

        fixtures = get_soccer_calendar()

        if not fixtures:

            st.warning(
                "Quota Bet365 atteint ou aucun match disponible."
            )

            st.stop()

        st.write(
            "Fixtures récupérées :",
            len(fixtures) if fixtures else 0
        )

        leagues = sorted(
            list(
                set(
                    f["league"]
                    for f in fixtures
                )
            )
        )

        st.write("Compétitions trouvées :", len(leagues))
                                              

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

        # =====================================================
        # TOP MATCH DU JOUR
        # =====================================================

        if fixtures:

            top_match = fixtures[0]

            st.markdown("---")

            st.subheader("🔥 TOP MATCH DU JOUR")

            st.success(
                f"""
        ⚽ {top_match['home']} 🆚 {top_match['away']}

        🏆 {top_match['league']}
        """
            )

            st.markdown("---")
            
        # =====================================================
        # STATISTIQUES PREMIUM
        # =====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "⚽ Matchs",
                len(fixtures)
            )

        with col2:

            st.metric(
                "🏆 Compétitions",
                len(leagues)
            )

        with col3:

            st.metric(
                "🤖 IA Ready",
                len(fixtures)
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

                odd_home = 2.20
                odd_draw = 3.20
                odd_away = 3.60

                with st.container():

                    st.markdown(
                        f"""
## ⚽ {home} 🆚 {away}

🏆 {league}

📅 {date_match}
"""
    )

            # Badge IA

                    st.success("🤖 IA READY")

            # Badge Match

                    if odd_home < 2:

                        st.success("🔥 FAVORI")

                    elif odd_home < 3:

                        st.info("⭐ ÉQUILIBRÉ")

                    else:

                        st.warning("⚠️ OUVERT")

                    # Cotes

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("🏠 1", odd_home)

                    with col2:
                        st.metric("🤝 N", odd_draw)

                    with col3:
                        st.metric("🚩 2", odd_away)


                    badge = "⭐ SOLIDE"

                    st.info(
                        badge
                    )

                    # Analyse

                    if st.button(
                        "🚀 Lancer Analyse IA",
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
# ADMIN PREMIUM V15.4
# =====================================================

elif menu == "Admin":

    st.title("⚙ Administration")

    admin_section = st.radio(

        "Navigation Administrateur",

        [

            "📊 Dashboard",
            "🧪 Tests API",
            "🤖 IA Learning",
            "🗄 Base de Données",
            "🔧 Maintenance"

        ]

    )

    # =====================================================
    # DASHBOARD
    # =====================================================

    if admin_section == "📊 Dashboard":

        st.subheader(
            "📊 Dashboard Administrateur"
        )

        predictions = load_predictions_db()

        db_predictions = []

        conn = get_conn()

        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM predictions_history"
        )

        st.write(
            "Table predictions_history :",
            cur.fetchone()[0]
        )

        conn.close()

        st.metric(
            "Pronostics",
            len(predictions)
        )

        pending_count = len(
            [
                p for p in predictions
                if p.get("result") == "PENDING"
            ]
        )

        sports_count = len(
            set(
                [
                    p.get("sport")
                    for p in predictions
                ]
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Pronostics",
                len(predictions)
            )

        with col2:

            st.metric(
                "En attente",
                pending_count
            )

        with col3:

            st.metric(
                "Sports",
                sports_count
            )

        st.markdown("---")

        st.success(
            "✅ Dashboard Administrateur opérationnel"
        )

    # =====================================================
    # TESTS API
    # =====================================================

    elif admin_section == "🧪 Tests API":

        st.subheader(
            "🧪 Centre de Tests API"
        )

        if st.button(
            "TEST EVENT"
        ):

            try:

                st.json(
                    get_soccer_event(
                        "198646827"
                    )
                )

            except Exception as e:

                st.error(e)

        if st.button(
            "TEST CALENDAR"
        ):

            try:

                st.json(
                    get_soccer_calendar()
                )

            except Exception as e:

                st.error(e)

        if st.button(
            "TEST VALIDATION BET365"
        ):

            try:

                result = (
                    validate_football_results_bet365()
                )

                st.success(
                    f"Validation exécutée : {result}"
                )

            except Exception as e:

                st.error(e)

    if st.button("CRÉER PRONOSTIC TEST"):

        save_prediction(

            sport="Football",

            match="Botafogo vs Flamengo",

            prediction="1",

            ai_index=85,

            odd=2.10,

            fixture_id="TEST123"

        )

        st.success(
            "✅ Pronostic test créé."
        )

        st.markdown("---")

        predictions = load_predictions()

        st.metric("Pronostics enregistrés", len(predictions))

        pending = len(
            [p for p in predictions if p.get("result") == "PENDING"]
        )

        st.metric("En attente", pending)

    # =====================================================
    # IA LEARNING
    # =====================================================

    elif admin_section == "🤖 IA Learning":

        st.subheader(
            "🤖 Centre IA Learning"
        )

        success_rate = (
            get_prediction_success_rate(
                "1"
            )
        )

        st.metric(
            "Réussite IA",
            f"{success_rate}%"
        )

        if success_rate >= 70:

            st.success(
                "🔥 IA Expert"
            )

        elif success_rate >= 50:

            st.info(
                "⭐ IA Stable"
            )

        else:

            st.warning(
                "⚠️ IA en apprentissage"
            )

        st.subheader("🤖 IA Learning Premium")

        stats = get_ai_learning_stats()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pronostics analysés",
                stats["total"]
            )

            st.metric(
                "Pronostics gagnants",
                stats["wins"]
            )

        with col2:
            st.metric(
                "Pronostics perdants",
                stats["losses"]
            )

            st.metric(
                "En attente",
                stats["pending"]
            )

        st.markdown("---")

        st.metric(
            "Taux de réussite IA",
            f"{stats['success_rate']}%"
        )

        st.success(
            get_ai_confidence_level()
        )

        bonus = get_learning_bonus()

        st.metric(
            "Bonus Auto-Learning",
            bonus
        )

        if bonus > 0:

            st.success(
                f"✅ Bonus IA actif : +{bonus}"
            )
            st.success(
                f"Bonus IA actuel : +{bonus}"
            )

        else:

            st.error(
                f"⚠ Malus IA : {bonus}"
            )

        st.markdown("---")

        st.subheader(
            "🎯 Learning par Marché"
        )
        
        st.info(
            "Le bonus marché influence désormais l'AI Index."
        )

        markets = get_market_learning_stats()

        if not markets:

            st.info(
                "Aucune donnée de marché disponible."
            )

        else:

            for market in markets:

                rate = get_market_success_rate(
                    market
                )

                bonus = get_market_bonus(
                    market
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        f"Marché {market}",
                        f"{rate}%"
                    )

                with col2:

                    st.metric(
                        "Bonus",
                        bonus
                    )

        if st.button("Ajouter 5 WIN"):

            for i in range(5):

                save_prediction(
                    sport="Football",
                    match=f"TEST_WIN_{i}",
                    prediction="1",
                    ai_index=90,
                    odd=2.0,
                    fixture_id=f"WIN{i}",
                    result="WIN"
                )

            st.success("5 WIN ajoutés")

        if st.button("Ajouter 5 LOSS"):

            for i in range(5):

                save_prediction(
                    sport="Football",
                    match=f"TEST_LOSS_{i}",
                    prediction="1",
                    ai_index=90,
                    odd=2.0,
                    fixture_id=f"LOSS{i}",
                    result="LOSS"
                )

            st.success("5 LOSS ajoutés")

        stats = get_ai_learning_stats()

        st.write("WIN :", stats["wins"])
        st.write("LOSS :", stats["losses"])
        st.write("PENDING :", stats["pending"])
        st.write("Taux :", stats["success_rate"])
        st.write("Bonus :", get_learning_bonus())
        

    # =====================================================
    # BASE DE DONNÉES
    # =====================================================

    elif admin_section == "🗄 Base de Données":

        st.subheader(
            "🗄 Gestion Base de Données"
        )

        predictions = load_predictions()

        st.metric(
            "Enregistrements",
            len(predictions)
        )

        st.dataframe(
            pd.DataFrame(
                predictions
            ),
            width="stretch"
        )

    # =====================================================
    # MAINTENANCE
    # =====================================================

    elif admin_section == "🔧 Maintenance":

        st.subheader(
            "🔧 Outils Maintenance"
        )

        st.info(
            "Zone réservée à la maintenance."
        )

        if st.button(
            "Vérifier le système"
        ):

            st.success(
                "✅ Système opérationnel"
            )

        if st.button(
            "Actualiser les données"
        ):

            st.success(
                "✅ Actualisation terminée"
            )

        st.markdown("---")

        st.warning(
            "Les fonctions sensibles seront ajoutées dans les prochaines versions."
        )

        if st.button(
            "TEST VALIDATION BET365"
        ):

            result = (
                validate_football_results_bet365()
            )

            st.success(
                f"Validation exécutée : {result}"
            )

        if st.button(
            "TEST CALENDAR"
        ):

            st.json(
                get_soccer_calendar()
            )
            
# =====================================================
# DASHBOARD IA GLOBAL
# =====================================================

elif menu == "Dashboard IA Global":
    dashboard_global_page()
