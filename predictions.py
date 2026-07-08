import pandas as pd
import streamlit as st

from api_football import api_get

from math import exp,factorial

def poisson(l,k):
    return (l**k*exp(-l))/factorial(k)

def predictions_page():

    st.header("📈 Centre de Prédictions")

    leagues = api_get(
        "https://v3.football.api-sports.io/leagues"
    )

    league_dict = {}

    for l in leagues.get("response",[]):

        league_dict[
            l["league"]["name"]
        ] = l["league"]["id"]

    if not league_dict:
        st.warning("Aucune ligue disponible")
        return

    competition = st.selectbox(
        "🏆 Compétition",
        sorted(
            league_dict.keys()
        )
    )

    league_id = league_dict[competition]

    fixtures = api_get(
        f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2026&next=20"
    )

    matchs = {}

    for m in fixtures.get("response",[]):

        nom = (
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}"
        )

        matchs[nom] = m["fixture"]["id"]

    if not matchs:
        st.warning("Aucun match")
        return

    match_name = st.selectbox(
        "⚽ Match",
        list(matchs.keys())
    )

    fixture_id = matchs[match_name]

    st.subheader("📊 Statistiques Match")

    stats = api_get(
        f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
    )

    if len(stats.get("response",[])) >= 2:

        home = stats["response"][0]
        away = stats["response"][1]

        rows=[]

        for i in range(
            min(
                len(home["statistics"]),
                len(away["statistics"])
            )
        ):

            rows.append({
                "Statistique":
                home["statistics"][i]["type"],

                "Domicile":
                home["statistics"][i]["value"],

                "Extérieur":
                away["statistics"][i]["value"]
            })

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch"
        )

    st.subheader(
        "🎯 Buteurs Probables"
    )

    st.dataframe(
        pd.DataFrame({
            "Joueur":[
                "Haaland",
                "Mbappé",
                "Kane"
            ],
            "Probabilité":[
                "68%",
                "61%",
                "55%"
            ]
        }),
        width="stretch"
    )

    st.subheader(
        "✅ BTTS"
    )

    st.metric(
        "BTTS",
        "67%"
    )

    st.subheader(
        "🎲 Score Exact Poisson"
    )

    scores=[]

    for h in range(6):

        for a in range(6):

            p = (
                poisson(1.8,h)
                *
                poisson(1.2,a)
            ) * 100

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

    st.subheader("🤖 Analyse IA")

    st.info("""
✅ Victoire domicile probable

✅ Over 2.5 conseillé

✅ BTTS conseillé

🎲 Score exact :
2-1

Confiance : 78%
""")

fixture_info = api_get(
    f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
)

home_id = fixture_info["response"][0]["teams"]["home"]["id"]
away_id = fixture_info["response"][0]["teams"]["away"]["id"]

home_last = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
)
st.subheader("🏠 5 derniers matchs domicile")

rows = []

for m in home_last["response"]:

    rows.append({
        "Date": m["fixture"]["date"][:10],
        "Match":
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}",
        "Score":
            f"{m['goals']['home']}-{m['goals']['away']}"
    })

st.dataframe(
    pd.DataFrame(rows),
    width="stretch"
)
away_last = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
)

st.subheader("📈 Forme récente")

col1,col2 = st.columns(2)

col1.success("✅ ✅ ❌ ✅ ✅")
col2.success("✅ ❌ ✅ ✅ ❌")
V = 3
N = 1
D = 0

st.subheader("⚽ Moyenne de buts")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Buts domicile",
    "1.80"
)

col2.metric(
    "Buts extérieur",
    "1.25"
)

col3.metric(
    "Total",
    "3.05"
)

st.subheader("✅ BTTS")

st.metric(
    "Probabilité",
    "67%"
)
BTTS observé
sur les 5 derniers matchs.

 st.subheader("⚽ Over / Under")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Over 1.5",
    "91%"
)

col2.metric(
    "Over 2.5",
    "76%"
)

col3.metric(
    "Over 3.5",
    "48%"
)

st.subheader("⚽ Over / Under")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Over 1.5",
    "91%"
)

col2.metric(
    "Over 2.5",
    "76%"
)

col3.metric(
    "Over 3.5",
    "48%"
)

st.subheader("⚔️ Confrontations directes")
    2025
Liverpool 2-1 Arsenal

2025
Arsenal 1-1 Liverpool

2024
Liverpool 3-0 Arsenal

st.subheader("🎯 Buteurs Probables")

buteurs = pd.DataFrame({
    "Joueur":[
        "Mbappé",
        "Haaland",
        "Salah"
    ],
    "Probabilité":[
        "68%",
        "61%",
        "54%"
    ]
})

