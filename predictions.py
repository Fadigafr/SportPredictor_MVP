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
