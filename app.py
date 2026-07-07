import streamlit as st
import requests
import pandas as pd
from math import exp, factorial

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

API_KEY = st.secrets["API_KEY"]

HEADERS = {
    "x-apisports-key": API_KEY
}

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:#0f1117;
    color:white;
}

.metric-container{
    background:#1a1d24;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# FONCTIONS
# ---------------------------------------------------

def api_get(url):
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )
        return r.json()
    except:
        return {"response":[]}

def poisson(l,k):
    return (l**k*exp(-l))/factorial(k)

# ---------------------------------------------------
# MENU
# ---------------------------------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "🔴 Matchs Live",
        "📅 Calendrier",
        "📊 Classements",
        "⚔️ H2H",
        "🎯 Buteurs",
        "💰 Cotes",
        "⚽ Over/Under",
        "✅ BTTS",
        "🎲 Score Exact",
        "🤖 Analyse IA"
    ]
)
)

# ---------------------------------------------------
# LIVE
# ---------------------------------------------------

if menu == "🔴 Matchs Live":

    st.title("🔴 Matchs en direct")

    data = api_get(
        "https://v3.football.api-sports.io/fixtures?live=all"
    )

    for m in data.get("response",[]):

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]

        minute = (
            m["fixture"]["status"]["elapsed"]
        )

        st.info(
            f"{home} {hg}-{ag} {away} | {minute}'"
        )

# ---------------------------------------------------
# COTES
# ---------------------------------------------------

elif menu == "💰 Cotes":

    st.title("💰 Cotes Bookmakers")

    fixture_id = st.number_input(
        "Fixture ID",
        value=0
    )

    if fixture_id > 0:

        url = (
            f"https://v3.football.api-sports.io/odds"
            f"?fixture={fixture_id}"
        )

        data = api_get(url)

        st.json(data)

elif menu == "💰 Cotes":

    st.title("💰 Cotes 1X2")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏠 Domicile",
        "1.75"
    )

    col2.metric(
        "🤝 Nul",
        "3.60"
    )

    col3.metric(
        "🛫 Extérieur",
        "4.50"
    )

# ---------------------------------------------------
# CALENDRIER
# ---------------------------------------------------

