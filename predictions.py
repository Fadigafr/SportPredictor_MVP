import streamlit as st
import pandas as pd

from api_football import api_get

def predictions_page():

    st.header("📈 Centre de Prédictions")

    module = st.selectbox(
        "Module",
        [
            "🏆 Sélection Match",
            "💰 Cotes",
            "📊 Statistiques",
            "⚽ Over/Under",
            "✅ BTTS",
            "🎲 Score Exact",
            "🤖 Analyse IA"
        ]
    )

    if module == "🏆 Sélection Match":

        leagues = api_get(
            "https://v3.football.api-sports.io/leagues"
        )

        st.write(
            f"{len(leagues.get('response',[]))} compétitions trouvées"
        )

    elif module == "💰 Cotes":

        st.subheader("💰 Cotes Bookmakers")

    elif module == "📊 Statistiques":

        st.subheader("📊 Statistiques Match")

    elif module == "⚽ Over/Under":

        st.subheader("⚽ Over / Under")

    elif module == "✅ BTTS":

        st.subheader("✅ BTTS")

    elif module == "🎲 Score Exact":

        st.subheader("🎲 Score Exact Poisson")

    elif module == "🤖 Analyse IA":

        st.subheader("🤖 Analyse IA")

    elif menu == "📅 Calendrier":

    st.title("📅 Calendrier")

    pays = st.selectbox(
        "🌍 Pays",
        [
            "France",
            "Angleterre",
            "Espagne",
            "Italie",
            "Allemagne"
        ]
    )

    competition = st.selectbox(
        "🏆 Compétition",
        [
            "Championnat",
            "Coupe",
            "Coupe d'Europe"
        ]
    )

    st.subheader("⚽ Matchs programmés")

    fixtures = api_get(
        "https://v3.football.api-sports.io/fixtures?next=50"
    )

    matchs = {}

    for m in fixtures.get("response", []):

        nom = (
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}"
        )

        matchs[nom] = m["fixture"]["id"]

    if matchs:

        match = st.selectbox(
            "Choisir un match",
            list(matchs.keys())
        )

        fixture_id = matchs[match]

     stats = api_get(
            f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
        )

        if len(stats.get("response", [])) >= 2:

            st.subheader("📊 Statistiques Match")

            home = stats["response"][0]
            away = stats["response"][1]

            rows = []

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
            st.subheader("⚔️ Historique H2H")

        fixture = api_get(
            f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
        )

        try:

            home_id = (
                fixture["response"][0]
                ["teams"]["home"]["id"]
            )

            away_id = (
                fixture["response"][0]
                ["teams"]["away"]["id"]
            )

            h2h = api_get(
                f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}"
            )

            rows = []

            for game in h2h.get("response", [])[:10]:

                rows.append({
                    "Date":
                    game["fixture"]["date"][:10],

                    "Match":
                    (
                        game["teams"]["home"]["name"]
                        +
                        " vs "
                        +
                        game["teams"]["away"]["name"]
                    ),

                    "Score":
                    f"{game['goals']['home']}-{game['goals']['away']}"
                })

            st.dataframe(
                pd.DataFrame(rows),
                width="stretch"
            )

        except:
            st.warning("H2H indisponible")

            st.subheader("🎯 Buteurs Probables")

        buteurs = pd.DataFrame({
            "Joueur": [
                "Mbappé",
                "Haaland",
                "Kane"
            ],
            "Probabilité": [
                "68%",
                "61%",
                "55%"
            ]
        })

        st.dataframe(
            buteurs,
            width="stretch"
        )

        st.subheader("🤖 Analyse IA")

        st.info(
            """
✅ Victoire domicile probable

✅ Over 2.5 conseillé

✅ BTTS conseillé

🎲 Score recommandé : 2-1

Confiance : 78 %
"""
        )

elif menu == "📈 Prédictions":

    st.title("📈 Centre de Prédictions")

    prediction_menu = st.selectbox(
        "Module",
        [
            "💰 Cotes",
            "⚽ Over / Under",
            "✅ BTTS",
            "🎲 Score Exact",
            "🤖 Analyse IA",
            "📜 Historique"
        ]
    )

elif menu == "🤖 Analyse IA du Jour":

    st.title("🤖 Top 5 Analyses IA")

    analyses = [
        ["PSG vs Monaco","71%","2-1","Victoire PSG"],
        ["Liverpool vs Arsenal","68%","2-1","Victoire Liverpool"],
        ["Real Madrid vs Bilbao","54%","3-1","Victoire Real"],
        ["Bayern vs Leverkusen","73%","2-2","Match Nul"],
        ["Inter vs Milan","66%","1-1","Match Nul"]
    ]

    for match,btts,score,analyse in analyses:

        with st.container():

            st.subheader(match)

            col1,col2,col3 = st.columns(3)

            col1.metric("BTTS", btts)
            col2.metric("Score Exact", score)
            col3.metric("Pronostic", analyse)

            st.divider()




