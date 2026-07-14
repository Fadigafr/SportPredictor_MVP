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

    # =====================================================
    # H2H
    # =====================================================

    h2h = api_get(
        f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}&last=10"
    )

    home_h2h_wins = 0
    away_h2h_wins = 0
    draws = 0

    for match in h2h.get("response", []):

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        if hg > ag:
            home_h2h_wins += 1

        if ag > hg:
            away_h2h_wins += 1

        else:
            draws += 1

    st.subheader("Historique H2H")

    c1, c2, c3 = st.columns(3)

    c1.metric(home_team, home_h2h_wins)
    c2.metric("Nuls", draws)
    c3.metric(away_team, away_h2h_wins)

    st.subheader(
        f"{home_team} vs {away_team}"
    )

    # =====================================================
    # CLASSEMENT
    # =====================================================

    league_id = game["league"]["id"]
    season = game["league"]["season"]

    home_rank = 99
    away_rank = 99

    standings = api_get(
        f"https://v3.football.api-sports.io/standings?league={league_id}&season={season}"
    )

    if standings.get("response"):

        table = standings["response"][0]["league"]["standings"][0]

        for team in table:

            if team["team"]["id"] == home_id:
                home_rank = team["rank"]

            if team["team"]["id"] == away_id:
                away_rank = team["rank"]

        st.subheader("🏆 Classement")

        col1, col2 = st.columns(2)

        col1.metric(
            home_team,
            f"{home_rank}e"
        )

        col2.metric(
            away_team,
            f"{away_rank}e"
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

    # =====================================================
    # PROBABILITES 1N2
    # =====================================================

    home_win_prob = 0
    draw_prob = 0
    away_win_prob = 0

    for h in range(6):
        for a in range(6):

            prob = (
                poisson(home_avg, h)
                * poisson(away_avg, a)
                * 100
            )

            if h > a:
                home_win_prob += prob

            elif h == a:
                draw_prob += prob

            else:
                away_win_prob += prob

    home_win_prob = round(home_win_prob, 1)
    draw_prob = round(draw_prob, 1)
    away_win_prob = round(away_win_prob, 1)
    
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
    # AI INDEX V3.2
    # =====================================================

    form_score = (
        home_stats["points"]
        + away_stats["points"]
    )

    h2h_score = abs(
        home_h2h_wins - away_h2h_wins
    ) * 5

    ranking_score = max(
        0,
        20 - abs(home_rank - away_rank)
    )

    ai_index = min(
        100,
        round(
            (
                form_score
                + h2h_score
                + ranking_score
            ) * 1.5,
            1
        )
    )

    # =====================================================
    # PARI RECOMMANDE
    # =====================================================

    best_prob = max(
        home_win_prob,
        draw_prob,
        away_win_prob
    )

    if best_prob == home_win_prob:

        recommended_bet = f"Victoire {home_team}"

    elif best_prob == away_win_prob:

        recommended_bet = f"Victoire {away_team}"

    else:

        recommended_bet = "Match Nul"

    confidence = round(
        (
            best_prob * 0.6
            + ai_index * 0.4
        ),
        1
    )
    
    if ai_index >= 90:
        level = "ELITE BET"

    elif ai_index >= 75:
        level = "BET FORT"

    elif ai_index >= 60:
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

    st.subheader("📊 Probabilités 1N2")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        home_team,
        f"{home_win_prob}%"
    )

    c2.metric(
        "Nul",
        f"{draw_prob}%"
    )

    c3.metric(
        away_team,
        f"{away_win_prob}%"
    )

    st.subheader("🎯 Pari Recommandé")

    st.success(
        recommended_bet
    )

    st.metric(
        "Confiance IA",
        f"{confidence}%"
    )

    # =====================================================
    # BADGE CONFIANCE
    # =====================================================

if confidence >= 85:
    st.success("🔥 Confiance TRÈS ÉLEVÉE")

elif confidence >= 70:
    st.success("✅ Confiance ÉLEVÉE")

elif confidence >= 55:
    st.warning("⚠️ Confiance MOYENNE")

else:
    st.error("❌ Confiance FAIBLE")

st.info(
    f"Niveau de confiance : {confidence_level}"
)

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
