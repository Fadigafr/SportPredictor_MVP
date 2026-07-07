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
