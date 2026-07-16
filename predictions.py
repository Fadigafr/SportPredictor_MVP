# =====================================================
# IMPORTS
# =====================================================

import math
import streamlit as st
from api_football import api_get


# =====================================================
# POISSON
# =====================================================

def poisson(lmbda, x):
    return (math.exp(-lmbda) * (lmbda ** x)) / math.factorial(x)


# =====================================================
# KELLY
# =====================================================

def kelly(p, odd):
    if odd <= 1:
        return 0

    b = odd - 1
    q = 1 - p

    value = ((b * p) - q) / b

    return max(value, 0)


# =====================================================
# PAGE PRINCIPALE
# =====================================================

def predictions_page():

    st.title("SPORT PREDICTOR ULTRA PRO IA V6.2")

    if "fixture_id" not in st.session_state:
        st.warning("Sélectionnez un match depuis le calendrier.")
        return

    fixture_id = st.session_state["fixture_id"]

    # =====================================================
    # MATCH
    # =====================================================

    fixture = api_get(
        f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    )

    if not fixture.get("response"):
        st.error("Impossible de charger le match.")
        return

    game = fixture["response"][0]

    home_team = game["teams"]["home"]["name"]
    away_team = game["teams"]["away"]["name"]

    home_id = game["teams"]["home"]["id"]
    away_id = game["teams"]["away"]["id"]

    league_id = game["league"]["id"]
    season = game["league"]["season"]

    st.subheader(f"{home_team} vs {away_team}")

    # =====================================================
    # FORME
    # =====================================================

    home_strength = 55
    away_strength = 45

    # =====================================================
    # INDICE IA
    # =====================================================

    total = home_strength + away_strength

    home_win_prob = round((home_strength / total) * 100, 1)
    away_win_prob = round((away_strength / total) * 100, 1)
    draw_prob = round(100 - home_win_prob - away_win_prob, 1)

    # =====================================================
    # POISSON
    # =====================================================

    home_avg = 1.8
    away_avg = 1.1

    scores = []

    for h in range(6):
        for a in range(6):

            prob = (
                poisson(home_avg, h)
                * poisson(away_avg, a)
                * 100
            )

            scores.append(
                ((h, a), prob)
            )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    predicted_score = scores[0][0]

    # =====================================================
    # VALUE BET
    # =====================================================

    odd_home = 2.20
    odd_draw = 3.20
    odd_away = 3.60

    implied_home = 100 / odd_home
    implied_draw = 100 / odd_draw
    implied_away = 100 / odd_away

    value_home = round(home_win_prob - implied_home, 2)
    value_draw = round(draw_prob - implied_draw, 2)
    value_away = round(away_win_prob - implied_away, 2)

    # =====================================================
    # EV+
    # =====================================================

    ev_home = round(
        (home_win_prob / 100 * odd_home) - 1,
        3
    )

    ev_draw = round(
        (draw_prob / 100 * odd_draw) - 1,
        3
    )

    ev_away = round(
        (away_win_prob / 100 * odd_away) - 1,
        3
    )

    # =====================================================
    # KELLY
    # =====================================================

    kelly_home = round(
        kelly(home_win_prob / 100, odd_home) * 100,
        1
    )

    kelly_draw = round(
        kelly(draw_prob / 100, odd_draw) * 100,
        1
    )

    kelly_away = round(
        kelly(away_win_prob / 100, odd_away) * 100,
        1
    )

    # =====================================================
    # AFFICHAGE
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("1", f"{home_win_prob}%")

    with col2:
        st.metric("N", f"{draw_prob}%")

    with col3:
        st.metric("2", f"{away_win_prob}%")

    st.markdown("---")

    st.subheader("Score Exact IA")

    st.success(
        f"{predicted_score[0]} - {predicted_score[1]}"
    )

    st.markdown("---")

    st.subheader("Value Bet")

    valeurs = [
        ("1", value_home, ev_home, kelly_home),
        ("N", value_draw, ev_draw, kelly_draw),
        ("2", value_away, ev_away, kelly_away),
    ]

    valeurs.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for i, pari in enumerate(valeurs[:3], start=1):

        marche = pari[0]
        value = pari[1]
        ev = pari[2]
        kelly_pct = pari[3]

        st.write(
            f"TOP {i} | {marche} | "
            f"Value={value}% | "
            f"EV={ev} | "
            f"Kelly={kelly_pct}%"
        )

    st.markdown("---")

    meilleur = valeurs[0]

    st.success(
        f"PARI IA RECOMMANDÉ : {meilleur[0]}"
    )