st.dataframe(
    buteurs,
    width="stretch"
)

st.subheader("🤖 Analyse IA")
st.info(f"""
🏟 Match :
{match_name}

📈 Forme récente :

Domicile : 4V 1D

Extérieur : 3V 1N 1D

⚽ Moyenne buts :
3.05

✅ BTTS :
67%

⚽ Over 2.5 :
76%

🎲 Score exact :

2-1

🎯 Buteurs probables :

Mbappé
Haaland
Salah

🤖 Conclusion :

L'équipe domicile présente une meilleure dynamique.

Le modèle recommande :

✅ Victoire domicile

✅ BTTS

✅ Over 2.5

✅ Score exact 2-1

🎯 Confiance :
78%
""")

fixture = api_get(
    f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
)

home_id = fixture["response"][0]["teams"]["home"]["id"]
away_id = fixture["response"][0]["teams"]["away"]["id"]
home_last5 = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
)

away_last5 = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
)

def calcul_forme(matches, team_id):

    points = 0
    buts_marques = 0
    buts_encaisses = 0

    for m in matches["response"]:

        home = m["teams"]["home"]["id"]
        away = m["teams"]["away"]["id"]

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]

        if team_id == home:

            buts_marques += hg
            buts_encaisses += ag

            if hg > ag:
                points += 3
            elif hg == ag:
                points += 1

        else:

            buts_marques += ag
            buts_encaisses += hg

            if ag > hg:
                points += 3
            elif ag == hg:
                points += 1

    return {
        "points": points,
        "buts_marques": buts_marques,
        "buts_encaisses": buts_encaisses
    }
    home_stats = calcul_forme(
    home_last5,
    home_id
)

away_stats = calcul_forme(
    away_last5,
    away_id
)

st.metric(
    "Points Domicile",
    home_stats["points"]
)

st.metric(
    "Points Extérieur",
    away_stats["points"]
)

def calcul_btts(matches):

    total = len(matches["response"])
    ok = 0

    for m in matches["response"]:

        if (
            m["goals"]["home"] > 0
            and
            m["goals"]["away"] > 0
        ):

            ok += 1

    return round(
        (ok / total) * 100,
        1
    )
    home_btts = calcul_btts(home_last5)
away_btts = calcul_btts(away_last5)

btts_final = round(
    (home_btts + away_btts)/2,
    1
)

def calcul_over25(matches):

    total = len(matches["response"])
    ok = 0

    for m in matches["response"]:

        buts = (
            m["goals"]["home"]
            +
            m["goals"]["away"]
        )

        if buts >= 3:
            ok += 1

    return round(
        ok/total*100,
        1
    )

h2h = api_get(
 *  f"https://v3.football.api-sports*io/fixtures/headtohead?h2h={home_i*}-{away_id}"
)
st.subheader("⚔️ *istorique H2H")

rows = []

for ga*e in h2h["response"][:10]:

    ro*s.append({
        "Date":
       *game["fixture"]["date"][:10],

   *    "Match":
        (
           *game["teams"]["home"]["name"]
    *       + " vs "
            +
    *       game["teams"]["away"]["name*]
        ),

        "Score":
   *    (
            str(game["goals"*["home"])
            + "-"
      *     +
            str(game["goals*]["away"])
        )
    })

st.da*aframe(
    pd.DataFrame(rows),
  * width="stretch"
)
home_wins = 0
away_wins = 0
draws * 0

for game in h2h["response"]:

*   hg = game["goals"]["home"]
    *g = game["goals"]["away"]

    if *g > ag:
        home_wins += 1

  * elif hg < ag:
        away_wins +* 1

    else:
        draws += 1
 *
 col1,col*,col3 = st.columns(3)

col1.metric*
    "🏠 Victoires",
    home_wins*)

col2.metric(
    "🤝 Nuls",
   *draws
)

col3.metric(
    "🛫 Vict*ires",
    away_wins
)

home_avg = (
    home_stats["buts*marques"] / 5
)

away_avg = (
    away_stats["buts_marques"] / 5
)

poisson(
    home_avg,
    h
)
*
poisson(
    away_avg,
    a
)

st.info(f"""
🏠 Forme domicile :
{home_stats['points']} points

🛫 Forme extérieur :
{away_stats['points']} points

⚽ BTTS :
{btts_final}%

⚽ Over 2.5 :
{over25_final}%

⚔️ H2H :
{home_wins}V - {draws}N - {away_wins}V

🎲 Score Exact :
{scores[0][0]}

🤖 Recommandation :

Victoire domicile probable

BTTS conseillé

Over 2.5 conseillé
""")
 
