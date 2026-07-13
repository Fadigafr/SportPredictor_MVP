import streamlit as st
import pandas as pd

from math import exp
from math import factorial

from api_football import api_get

# =====================================================
# OUTILS
# =====================================================

def poisson(lmbda, k):
    return (lmbda ** k * exp(-lmbda)) / factorial(k)


def calcul_forme(matches, team_id):

    points = 0
    buts_marques = 0
    buts_encaisses = 0

    for match in matches.get("response", []):

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        if team_id == home_id:

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


def calcul_btts(matches):

    total = len(matches.get("response", []))

    if total == 0:
        return 0

    ok = 0

    for match in matches["response"]:

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        if hg > 0 and ag > 0:
            ok += 1

    return round((ok / total) * 100, 1)


def calcul_over25(matches):

    total = len(matches.get("response", []))

    if total == 0:
        return 0

    ok = 0

    for match in matches["response"]:

        buts = (
            (match["goals"]["home"] or 0)
            +
            (match["goals"]["away"] or 0)
        )

        if buts >= 3:
            ok += 1

    return round((ok / total) * 100, 1)


# =====================================================
# PAGE PREDICTIONS
# =====================================================

def predictions_page():

    st.title("🤖 SPORT PREDICTOR IA")

    fixture_id = st.session_state.get(
        "fixture_id"
    )

    if not fixture_id:

        st.warning(
            "Sélectionnez un match dans Calendrier."
        )

        return

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

    st.subheader(
        f"{home_team} vs {away_team}"
    )

    # =====================================================
    # FORME 5 MATCHS
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

    return points, buts_marques
    home_last5 = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
    )

    away_last5 = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
    )

    home_stats = calcul_forme(home_last5, home_id)
    away_stats = calcul_forme(away_last5, away_id)

    st.header("📈 Forme")

    c1, c2 = st.columns(2)

    c1.metric(
        f"{home_team}",
        home_stats["points"]
    )

    c2.metric(
        f"{away_team}",
        away_stats["points"]
    )

    # =====================================================
    # BTTS / OVER UNDER
    # =====================================================

    home_btts = calcul_btts(home_last5)
    away_btts = calcul_btts(away_last5)

    btts_final = round(
        (home_btts + away_btts) / 2,
        1
    )

    home_over = calcul_over25(home_last5)
    away_over = calcul_over25(away_last5)

    over25_final = round(
        (home_over + away_over) / 2,
        1
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "BTTS",
        f"{btts_final}%"
    )

    c2.metric(
        "Over 2.5",
        f"{over25_final}%"
    )

    # =====================================================
    # H2H
    # =====================================================

    st.header("⚔️ H2H")

    h2h = api_get(
        f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}"
    )

    home_wins = 0
    away_wins = 0
    draws = 0

    for match in h2h.get("response", [])[:10]:

        hg = match["goals"]["home"] or 0
        ag = match["goals"]["away"] or 0

        if hg > ag:
            home_wins += 1
        elif ag > hg:
            away_wins += 1
        else:
            draws += 1

    c1, c2, c3 = st.columns(3)

    c1.metric("🏠", home_wins)
    c2.metric("🤝", draws)
    c3.metric("✈️", away_wins)

    # =====================================================
    # POISSON
    # =====================================================
def poisson(lmbda, k):

    return (
        lmbda ** k *
        exp(-lmbda)
    ) / factorial(k)
    
    st.header("🎲 Score Exact Poisson")

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
                *
                poisson(away_avg, a)
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

    st.table(scores[:10])

    predicted_score = scores[0][0]

    predicted_home_goals = int(
        predicted_score.split("-")[0]
    )

    predicted_away_goals = int(
        predicted_score.split("-")[1]
    )

    btts_result = (
        predicted_home_goals > 0
        and
        predicted_away_goals > 0
    )

    total_goals = (
        predicted_home_goals +
        predicted_away_goals
    )

    over25_result = total_goals >= 3
    under25_result = total_goals < 3

        home_avg = max(
        home_goals / 5,
        0.1
    )

    away_avg = max(
        away_goals / 5,
        0.1
    )

    scores = []

    for h in range(6):

        for a in range(6):

            prob = (
                poisson(home_avg, h)
                *
                poisson(away_avg, a)
                * 100
            )

            scores.append(
                (f"{h}-{a}", prob)
            )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    predicted_score = scores[0][0]

    # =====================================================
    # BUTEURS PROBABLES
    # =====================================================
