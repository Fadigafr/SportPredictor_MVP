import streamlit as st
import pandas as pd
import requests
from math import exp, factorial

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

API_KEY = st.secrets.get("API_KEY", "")

HEADERS = {
    "x-apisports-key": API_KEY
}

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>
.stApp{
    background:#0f1117;
}

[data-testid="stMetric"]{
    background:#1c2028;
    padding:15px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FONCTIONS
# =====================================================

def api_get(url):
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )
        return r.json()
    except Exception:
        return {"response": []}

def poisson(l, k):
    return (l ** k * exp(-l)) / factorial(k)

# =====================================================
# MENU PRINCIPAL
# =====================================================

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",

        "🔴 Matchs Live",
        "📅 Calendrier",

        "⚽ Football",
        "🎾 Tennis",
        "🏒 Hockey",

        "🏆 Compétitions",
        "📊 Classements",

        "👥 Joueurs",
        "🎯 Buteurs",

        "📈 Prédictions",
        "📉 Statistiques",

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
    c2.metric("Matchs analysés", "3250")
    c3.metric("Prédictions", "18750")
    c4.metric("Ligues", "500+")

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
            "Minute": m["fixture"]["status"]["elapsed"],
            "Domicile": m["teams"]["home"]["name"],
            "Score":
            f"{m['goals']['home']} - {m['goals']['away']}",
            "Extérieur": m["teams"]["away"]["name"],
            "Compétition": m["league"]["name"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# =====================================================
# CALENDRIER
# =====================================================

elif menu == "📅 Calendrier":

    st.title("📅 Calendrier")

    data = api_get(
        "https://v3.football.api-sports.io/fixtures?next=50"
    )

    rows = []

    for m in data.get("response", []):

        rows.append({
            "Date": m["fixture"]["date"][:16],
            "Domicile": m["teams"]["home"]["name"],
            "Extérieur": m["teams"]["away"]["name"],
            "Compétition": m["league"]["name"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# =====================================================
# FOOTBALL
# =====================================================

elif menu == "⚽ Football":

    st.title("⚽ Football")

    st.info("Ligues, équipes et statistiques football.")

# =====================================================
# TENNIS
# =====================================================

elif menu == "🎾 Tennis":

    st.title("🎾 Tennis")

# =====================================================
# HOCKEY
# =====================================================

elif menu == "🏒 Hockey":

    st.title("🏒 Hockey")

# =====================================================
# COMPÉTITIONS
# =====================================================

elif menu == "🏆 Compétitions":

    st.title("🏆 Compétitions")

    data = api_get(
        "https://v3.football.api-sports.io/leagues"
    )

    rows = []

    for league in data.get("response", []):

        rows.append({
            "Compétition": league["league"]["name"],
            "Pays": league["country"]["name"]
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

    league = st.number_input(
        "League ID",
        value=39
    )

    season = st.number_input(
        "Saison",
        value=2026
    )

    data = api_get(
        f"https://v3.football.api-sports.io/standings?league={league}&season={season}"
    )

    try:

        standings = \
            data["response"][0]["league"]["standings"][0]

        rows = []

        for t in standings:

            rows.append({
                "Pos": t["rank"],
                "Club": t["team"]["name"],
                "Pts": t["points"]
            })

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch"
        )

    except:
        st.warning("Aucune donnée")

# =====================================================
# JOUEURS
# =====================================================

elif menu == "👥 Joueurs":

    st.title("👥 Joueurs")

    team_id = st.number_input(
        "ID équipe",
        value=33
    )

    data = api_get(
        f"https://v3.football.api-sports.io/players?team={team_id}&season=2026"
    )

    rows = []

    for p in data.get("response", [])[:20]:

        rows.append({
            "Nom": p["player"]["name"],
            "Age": p["player"]["age"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# =====================================================
# BUTEURS
# =====================================================

elif menu == "🎯 Buteurs":

    st.title("🎯 Top Buteurs")

    data = api_get(
        "https://v3.football.api-sports.io/players/topscorers?league=39&season=2026"
    )

    rows = []

    for p in data.get("response", []):

        rows.append({
            "Joueur": p["player"]["name"],
            "Buts": p["statistics"][0]["goals"]["total"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# =====================================================
# PREDICTIONS
# =====================================================

elif menu == "📈 Prédictions":

    st.title("📈 Centre de Prédictions")

    prediction_menu = st.selectbox(
        "Module",
        [
            "💰 Cotes",
            "📊 Probabilités 1X2",
            "⚽ Over / Under",
            "✅ BTTS",
            "🎲 Score Exact",
            "🎯 Buteurs Probables",
            "📈 xG",
            "🤖 Analyse IA"
        ]
    )

    if prediction_menu == "💰 Cotes":

        fixture_id = st.number_input(
            "Fixture ID",
            value=123456
        )

        st.info(
            "Connectez ici l'endpoint /odds"
        )

    elif prediction_menu == "⚽ Over / Under":

        dom = st.slider(
            "Buts domicile",
            0.0, 5.0, 1.8
        )

        ext = st.slider(
            "Buts extérieur",
            0.0, 5.0, 1.2
        )

        total = dom + ext

        st.metric(
            "Over 2.5",
            f"{min(round((total/2.5)*50,1),95)}%"
        )

    elif prediction_menu == "✅ BTTS":

        dom = st.slider(
            "Moyenne domicile",
            0.0, 5.0, 1.8
        )

        ext = st.slider(
            "Moyenne extérieur",
            0.0, 5.0, 1.2
        )

        btts = min(
            round(dom * ext * 25, 1),
            95
        )

        st.metric(
            "BTTS Oui",
            f"{btts}%"
        )

    elif prediction_menu == "🎲 Score Exact":

        home_xg = st.slider(
            "xG domicile",
            0.1, 5.0, 1.8
        )

        away_xg = st.slider(
            "xG extérieur",
            0.1, 5.0, 1.2
        )

        scores = []

        for h in range(6):
            for a in range(6):

                p = (
                    poisson(home_xg, h)
                    *
                    poisson(away_xg, a)
                    * 100
                )

                scores.append(
                    (f"{h}-{a}", round(p, 2))
                )

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        st.table(scores[:10])

    elif prediction_menu == "🤖 Analyse IA":

        equipe1 = st.text_input(
            "Équipe domicile"
        )

        equipe2 = st.text_input(
            "Équipe extérieur"
        )

        forme1 = st.slider(
            "Forme domicile",
            0, 100, 70
        )

        forme2 = st.slider(
            "Forme extérieur",
            0, 100, 55
        )

        if st.button("Analyser"):

            home = round(
                (forme1/(forme1+forme2))*100,
                1
            )

            away = round(
                (forme2/(forme1+forme2))*100,
                1
            )

            draw = round(
                100-(home+away)*0.8,
                1
            )

            st.metric(
                "🏠 1",
                f"{home}%"
            )

            st.metric(
                "🤝 X",
                f"{draw}%"
            )

            st.metric(
                "🛫 2",
                f"{away}%"
            )

# =====================================================
# STATISTIQUES
# =====================================================

elif menu == "📉 Statistiques":

    st.title("📉 Statistiques")

    stats_menu = st.selectbox(
        "Module",
        [
            "xG",
            "H2H",
            "Possession",
            "Tirs",
            "Forme"
        ]
    )

    st.info(f"Module : {stats_menu}")

# =====================================================
# ADMIN
# =====================================================

elif menu == "👑 Admin":

    st.title("👑 Dashboard Admin")

    admin_menu = st.selectbox(
        "Administration",
        [
            "📊 Dashboard",
            "👥 Utilisateurs",
            "💎 VIP",
            "⚽ Matchs analysés",
            "🤖 Prédictions générées",
            "🏆 Ligues suivies",
            "📜 Logs",
            "⚙️ Paramètres"
        ]
    )

    st.success(f"Section : {admin_menu}")
