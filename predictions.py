import streamlit as st
from math import exp, factorial

from api_football import api_get


# =====================================================
# POISSON
# =====================================================

def poisson(lmbda, k):
    return ((lmbda ** k) * exp(-lmbda)) / factorial(k)


# =====================================================
# FORME
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
# PAGE PREDICTION
# =====================================================

def predictions_page():

    st.title("SPORT PREDICTOR ULTRA PRO IA V5")

    if "fixture_id" not in st.session_state:
        st.warning("Sélectionnez un match.")
        return

    fixture_id = st.session_state["fixture_id"]

    fixture = api_get(
        f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    )

    if not fixture.get("response"):
        st.error("Match introuvable")
        return

    game = fixture["response"][0]

    home_team = game["teams"]["home"]["name"]
    away_team = game["teams"]["away"]["name"]

    home_id = game["teams"]["home"]["id"]
    away_id = game["teams"]["away"]["id"]

    # =====================================================
    # H2H
    # =====================================================

    home_h2h_wins = 0
    away_h2h_wins = 0
    draws = 0

    h2h = api_get(
        f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}&last=10"
    )

    for match in h2h.get("response", []):

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        if hg > ag:
            home_h2h_wins += 1

        elif ag > hg:
            away_h2h_wins += 1

        else:
            draws += 1

    # =====================================================
    # CLASSEMENT
    # =====================================================

    home_rank = 99
    away_rank = 99

    league_id = game["league"]["id"]
    season = game["league"]["season"]

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

    # =====================================================
    # FORME
    # =====================================================

    home_last5 = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
    )

    away_last5 = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
    )

    home_stats = calcul_forme(home_last5, home_id)
    away_stats = calcul_forme(away_last5, away_id)

    # =====================================================
    # POISSON
    # =====================================================

        scores = []

    for h in range(6):

        for a in range(6):

            prob = (
                poisson(adjusted_home_avg, h)
                * poisson(adjusted_away_avg, a)
                * 100
            )

            scores.append(
                (
                    f"{h}-{a}",
                    round(prob, 2)
                )
            )

    predicted_home_goals = round(adjusted_home_avg)
    predicted_away_goals = round(adjusted_away_avg)

    predicted_score = (
        f"{predicted_home_goals}-{predicted_away_goals}"
    )

    # =====================================================
    # FORCE IA V5
    # =====================================================

    home_strength = 50
    away_strength = 50

    home_strength += home_stats["points"]
    away_strength += away_stats["points"]

    if home_rank < away_rank:
        home_strength += 15

    elif away_rank < home_rank:
        away_strength += 15

    if home_h2h_wins > away_h2h_wins:
        home_strength += 10

    elif away_h2h_wins > home_h2h_wins:
        away_strength += 10

    home_strength += 8

    if home_strength > away_strength:

        adjusted_home_avg += 0.50

    elif away_strength > home_strength:

        adjusted_away_avg += 0.50
        home_avg = max(
            home_stats["buts_marques"] / 5,
            0.1
        )

        away_avg = max(
            away_stats["buts_marques"] / 5,
            0.1
        )

        adjusted_home_avg = home_avg
        adjusted_away_avg = away_avg

    # =====================================================
    # SCORE EXACT IA V5.1
    # =====================================================

    adjusted_home_avg = home_avg
    adjusted_away_avg = away_avg

    # =====================================================
    # AJUSTEMENT DES MOYENNES DE BUTS
    # =====================================================

    home_avg = home_avg * (
        home_strength / 100
    )

    away_avg = away_avg * (
        away_strength / 100
    )

    # =====================================================
    # PROBABILITES 1N2
    # =====================================================

    home_win_prob = 0
    draw_prob = 0
    away_win_prob = 0

    for h in range(6):

        for a in range(6):

            prob = (
                poisson(adjusted_home_avg, h)
                * poisson(adjusted_away_avg, a)
                * 100
            )

            if h > a:
                home_win_prob += prob

            elif h == a:
                draw_prob += prob

            else:
                away_win_prob += prob

    total_strength = home_strength + away_strength

    home_factor = home_strength / total_strength
    away_factor = away_strength / total_strength

    home_win_prob = round(
        home_win_prob * home_factor * 2,
        1
    )

    away_win_prob = round(
        away_win_prob * away_factor * 2,
        1
    )

    draw_prob = round(
        max(
            0,
            100 - home_win_prob - away_win_prob
        ),
        1
    )

    # =====================================================
    # AI INDEX
    # =====================================================

    ai_index = min(
        100,
        round(
            (
                home_strength +
                away_strength
            ) / 2,
            1
        )
    )
    
    # =====================================================
    # ANALYSE IA V5.1
    # =====================================================

    ai_reasons = []

    if home_rank < away_rank:
        ai_reasons.append(
            f"{home_team} est mieux classé"
        )

    elif away_rank < home_rank:
        ai_reasons.append(
            f"{away_team} est mieux classé"
        )

    if home_stats["points"] > away_stats["points"]:
        ai_reasons.append(
            f"{home_team} est en meilleure forme"
        )

    elif away_stats["points"] > home_stats["points"]:
        ai_reasons.append(
            f"{away_team} est en meilleure forme"
        )

    if home_h2h_wins > away_h2h_wins:
        ai_reasons.append(
            f"H2H favorable à {home_team}"
        )

    elif away_h2h_wins > home_h2h_wins:
        ai_reasons.append(
            f"H2H favorable à {away_team}"
        )

    if home_avg > away_avg:
        ai_reasons.append(
            f"{home_team} possède la meilleure attaque récente"
        )

    elif away_avg > home_avg:
        ai_reasons.append(
            f"{away_team} possède la meilleure attaque récente"
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

    # =====================================================
    # AFFICHAGE
    # =====================================================

    st.metric(
        "AI INDEX",
        f"{ai_index}/100"
    )

    st.subheader("Probabilités 1N2")

    c1, c2, c3 = st.columns(3)

    c1.metric(home_team, f"{home_win_prob}%")
    c2.metric("Nul", f"{draw_prob}%")
    c3.metric(away_team, f"{away_win_prob}%")

    st.success(recommended_bet)

    st.metric(
        "Confiance IA",
        f"{confidence}%"
    )
    
    # =====================================================
    # ANALYSE IA
    # =====================================================

    st.subheader("🧠 Analyse IA")

    for reason in ai_reasons:
        st.write(f"✅ {reason}")

    st.success(
        f"Score Exact Prévu : {predicted_score}"
    )

    st.table(scores[:10])

    st.info(
        f"L'IA a identifié {len(ai_reasons)} facteurs favorables."
    )
