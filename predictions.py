# Predictions module
elif menu == "📈 Prédictions":

    st.title("📈 Centre de Prédictions")

prediction_menu = st.selectbox(
    "Module",
    [
        "🎯 Vue Générale",
        "💰 Cotes",
        "⚽ Over/Under",
        "✅ BTTS",
        "🎲 Score Exact",
        "🤖 Analyse IA",
        "📜 Historique"
    ]
)

# Score exact Poisson
home_xg = 1.8
away_xg = 1.2

scores=[]

for h_score in range(6):

    for a_score in range(6):

        p = (
            poisson(home_xg,h_score)
            *
            poisson(away_xg,a_score)
            *100
        )

        scores.append(
            (
                f"{h_score}-{a_score}",
                round(p,2)
            )
        )

scores = sorted(
    scores,
    key=lambda x:x[1],
    reverse=True
)

#  Analyse IA
st.table(scores[:10])

if st.button("Analyser"):

    home = 57
    draw = 24
    away = 19

    st.metric("🏠 1", f"{home}%")
    st.metric("🤝 X", f"{draw}%")
    st.metric("🛫 2", f"{away}%")

    st.success(
        "Victoire domicile probable"
    )

prediction_menu = st.selectbox(
    "Prédictions",
    [
        "🎯 Vue Générale IA",
        "🤖 Prédictions API",
        "💰 Cotes",
        "⚽ Over/Under",
        "✅ BTTS",
        "🎲 Score Exact",
        "📜 Historique"
    ]
)

elif prediction_menu == "🤖 Prédictions API":

    st.subheader("🤖 Prédiction officielle API-Football")

    fixture_id = st.number_input(
        "Fixture ID",
        min_value=1,
        value=123456
    )

    if st.button("Charger la prédiction"):

        url = (
            f"https://v3.football.api-sports.io/predictions"
            f"?fixture={fixture_id}"
        )

        data = api_get(url)

        if data.get("response"):

            pred = data["response"][0]

            st.success(
                pred["predictions"]["advice"]
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "🏠 Domicile",
                pred["percent"]["home"] + "%"
            )

            c2.metric(
                "🤝 Nul",
                pred["percent"]["draw"] + "%"
            )

            c3.metric(
                "🛫 Extérieur",
                pred["percent"]["away"] + "%"
            )

            st.subheader("📊 Comparaison")

            st.write(
                f"Forme domicile : "
                f"{pred['comparison']['form']['home']}"
            )

            st.write(
                f"Forme extérieur : "
                f"{pred['comparison']['form']['away']}"
            )

            st.write(
                f"Attaque domicile : "
                f"{pred['comparison']['att']['home']}"
            )

            st.write(
                f"Attaque extérieur : "
                f"{pred['comparison']['att']['away']}"
            )
            