elif menu == "📅 Calendrier":

    st.title("📅 Matchs à venir")

    data = api_get(
        "https://v3.football.api-sports.io/fixtures?next=50"
    )

    rows=[]

    for m in data.get("response",[]):

        rows.append({
            "Date":
            m["fixture"]["date"][:16],

            "Domicile":
            m["teams"]["home"]["name"],

            "Extérieur":
            m["teams"]["away"]["name"],

            "Compétition":
            m["league"]["name"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )
equipe1 = st.text_input(
    "Équipe domicile"
)

equipe2 = st.text_input(
    "Équipe extérieur"
)
# ---------------------------------------------------
# CLASSEMENT
# ---------------------------------------------------

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

        standings = (
            data["response"][0]
            ["league"]
            ["standings"][0]
        )

        rows=[]

        for t in standings:

            rows.append({
                "Pos":t["rank"],
                "Club":t["team"]["name"],
                "Pts":t["points"]
            })

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch"
        )

    except:

        st.warning("Classement indisponible")

# ---------------------------------------------------
# H2H
# ---------------------------------------------------

elif menu == "⚔️ H2H":

    st.title("⚔️ Face à Face")

    h2h = st.text_input(
        "Exemple : 33-40"
    )

    if h2h:

        data = api_get(
            f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={h2h}"
        )

        for m in data.get("response",[]):

            st.write(
                f"{m['teams']['home']['name']} "
                f"{m['goals']['home']}"
                f" - "
                f"{m['goals']['away']} "
                f"{m['teams']['away']['name']}"
            )

# ---------------------------------------------------
# BUTEURS
# ---------------------------------------------------

elif menu == "🎯 Buteurs":

    st.title("🎯 Top Buteurs")

    data = api_get(
        "https://v3.football.api-sports.io/players/topscorers?league=39&season=2026"
    )

    rows=[]

    for p in data.get("response",[]):

        rows.append({
            "Joueur":
            p["player"]["name"],

            "Buts":
            p["statistics"][0]["goals"]["total"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# ---------------------------------------------------
# OVER UNDER
# ---------------------------------------------------

elif menu == "⚽ Over/Under":

    st.title("⚽ Over / Under")

    dom = st.number_input(
        "Buts domicile",
        0.0,
        5.0,
        1.8
    )

    ext = st.number_input(
        "Buts extérieur",
        0.0,
        5.0,
        1.2
    )

    total = dom + ext

    st.metric(
        "Over 1.5",
        f"{min(round((total/1.5)*50,1),99)}%"
    )

    st.metric(
        "Over 2.5",
        f"{min(round((total/2.5)*50,1),99)}%"
    )

    st.metric(
        "Over 3.5",
        f"{min(round((total/3.5)*50,1),99)}%"
    )
over25 = min(
        round(
            (total/2.5)*50,
            1
        ),
        95
    )

    st.metric(
        "⚽ Over 2.5",
        f"{over25}%"
    )

# ---------------------------------------------------
# BTTS
# ---------------------------------------------------

elif menu == "✅ BTTS":

    st.title("✅ Both Teams To Score")

    dom = st.number_input(
        "Moyenne domicile",
        0.0,
        5.0,
        1.8
    )

    ext = st.number_input(
        "Moyenne extérieur",
        0.0,
        5.0,
        1.2
    )

    btts = min(
        round(dom*ext*25,1),
        95
    )

    st.metric(
        "BTTS Oui",
        f"{btts}%"
    )
btts = min(
        round(
            xg_dom*xg_ext*25,
            1
        ),
        95
    )

    st.metric(
        "✅ BTTS",
        f"{btts}%"
    )

# ---------------------------------------------------
# SCORE EXACT
# ---------------------------------------------------

elif menu == "🎲 Score Exact":

    st.title("🎲 Score Exact Poisson")

    home_xg = st.number_input(
        "xG domicile",
        0.1,
        5.0,
        1.8
    )

    away_xg = st.number_input(
        "xG extérieur",
        0.1,
        5.0,
        1.2
    )

    scores=[]

    for h in range(6):

        for a in range(6):

            p = (
                poisson(home_xg,h)
                *
                poisson(away_xg,a)
                *100
            )

            scores.append(
                (
                    f"{h}-{a}",
                    round(p,2)
                )
            )

    scores=sorted(
        scores,
        key=lambda x:x[1],
        reverse=True
    )

    st.table(scores[:10])
scores = []

    for h in range(6):

        for a in range(6):

            p = (
                poisson(xg_dom,h)
                *
                poisson(xg_ext,a)
                *
                100
            )

            scores.append(
                (
                    f"{h}-{a}",
                    round(p,2)
                )
            )

    scores = sorted(
        scores,
        key=lambda x:x[1],
        reverse=True
    )

    st.subheader(
        "🎲 Score Exact"
    )

    st.table(scores[:5])

# ---------------------------------------------------
# IA
# ---------------------------------------------------

elif menu == "🤖 Analyse IA":

    st.title("🤖 Analyse IA")

    equipe1 = st.text_input("Equipe domicile")
    equipe2 = st.text_input("Equipe extérieur")

    forme1 = st.slider(
        "Forme domicile",
        0,
        100,
        70
    )

    forme2 = st.slider(
        "Forme extérieur",
        0,
        100,
        55
    )

    if st.button("Analyser"):

        avantage = forme1 - forme2

        if avantage > 10:
            prediction = "✅ Victoire domicile"

        elif avantage < -10:
            prediction = "✅ Victoire extérieur"

        else:
            prediction = "✅ Match équilibré"

        st.success(prediction)

        st.info(
            f'''
{equipe1} possède une forme de {forme1}%.

{equipe2} possède une forme de {forme2}%.

Pronostic :
{prediction}

Over 2.5 probable.

BTTS envisageable.
'''
        )
analyse = f"""
✅ Match : {equipe1} vs {equipe2}

🏠 Victoire domicile : {home_win} %

🤝 Nul : {round(draw,1)} %

🛫 Victoire extérieur : {away_win} %

⚽ Over 2.5 : {over25} %

✅ BTTS : {btts} %

🎲 Score probable :
{scores[0][0]}

📈 Analyse :

{xg_dom} xG contre {xg_ext} xG.

Le modèle favorise
{'le domicile' if home_win > away_win else 'l extérieur'}.
"""

    st.info(analyse)

st.subheader("⚽ Résultat probable")

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "🏠 1",
        f"{home_win}%"
    )

    col2.metric(
        "🤝 X",
        f"{round(draw,1)}%"
    )

    col3.metric(
        "🛫 2",
        f"{away_win}%"
    )

if st.button("Analyser"):

    total = xg_dom + xg_ext

    home_win = min(
        round(
            (forme1/(forme1+forme2))*100,
            1
        ),
        90
    )

    away_win = 100 - home_win

    draw = 100 - (
        home_win * 0.75
        +
        away_win * 0.75
    )
