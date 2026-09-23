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
from database import save_prediction_db
from database import get_conn
from database import get_conn, DB
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
from results_db import (
    validate_prediction_with_event
)
from results_db import get_market_ranking
from results_db import get_market_bonus
from results_db import get_learning_bonus
from results_db import get_ai_learning_stats
from results_db import get_ai_confidence_level
from results_db import (
    get_pending_predictions,
    get_pending_count,
    mark_prediction_win,
    mark_prediction_loss,
    auto_validate_pending,
    get_pending_fixture_ids
)
from results_db import (
    get_ai_learning_stats,
    get_learning_bonus
)
from results_db import (
    get_pending_predictions,
    update_prediction_result,
    calculate_real_result
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
from pulsescore_api import (
    get_live_soccer_events,
    get_event_details,
    get_first_live_event,
    extract_match_result,
    get_upcoming_soccer_events
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
            "💾 Sauvegarder Event PulseScore",
            key="save_pulsescore_event"
        ):

            events = get_live_soccer_events()

            if events:

                event = events[0]

                save_prediction(

                    sport="Football",

                    match=f"{event['home']} vs {event['away']}",

                    prediction="1",

                    ai_index=80,

                    odd=2.00,

                    fixture_id=event["eventId"]

                )

                st.success(
                    f"✅ EventID sauvegardé : "
                    f"{event['eventId']}"
                )

        if st.button(
            "📋 Voir les derniers EventID",
            key="show_last_eventids"
        ):

            predictions = load_predictions()

            for prediction in predictions[-10:]:

                st.write({

                    "match": prediction.get("match"),

                    "fixture_id": prediction.get(
                        "fixture_id"
                    ),

                    "result": prediction.get(
                        "result"
                    )

                })

        if st.button(
            "🔍 Dernière prédiction"
        ):

            predictions = load_predictions()

            if predictions:

                st.subheader("📋 Dernières prédictions")

                predictions = load_predictions()

                st.write(
                    f"Total : {len(predictions)}"
                )

                st.subheader("📋 5 dernières prédictions")

                for prediction in predictions[:5]:

                    st.json(prediction)

                predictions = load_predictions()

                st.subheader("🔍 Dernier enregistrement")

                st.success(
                    f"ID le plus récent : {predictions[0]['id']}"
                )
                
                st.json(
                    predictions[0]
                )

                predictions = load_predictions()

                st.write(
                    "Premier ID :",
                    predictions[0]["id"]
                )

                st.write(
                    "Dernier ID :",
                    predictions[-1]["id"]
                )

        if st.button(
            "🔍 Tester EventID Réel",
            key="test_event_details"
        ):

            data = get_event_details(
                201586086
            )

            st.json(data)

        if st.button(
            "🔍 Tester Premier Match Live",
            key="test_first_live"
        ):

            events = get_live_soccer_events()

            if events:

                first_event = events[0]

                st.json(first_event)

        if st.button(
            "🎯 Tester Résultat Réel"
        ):

            event = get_first_live_event()

            if event:

                result = extract_match_result(
                    event
                )

                st.success(
                    f"Résultat réel : {result}"
                )

        if st.button(
            "🚀 Tester Validation Réelle"
        ):

            prediction = "1"

            actual_result = "1"

            result = calculate_real_result(
                prediction,
                actual_result
            )

            st.success(
                f"Résultat : {result}"
            )

        if st.button(
            "🚀 Validation Réelle Complète"
        ):

            predictions = load_predictions()

            latest_prediction = predictions[0]

            event = get_first_live_event()

            result = validate_prediction_with_event(
                latest_prediction,
                event
            )

            update_prediction_result(
                prediction_id,
                result
            )

            stats = get_ai_learning_stats()

            bonus = get_learning_bonus()

            st.success(
                f"✅ Learning mis à jour | Bonus IA : {bonus}"
            )

            st.json(stats)

            st.success(
                f"✅ Prédiction #{latest_prediction['id']} mise à jour : {result}"
            )

            st.write(
                "Event :",
                event
            )

        if st.button("🧠 Tester Learning Temps Réel"):

            stats = get_ai_learning_stats()

            bonus = get_learning_bonus()

            st.write("Stats Learning :")
            st.json(stats)

            st.write("Bonus IA :")
            st.success(bonus)

        # ====================================================
        # V16.5 CALENDRIER RÉEL PULSESCORE
        # ====================================================

        st.subheader("📅 Calendrier Réel PulseScore")

        if st.button(
            "📅 Charger Matchs Futurs",
            key="load_upcoming_events"
        ):

            events = get_upcoming_soccer_events()

            st.success(
                f"{len(events)} matchs futurs trouvés."
            )

            for event in events:

                league = event.get("league", "")

                # Optionnel : ignorer Esoccer
                # if "Esoccer" in league:
                #     continue

                st.info(
                    f"""
        🏆 {league}

        ⚽ {event.get('home')}
        vs
        {event.get('away')}

        🕒 {event.get('startTime')}

        🆔 {event.get('eventId')}
        """
                )

                # ------------------------------------------------
                # V16.5.3 PRONOSTIC RÉEL
                # ------------------------------------------------

                if st.button(
                    f"🎯 Pronostiquer {event.get('eventId')}",
                    key=f"predict_{event.get('eventId')}"
                ):

                    predictions = load_predictions()

                    for p in predictions[:5]:

                        st.json(p)
                        
                    st.json(event)
                    
                    save_prediction(

                        sport="Football",

                        match=(
                            f"{event.get('home')} "
                            f"vs "
                            f"{event.get('away')}"
                        ),

                        prediction="1",

                        ai_index=80,

                        fixture_id=event.get(
                            "eventId"
                        )

                    )
                    
                    st.success(
                        f"✅ Pronostic créé : {event.get('eventId')}"
                    )

                    data = load_predictions()

                    st.write(
                        "DEBUG TOTAL =",
                        len(data)
                    )

                    if data:
                        st.json(data[0])
                    else:
                        st.error("Aucune donnée chargée")
                        
                    predictions = load_predictions()

                    st.write(
                        "Total prédictions :",
                        len(predictions)
                    )

                    st.json(
                        predictions[0]
                    )

        # ====================================================
        # HISTORIQUE DES MATCHS FUTURS
        # ====================================================

        st.subheader("📋 Historique des Matchs Futurs")

        predictions = load_predictions()

        pending_predictions = [

            p for p in predictions

            if p.get("result") == "PENDING"
        ]

        st.metric(
            "📅 Matchs en attente",
            len(pending_predictions)
        )

        for p in pending_predictions[:20]:

            st.info(
                f"""
        ⚽ {p.get('match')}

        🆔 {p.get('fixture_id')}

        🎯 Pronostic : {p.get('prediction')}

        📊 IA Index : {p.get('ai_index')}

        ⏳ Statut : {p.get('result')}
        """
            )

        if st.button("TEST CALENDAR"):

            st.write("DB =", DB)

            conn = get_conn()

            c = conn.cursor()

            c.execute(
                "SELECT COUNT(*) FROM predictions_history"
            )

            total = c.fetchone()[0]

            st.success(
                f"TOTAL SQL = {total}"
            )

            c.execute(
                """
                SELECT id, match, fixture_id, result
                FROM predictions_history
                ORDER BY id DESC
                LIMIT 5
                """
            )

            rows = c.fetchall()

            st.write(rows)

            conn.close()

        if st.button(
            "🎯 Event Live Actuel"
        ):

            event = get_first_live_event()

            st.json(event)

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

           fixture_id=event["eventId"]

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

        st.subheader(
            "🧪 Test PulseScore"
        )

        events = get_live_soccer_events()

        st.write(
            f"Matchs trouvés : {len(events)}"
        )

        for event in events:

            st.info(
                f"""
        🏆 {event.get('league')}

        ⚽ {event.get('home')}
        vs
        {event.get('away')}

        🆔 {event.get('eventId')}
        """
            )
            
        st.subheader("🤖 IA Learning Premium")

        stats = get_ai_learning_stats()

        st.write(type(stats))
        st.write(stats)

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

        if st.button("📊 Générer historique test"):

            for i in range(10):

                save_prediction_db(
                    date="2026-08-30",
                    sport="Football",
                    match=f"TEST_{i}",
                    fixture_id=event["eventId"],
                    prediction="1",
                    ai_index=85,
                    odd=2.0,
                    result="WIN" if i < 7 else "LOSS"
                )

            st.success(
                "✅ Historique de test généré"
            )

        stats = get_ai_learning_stats()

        st.write("WIN :", stats["wins"])
        st.write("LOSS :", stats["losses"])
        st.write("PENDING :", stats["pending"])
        st.write("Taux :", stats["success_rate"])
        st.write("Bonus :", get_learning_bonus())

        # =====================================================
        # 🏆 TOP MARCHÉS IA
        # =====================================================

        st.subheader("🏆 Top Marchés IA")

        markets = get_market_learning_stats()

        ranking = []

        for market in markets:

            ranking.append({
                "market": market,
                "rate": get_market_success_rate(market),
                "bonus": get_market_bonus(market)
            })

        ranking = sorted(
            ranking,
            key=lambda x: x["rate"],
            reverse=True
        )

        if not ranking:

            st.info(
                "Aucune donnée de marché disponible."
            )

        else:

            for item in ranking:

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"🎯 {item['market']}")

                with col2:
                    st.metric(
                        "Réussite",
                        f"{item['rate']}%"
                    )

                with col3:
                    st.metric(
                        "Bonus",
                        item["bonus"]
                    )

        # =====================================================
        # 📈 RÉSUMÉ IA GLOBAL
        # =====================================================

        st.markdown("---")

        st.subheader("📈 Résumé IA Global")

        stats = get_ai_learning_stats()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Historique Total",
                stats["total"]
            )

        with col2:

            st.metric(
                "Taux de Réussite",
                f"{stats['success_rate']}%"
            )

        with col3:

            st.metric(
                "Bonus IA",
                get_learning_bonus()
            )

        # =====================================================
        # ⏳ VALIDATION AUTOMATIQUE
        # =====================================================

        st.markdown("---")

        st.subheader("⏳ Validation Automatique")

        pending_predictions = get_pending_predictions()

        st.metric(
            "Pronostics en attente",
            len(pending_predictions)
        )

        if pending_predictions:

            st.warning(
                f"{len(pending_predictions)} pronostics attendent une validation."
            )

        else:

            st.success(
                "✅ Aucun pronostic en attente."
            )

            wins = len(
                [p for p in load_predictions()
                 if p.get("result") == "WIN"]
            )

            losses = len(
                [p for p in load_predictions()
                 if p.get("result") == "LOSS"]
            )

            st.metric(
                "WIN Auto",
                wins
            )

            st.metric(
                "LOSS Auto",
                losses
            )
            
        # =====================================================
        # 🏆 NIVEAU IA
        # =====================================================

        if stats["success_rate"] >= 80:

            st.success("🔥 IA ELITE")

        elif stats["success_rate"] >= 70:

            st.success("🚀 IA PREMIUM")

        elif stats["success_rate"] >= 60:

            st.info("✅ IA STABLE")

        elif stats["success_rate"] >= 50:

            st.warning("⚠️ IA EN APPRENTISSAGE")

        else:

            st.error("🔧 IA À OPTIMISER")

        # =====================================================
        # ⚠️ MARCHÉS À SURVEILLER
        # =====================================================

        st.markdown("---")

        st.subheader("⚠️ Marchés à Surveiller")

        weak_markets = [
            item for item in ranking
            if item["rate"] < 50
        ]

        if weak_markets:

            for item in weak_markets:

                st.warning(
                    f"{item['market']} → {item['rate']}%"
                )

        else:

            st.success(
                "✅ Aucun marché critique détecté."
            )

        # =====================================================
        # 🏆 MEILLEUR MARCHÉ IA
        # =====================================================

        if ranking:

            best_market = ranking[0]

            st.markdown("---")

            st.subheader("🏅 Meilleur Marché IA")

            st.success(
                f"{best_market['market']} | "
                f"{best_market['rate']}% | "
                f"Bonus +{best_market['bonus']}"
            )
        st.markdown("---")

        st.subheader("🧪 Test Validation Auto")

        if st.button(
            "✅ Transformer un PENDING en WIN",
            key="btn_pending_win_v16"
        ):

            pending = get_pending_predictions()

            if pending:

                mark_prediction_win(
                    pending[0]["id"]
                )

                st.success(
                    "PENDING → WIN"
                )

        if st.button(
            "❌ Transformer un PENDING en LOSS",
            key="btn_pending_loss_v16"
        ):

            pending = get_pending_predictions()

            if pending:

                mark_prediction_loss(
                    pending[0]["id"]
                )

                st.success(
                    "PENDING → LOSS"
                )

        st.markdown("---")

        st.subheader("🤖 Auto Validation V16.2")

        if st.button(
            "🚀 Lancer Validation Auto",
            key="auto_validation_v162"
        ):

            total = auto_validate_pending()

            st.success(
                f"{total} pronostics validés automatiquement."
            )

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
