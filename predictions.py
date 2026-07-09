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

    st.title("📈 Centre de Prédictions")
    # H2H
    # Score Exact
    # Analyse IA

    # =====================================================
    # COMPÉTITION
    # =====================================================

    leagues = api_get(
        "https://v3.football.api-sports.io/leagues"
    )

    league_dict = {}

    for league in leagues.get("response", []):

        league_dict[
            league["league"]["name"]
        ] = league["league"]["id"]

    if not league_dict:

        st.warning("Aucune compétition disponible.")
        return

    competition = st.selectbox(
        "🏆 Compétition",
        sorted(league_dict.keys())
    )

    league_id = league_dict[competition]

    # =====================================================
    # MATCHES
    # =====================================================

    fixtures = api_get(
        f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2026&next=20"
    )

    matchs = {}

    for match in fixtures.get("response", []):

        nom = (
            f"{match['teams']['home']['name']} vs "
            f"{match['teams']['away']['name']}"
        )

        matchs[nom] = match["fixture"]["id"]

    if not matchs:

        st.warning("Aucun match disponible.")
        return

    match_name = st.selectbox(
        "⚽ Match",
        list(matchs.keys())
    )

    fixture_id = matchs[match_name]

    # =====================================================
    # INFOS MATCH
    # =====================================================

    fixture_info = api_get(
        f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    )

    if not fixture_info.get("response"):

        st.warning("Informations du match indisponibles.")
        return

    home_id = fixture_info["response"][0]["teams"]["home"]["id"]
    away_id = fixture_info["response"][0]["teams"]["away"]["id"]

    # =====================================================
    # STATS MATCH
    # =====================================================

    st.header("📊 Statistiques du Match")

    stats = api_get(
        f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
    )

    if len(stats.get("response", [])) >= 2:

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

    # =====================================================
    # 5 DERNIERS MATCHES
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

    st.header("📈 Forme des équipes")

    col1, col2 = st.columns(2)

    col1.metric(
        "Points domicile (5 matchs)",
        home_stats["points"]
    )

    col2.metric(
        "Points extérieur (5 matchs)",
        away_stats["points"]
    )

    # =====================================================
    # BTTS & OVER
    # =====================================================

    home_btts = calcul_btts(home_last5)
    away_btts = calcul_btts(away_last5)

    btts_final = round(
        (home_btts + away_btts) / 2,
        1
    )

    home_over25 = calcul_over25(home_last5)
    away_over25 = calcul_over25(away_last5)

    over25_final = round(
        (home_over25 + away_over25) / 2,
        1
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "✅ BTTS",
        f"{btts_final}%"
    )

    col2.metric(
        "⚽ Over 2.5",
        f"{over25_final}%"
    )
    
    # =====================================================
    # H2H
    # =====================================================

    st.header("⚔️ Historique H2H")

    h2h = api_get(
        f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}"
    )

    rows = []

    home_wins = 0
    away_wins = 0
    draws = 0

    for game in h2h.get("response", [])[:10]:

        hg = game["goals"]["home"] or 0
        ag = game["goals"]["away"] or 0

        rows.append({
            "Date": game["fixture"]["date"][:10],
            "Match": (
                f"{game['teams']['home']['name']} vs "
                f"{game['teams']['away']['name']}"
            ),
            "Score": f"{hg}-{ag}"
        })

        if hg > ag:
            home_wins += 1

        elif hg < ag:
            away_wins += 1

        else:
            draws += 1

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🏠 Victoires",
            home_wins
        )

        col2.metric(
            "🤝 Nuls",
            draws
        )

        col3.metric(
            "🛫 Victoires",
            away_wins
        )

    else:

        st.warning(
            "Aucune donnée H2H disponible"
        )

    # =====================================================
    # SCORE EXACT
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

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    st.table(scores[:10])

    # =====================================================
    # ANALYSE IA
    # =====================================================

    st.header("🤖 Analyse IA")

    st.info(f"""
🏟 Match : {match_name}

📈 Forme domicile : {home_stats['points']} pts

📈 Forme extérieur : {away_stats['points']} pts

⚔️ H2H :
{home_wins}V - {draws}N - {away_wins}V

✅ BTTS : {btts_final}%

⚽ Over 2.5 : {over25_final}%

🎲 Score Exact recommandé :
{scores[0][0]}

🤖 Recommandation :

✅ Victoire domicile probable

✅ BTTS conseillé

✅ Over 2.5 conseillé
""")
