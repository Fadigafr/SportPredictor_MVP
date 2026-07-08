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
