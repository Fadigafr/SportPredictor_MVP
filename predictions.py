import streamlit as st
import pandas as pd
from math import exp, factorial

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

odds = api_get(
    f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"
)
home_odd = None
draw_odd = None
away_odd = None

try:

    bookmaker = odds["response"][0]

    bets = bookmaker["bookmakers"][0]["bets"]

    for bet in bets:

        if bet["name"] == "Match Winner":

            home_odd = float(bet["values"][0]["odd"])
            draw_odd = float(bet["values"][1]["odd"])
            away_odd = float(bet["values"][2]["odd"])

except:
    pass

st.header("💰 Cotes")

c1, c2, c3 = st.columns(3)

c1.metric("1", home_odd)
c2.metric("N", draw_odd)
c3.metric("2", away_odd)

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

    st.title("📈 Centre de Prédictions IA")

    fixture_id = st.session_state.get("fixture_id")

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

    book_home = round(
    (1 / home_odd) * 100,
    1
)

book_draw = round(
    (1 / draw_odd) * 100,
    1
)

book_away = round(
    (1 / away_odd) * 100,
    1
)

if value > 10:

    st.success(
        f"✅ VALUE BET détecté (+{round(value,1)}%)"
    )

else:

    st.info(
        "Aucune Value Bet détectée"
    )



    # =====================================================
    # FORME 5 MATCHS
    # =====================================================

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

home_prob = 0
draw_prob = 0
away_prob = 0

for score, prob in scores:

    h = int(score.split("-")[0])
    a = int(score.split("-")[1])

    if h > a:
        home_prob += prob

    elif h == a:
        draw_prob += prob

    else:
        away_prob += prob

st.header("📊 Probabilités IA")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Victoire Domicile",
    f"{round(home_prob,1)}%"
)

c2.metric(
    "Nul",
    f"{round(draw_prob,1)}%"
)

c3.metric(
    "Victoire Extérieur",
    f"{round(away_prob,1)}%"
)

    # =====================================================
    # BUTEURS PROBABLES
    # =====================================================
  def get_top_scorers(team_id):

    players = api_get(
        f"https://v3.football.api-sports.io/players?team={team_id}&season=2026"
    )

    scorers = []

    for player in players.get("response", []):

        try:

            stats = player["statistics"][0]

            goals = stats["goals"]["total"] or 0
            appearances = stats["games"]["appearences"] or 1
            minutes = stats["games"]["minutes"] or 0

            score = (

                goals * 0.60 +

                appearances * 0.20 +

                (minutes / 90) * 0.20

            )

            scorers.append({

                "name":
                player["player"]["name"],

                "score":
                score

            })

        except:
            pass

    return sorted(
        scorers,
        key=lambda x: x["score"],
        reverse=True
    )[:3]

      home_scorers = get_top_scorers(home_id)
away_scorers = get_top_scorers(away_id)

st.header("🥅 Buteurs Probables")

col1, col2 = st.columns(2)

with col1:

    st.subheader(home_team)

    for p in home_scorers:

        st.write(
            f"⚽ {p['name']}"
        )

with col2:

    st.subheader(away_team)

    for p in away_scorers:

        st.write(
            f"⚽ {p['name']}"
        )
        
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

    bookmaker_score = book_home
    scorer_score = min(
    (
        len(home_scorers) * 30
    ),
    100
)
    domicile_score = 80

    ai_index = round(

        poisson_score * 0.25 +

        form_score * 0.25 +

        h2h_score * 0.15 +

        bookmaker_score * 0.15 +

        scorer_score * 0.10 +

        domicile_score * 0.10,

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

      st.header("🚀 SPORT PREDICTOR IA V2")

st.metric(
    "AI INDEX",
    f"{ai_index}/100"
)

st.success(level)

st.markdown(f"""
### Pronostic Final

✅ Score exact : **{predicted_score}**

✅ BTTS : **{'OUI' if btts_result else 'NON'}**

✅ Over 2.5 : **{'OUI' if over25_result else 'NON'}**

✅ Under 2.5 : **{'OUI' if under25_result else 'NON'}**

🏠 Probabilité domicile : **{round(home_prob,1)}%**

🤝 Probabilité nul : **{round(draw_prob,1)}%**

✈️ Probabilité extérieur : **{round(away_prob,1)}%**
""")

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