def get_top_scorers(team_id):

    players = api_get(
        f"https://v3.football.api-sports.io/players?team={team_id}&season=2025"
    )

    scorers = []

    for player in players.get("response", []):

        try:

            stats = player["statistics"][0]

            goals = stats["goals"]["total"] or 0

            score = goals * 10

            scorers.append({

                "name":
                player["player"]["name"],

                "score":
                score

            })

        except:
            pass

    scorers = sorted(
        scorers,
        key=lambda x: x["score"],
        reverse=True
    )

    return scorers[:3]
    
    st.header("🥅 Buteurs Probables")

    players = api_get(
        f"https://v3.football.api-sports.io/players?team={home_id}&season=2026"
    )

    scorers = []

    for player in players.get("response", []):

        try:

            stats = player["statistics"][0]

            goals = stats["goals"]["total"] or 0
            appearances = stats["games"]["appearences"] or 1
            minutes = stats["games"]["minutes"] or 0

            score = (
                goals * 0.6
                +
                appearances * 0.2
                +
                (minutes / 90) * 0.2
            )

            scorers.append({
                "name": player["player"]["name"],
                "score": score
            })

        except:
            pass

    scorers = sorted(
        scorers,
        key=lambda x: x["score"],
        reverse=True
    )

    for player in scorers[:3]:

        st.write(
            f"⚽ {player['name']}"
        )

    st.subheader(
        "🥅 Buteurs Probables"
    )

    home_scorers = get_top_scorers(home_id)

    for p in home_scorers:

        st.write(
            f"⚽ {p['name']}"
        )
        
    # =====================================================
    # AI INDEX
    # =====================================================

    poisson_score = min(
        scores[0][1] * 5,
        100
    )

    form_score = (
        home_stats["points"] / 15
    ) * 100

    h2h_score = (
        home_wins /
        max(
            home_wins + away_wins + draws,
            1
        )
    ) * 100

    poisson_score = 80

    form_score = (
        home_points / 15
    ) * 100

    h2h_score = 70

    bookmaker_score = 70

    scorer_score = 70

    home_score = 80

    ai_index = round(

        poisson_score * 0.25 +

        form_score * 0.25 +

        h2h_score * 0.15 +

        bookmaker_score * 0.15 +

        scorer_score * 0.10 +

        home_score * 0.10,

        1

    )

    if ai_index >= 85:
        level = "🔥 ELITE BET"

    elif ai_index >= 70:
        level = "✅ BET FORT"

    elif ai_index >= 55:
        level = "⚠️ BET MOYEN"

    else:
        level = "❌ RISQUE ÉLEVÉ"

    odds = api_get(
        f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"
    )

    home_odd = None

    try:

        bets = (
            odds["response"][0]
            ["bookmakers"][0]
            ["bets"]
        )

        for bet in bets:

            if bet["name"] == "Match Winner":

                home_odd = float(
                    bet["values"][0]["odd"]
                )

                draw_odd = float(
                    bet["values"][1]["odd"]
                )

                away_odd = float(
                    bet["values"][2]["odd"]
                )

                break

    except:
        pass

    if home_odd:

        st.subheader(
            "💰 Cotes Bookmakers"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric("1", home_odd)
        c2.metric("N", draw_odd)
        c3.metric("2", away_odd)

    # =====================================================
    # ANALYSE IA
    # =====================================================

    st.header("🤖 Analyse IA")

    st.metric(
        "AI INDEX",
        f"{ai_index}/100"
    )

    st.success(level)

    st.info(f"""
Match : {home_team} vs {away_team}

Score Exact : {predicted_score}

BTTS : {'OUI' if btts_result else 'NON'}

Over 2.5 : {'OUI' if over25_result else 'NON'}

Under 2.5 : {'OUI' if under25_result else 'NON'}

Forme domicile : {home_stats['points']} pts

Forme extérieur : {away_stats['points']} pts

H2H : {home_wins}V - {draws}N - {away_wins}V
""")

st.header("🚀 Analyse IA")

    st.metric(
        "AI INDEX",
        f"{ai_index}/100"
    )

    st.success(
        f"Score Exact IA : {predicted_score}"
    )
