import streamlit as st
from math import exp, factorial

from api_football import api_get


# =====================================================
# POISSON
# =====================================================

def poisson(lmbda, k):

    return (
        (lmbda ** k)
        * exp(-lmbda)
    ) / factorial(k)


# =====================================================
# FORME EQUIPE
# =====================================================

def calcul_forme(matches, team_id):

    points = 0
    buts_marques = 0

    for match in matches.get("response", []):

        home_id = match["teams"]["home"]["id"]

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        if home_id == team_id:

            buts_marques += hg

            if hg > ag:
                points += 3

            elif hg == ag:
                points += 1

        else:

            buts_marques += ag

            if ag > hg:
                points += 3

            elif ag == hg:
                points += 1

    return {
        "points": points,
        "buts_marques": buts_marques
    }


# =====================================================
# BUTEURS
# =====================================================

def get_top_scorers(team_id):

    return []


# =====================================================
# PAGE PRINCIPALE
# =====================================================

def predictions_page():

    st.title("🤖 SPORT PREDICTOR IA")

    if "fixture_id" not in st.session_state:

        st.warning(
            "Sélectionnez un match dans le calendrier."
        )

        return

    fixture_id = st.session_state["fixture_id"]

    fixture = api_get(
        f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    )

    if not fixture.get("response"):

        st.error(
            "Impossible de récupérer le match."
        )

        return

    game = fixture["response"][0]

    home_team = game["teams"]["home"]["name"]
    away_team = game["teams"]["away"]["name"]

    home_id = game["teams"]["home"]["id"]
    away_id = game["teams"]["away"]["id"]
   
st.subheader(
        f"{home_team} vs {away_team}"
    )

    # =====================================================
    # FORME
    # =====================================================

    home_last5 = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
    )

    away_last5 = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
    )

    home_stats = calcul_forme(
        home_last5,
        home_id
    )

    away_stats = calcul_forme(
        away_last5,
        away_id
    )

    c1, c2 = st.columns(2)

    c1.metric(
        f"Forme {home_team}",
        f"{home_stats['points']}/15"
    )

    c2.metric(
        f"Forme {away_team}",
        f"{away_stats['points']}/15"
    )

    # =====================================================
    # POISSON
    # =====================================================

    home_avg = max(
        home_stats["buts_marques"] / 5,
        0.1
    )

    away_avg = max(
        away_stats["buts_marques"] / 5,
        0.1
    )

    scores = []

    for h in range(6):

        for a in range(6):

            prob = (
                poisson(home_avg, h)
                * poisson(away_avg, a)
                * 100
            )

            scores.append(
                (
                    f"{h}-{a}",
                    round(prob, 2)
                )
            )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    predicted_score = scores[0][0]

    predicted_home_goals = int(
        predicted_score.split("-")[0]
    )

    predicted_away_goals = int(
        predicted_score.split("-")[1]
    )

    btts_result = (
        predicted_home_goals > 0
        and predicted_away_goals > 0
    )

    total_goals = (
        predicted_home_goals
        + predicted_away_goals
    )

    over25_result = total_goals >= 3

    # =====================================================
    # AI INDEX SIMPLE
    # =====================================================

    ai_index = min(
        100,
        round(
            (
                home_stats["points"]
                + away_stats["points"]
            ) * 3,
            1
        )
    )

    if ai_index >= 85:
        level = "ELITE BET"

    elif ai_index >= 70:
        level = "BET FORT"

    elif ai_index >= 55:
        level = "BET MOYEN"

    else:
        level = "RISQUE"

    # =====================================================
    # RESULTATS
    # =====================================================

    st.header("🚀 Analyse IA")

    st.metric(
        "AI INDEX",
        f"{ai_index}/100"
    )

    st.info(level)

    st.success(
        f"Score Exact Prévu : {predicted_score}"
    )

    st.write(
        f"BTTS : {'OUI' if btts_result else 'NON'}"
    )

    st.write(
        f"Over 2.5 : {'OUI' if over25_result else 'NON'}"
    )

    st.subheader(
        "Top 10 Scores Probables"
    )

    st.table(scores[:10])
