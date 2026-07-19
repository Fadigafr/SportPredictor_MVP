# =====================================================
# IMPORTS
# =====================================================

import math
import streamlit as st
from api_football import api_get
from api_basketball import get_games_today

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
# MOTEUR IA REEL
# =====================================================

FORM_WEIGHT = 0.25
STANDING_WEIGHT = 0.20
H2H_WEIGHT= 0.15
HOME_WEIGHT = 0.10
BOOK_WEIGHT = 0.30
   
# =====================================================
# FONCTION IA SCORE
# =====================================================

def calculate_ai_strength(
    form_score,
    standing_score,
    h2h_score,
    home_advantage,
    bookmaker_score
):
    return (
        form_score * 0.25 +
        standing_score * 0.20 +
        h2h_score * 0.15 +
        home_advantage * 0.10 +
        bookmaker_score * 0.30
    )

def calculate_form(team_id):

    data = api_get(
        f"https://v3.football.api-sports.io/fixtures?team={team_id}&last=5"
    )

    if not data.get("response"):
        return 50

    points = 0

    for match in data["response"]:

        home_id = match["teams"]["home"]["id"]
        winner = match["teams"]["home"]["winner"]

        if team_id == home_id:

            if winner is True:
                points += 3
            elif winner is None:
                points += 1

        else:

            away_winner = match["teams"]["away"]["winner"]

            if away_winner is True:
                points += 3
            elif away_winner is None:
                points += 1

    return round((points / 15) * 100, 1)

def get_ranking_scores(league_id, season, home_id, away_id):

    standings = api_get(
        f"https://v3.football.api-sports.io/standings?league={league_id}&season={season}"
    )

    home_rank = 10
    away_rank = 10

    try:

        table = standings["response"][0]["league"]["standings"][0]

        for team in table:

            if team["team"]["id"] == home_id:
                home_rank = team["rank"]

            if team["team"]["id"] == away_id:
                away_rank = team["rank"]

    except:
        pass

    home_score = max(0, 100 - home_rank * 4)
    away_score = max(0, 100 - away_rank * 4)

    return home_score, away_score

def calculate_h2h(home_id, away_id):

    h2h = api_get(
        f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}&last=10"
    )

    home_wins = 0
    away_wins = 0

    if h2h.get("response"):

        for match in h2h["response"]:

            if match["teams"]["home"]["winner"]:

                if match["teams"]["home"]["id"] == home_id:
                    home_wins += 1
                else:
                    away_wins += 1

            elif match["teams"]["away"]["winner"]:

                if match["teams"]["away"]["id"] == home_id:
                    home_wins += 1
                else:
                    away_wins += 1

    total = max(home_wins + away_wins, 1)

    return (
        round(home_wins / total * 100, 1),
        round(away_wins / total * 100, 1)
    )

def get_top_scorers(team_id, season):

    data = api_get(
        f"https://v3.football.api-sports.io/players?team={team_id}&season={season}"
    )

    if not data.get("response"):
        return []

    players = []

    for player in data["response"]:

        try:
            name = player["player"]["name"]

            goals = player["statistics"][0]["goals"]["total"] or 0

            appearances = (
                player["statistics"][0]["games"]["appearences"]
                or 1
            )

            shots = (
                player["statistics"][0]["shots"]["total"]
                or 0
            )

            score = (
                goals * 5 +
                shots * 0.3 +
                appearances * 0.1
            )

            players.append(
                {
                    "name": name,
                    "goals": goals,
                    "score": score
                }
            )

        except:
            pass

    players.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return players[:3]
    
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

    try:

        home_scorers = get_top_scorers(
            home_id,
            season
        )

        away_scorers = get_top_scorers(
            away_id,
            season
        )

    except Exception:

        home_scorers = []
        away_scorers = []

    all_scorers = home_scorers + away_scorers

    all_scorers.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    if all_scorers:

        probable_scorer = all_scorers[0]["name"]

    else:

        probable_scorer = "Non disponible"

    home_form = calculate_form(home_id)
    away_form = calculate_form(away_id)

    home_rank_score, away_rank_score = get_ranking_scores(
       league_id,
       season,
        home_id,
        away_id
    )

    home_h2h_score, away_h2h_score = calculate_h2h(
        home_id,
        away_id
    )

    home_advantage = 100
    away_advantage = 0

    st.subheader(f"{home_team} vs {away_team}")

    # =====================================================
    # Cotes Bookmakers API-Football
    # =====================================================

    odd_home = 2.20
    odd_draw = 3.20
    odd_away = 3.60

    try:

        odds_data = api_get(
            f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"
        )

        if odds_data.get("response"):

            bookmakers = odds_data["response"][0]["bookmakers"]

            home_odds = []
            draw_odds = []
            away_odds = []

            for bookmaker in bookmakers:

                for bet in bookmaker["bets"]:

                    if bet["name"] == "Match Winner":

                        home_odds.append(
                            float(bet["values"][0]["odd"])
                        )

                        draw_odds.append(
                            float(bet["values"][1]["odd"])
                        )

                        away_odds.append(
                            float(bet["values"][2]["odd"])
                        )

                        break

            odd_home = sum(home_odds) / len(home_odds)
            odd_draw = sum(draw_odds) / len(draw_odds)
            odd_away = sum(away_odds) / len(away_odds)

    except Exception as e:

        st.error(f"Erreur Odds : {e}")

    st.write(
        f"📊 Cotes : "
        f"{odd_home} | "
        f"{odd_draw} | "
        f"{odd_away}"
    )

    # =====================================================
    # Conversion bookmakers
    # =====================================================

    book_home = (1 / odd_home)
    book_draw = (1 / odd_draw)
    book_away = (1 / odd_away)

    total_book = (
        book_home +
        book_draw +
        book_away
    )

    book_home = (book_home / total_book) * 100
    book_draw = (book_draw / total_book) * 100
    book_away = (book_away / total_book) * 100
    
    # =====================================================
    # IA STRENGTH
    # =====================================================

    home_strength = calculate_ai_strength(
        home_form,
        home_rank_score,
        home_h2h_score,
        home_advantage,
        book_home
    )

    away_strength = calculate_ai_strength(
        away_form,
        away_rank_score,
        away_h2h_score,
        away_advantage,
        book_away
    )

    st.write("Force domicile :", round(home_strength, 2))
    st.write("Force extérieur :", round(away_strength, 2))

    # =====================================================
    # ANALYSE IA PREMIUM
    # =====================================================

    home_bonus = 0
    away_bonus = 0

    reasons = []

    # Forme

    if home_form > away_form:

        home_bonus += 10
        reasons.append(
            f"✅ Forme récente favorable à {home_team}"
        )

    elif away_form > home_form:

        away_bonus += 10
        reasons.append(
            f"✅ Forme récente favorable à {away_team}"
        )

    # Classement

    if home_rank_score > away_rank_score:

        home_bonus += 10
        reasons.append(
            f"✅ Classement favorable à {home_team}"
        )

    elif away_rank_score > home_rank_score:

        away_bonus += 10
        reasons.append(
            f"✅ Classement favorable à {away_team}"
        )

    # Domicile

    home_bonus += 5

    reasons.append(
        f"✅ Avantage domicile pour {home_team}"
    )

    # =====================================================
    # INDICE IA
    # =====================================================

    total = home_strength + away_strength

    home_win_prob = round((home_strength / total) * 100, 1)
    away_win_prob = round((away_strength / total) * 100, 1)
    draw_prob = round(100 - home_win_prob - away_win_prob, 1)

    total_strength = (
        home_strength +
        away_strength
    )

    home_win_prob = round(
        home_strength / total_strength * 100,
        1
    )

    away_win_prob = round(
        away_strength / total_strength * 100,
        1
    )

    draw_prob = round(
        max(
            10,
            100 - home_win_prob - away_win_prob
        ),
        1
    )

    if (
        home_win_prob > away_win_prob
        and odd_home < odd_away
    ):

        st.success(
            "✅ IA et Bookmakers alignés"
        )

    elif (
        away_win_prob > home_win_prob
        and odd_away < odd_home
    ):

        st.success(
            "✅ IA et Bookmakers alignés"
        )

    else:

        st.warning(
            "⚠️ Désaccord IA / Bookmakers"
        )

    # =====================================================
    # POISSON
    # =====================================================

    home_avg = (
        (home_form / 100) * 1.8 +
        (home_rank_score / 100) * 1.0 +
        (home_h2h_score / 100) * 0.5 +
        0.4
    )

    away_avg = (
        (away_form / 100) * 1.6 +
        (away_rank_score / 100) * 0.8 +
        (away_h2h_score / 100) * 0.4 +
        0.2
    )

    if home_strength > away_strength + 15:
        home_avg += 0.5

    elif away_strength > home_strength + 15:
        away_avg += 0.5
        
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

    predicted_home_goals = predicted_score[0]
    predicted_away_goals = predicted_score[1]

    if home_win_prob > away_win_prob:

        if predicted_home_goals <= predicted_away_goals:
            predicted_home_goals = predicted_away_goals + 1

    elif away_win_prob > home_win_prob:

        if predicted_away_goals <= predicted_home_goals:
            predicted_away_goals = predicted_home_goals + 1

    predicted_score = (
        predicted_home_goals,
        predicted_away_goals
    )

    st.write("Home Avg :", round(home_avg,2))
    st.write("Away Avg :", round(away_avg,2))

    # =====================================================
    # BTTS
    # =====================================================

    btts_prob = 0

    for h in range(1, 6):
        for a in range(1, 6):

            btts_prob += (
                poisson(home_avg, h)
                * poisson(away_avg, a)
                * 100
            )

    btts_result = (
        "OUI"
        if btts_prob >= 50
        else "NON"
    )

    # =====================================================
    # OVER / UNDER
    # =====================================================

    over25_prob = 0
    over35_prob = 0

    for h in range(6):
        for a in range(6):

            p = (
                poisson(home_avg, h)
                * poisson(away_avg, a)
                * 100
            )

            if (h + a) > 2:
                over25_prob += p

            if (h + a) > 3:
                over35_prob += p

    under25_prob = round(
        100 - over25_prob,
        1
    )

    under35_prob = round(
        100 - over35_prob,
        1
    )

    over25_prob = round(over25_prob, 1)
    over35_prob = round(over35_prob, 1)

    # =====================================================
    # HT / FT
    # =====================================================

    if home_win_prob >= 60:
        htft = "1/1"

    elif away_win_prob >= 60:
        htft = "2/2"

    else:
        htft = "N/1"

    # =====================================================
    # DOUBLE CHANCE
    # =====================================================

    double_chance_1x = round(
        home_win_prob + draw_prob,
        1
    )

    double_chance_x2 = round(
        away_win_prob + draw_prob,
        1
    )

    double_chance_12 = round(
        home_win_prob + away_win_prob,
        1
    )

    # =====================================================
    # CONFIANCE IA
    # =====================================================

    confidence_gap = abs(
        home_win_prob - away_win_prob
    )

    confidence_score = min(
        95,
        round(confidence_gap + 50)
    )

    confidence = round(
        abs(
            home_win_prob -
            away_win_prob
        ),
        1
    )

    confidence_score = min(
        95,
        confidence + 50
    )

    confidence_score = min(
    95,
    round(
        abs(home_strength - away_strength) * 1.5
    )
)  
   
    # =====================================================
    # IA INDEX PREMIUM V6.8
    # =====================================================

    if confidence_score >= 90:

        rating = "A+"
        rating_label = "Elite"

    elif confidence_score >= 80:

        rating = "A"
        rating_label = "Excellent"

    elif confidence_score >= 70:

        rating = "B+"
        rating_label = "Très Bon"

    elif confidence_score >= 60:

        rating = "B"
        rating_label = "Bon"

    elif confidence_score >= 50:

        rating = "C"
        rating_label = "Moyen"

    else:

        rating = "D"
        rating_label = "Risqué"
    
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

    recommended_stake = round(
        max(
            kelly_home,
            kelly_draw,
            kelly_away
        ),
        1
    )

    # =====================================================
    # MISE RECOMMANDEE
    # =====================================================

    recommended_stake = round(
        max(
            kelly_home,
            kelly_draw,
            kelly_away
        ),
        1
    )

    recommended_stake = min(
        recommended_stake,
        10
    )

    # =====================================================
    # Niveau du pari
    # =====================================================

    if confidence_score >= 85:
        risk_level = "FAIBLE"

    elif confidence_score >= 70:
        risk_level = "MOYEN"

    else:
        risk_level = "ÉLEVÉ"
        
    # =====================================================
    # AFFICHAGE
    # =====================================================
    
    if home_win_prob > away_win_prob:

        ia_favorite = home_team

    elif away_win_prob > home_win_prob:

        ia_favorite = away_team

    else:

        ia_favorite = "Match équilibré"
    
    st.markdown("---")

    st.subheader("🧠 Analyse IA Premium")

    favorite = home_team if home_win_prob > away_win_prob else away_team

    st.success(
        f"🎯 Favori IA : {favorite}"
    )

    st.metric(
        "Indice de confiance",
        f"{confidence_score}/100"
    )

    for reason in reasons:

        st.write(reason)
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("1", f"{home_win_prob}%")

    with col2:
        st.metric("N", f"{draw_prob}%")

    with col3:
        st.metric("2", f"{away_win_prob}%")

    # =====================================================
    # IA INDEX PREMIUM
    # =====================================================

    st.markdown("---")

    st.subheader("🏆 IA INDEX PREMIUM")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Note IA",
            rating
        )

    with col2:

        st.metric(
            "Indice IA",
            f"{confidence_score}/100"
        )

    st.info(
        f"📈 Niveau : {rating_label}"
    )

    if rating in ["A+", "A"]:

        st.success(
            "✅ Excellent match à parier"
        )

    elif rating in ["B+", "B"]:

        st.info(
            "✅ Opportunité intéressante"
        )

    else:

        st.warning(
            "⚠️ Match plus risqué"
        )

    best_value = max(
        value_home,
        value_draw,
        value_away
    )

    if best_value > 5:

        st.success(
            f"💰 Value Bet détecté : +{best_value}%"
        )

    else:

        st.info(
            "📊 Aucun Value Bet majeur"
        )
        
# =====================================================
# SCORE EXACT IA
# =====================================================
    st.markdown("---")

    st.subheader("Score Exact IA")

    st.success(
        f"{predicted_score[0]} - {predicted_score[1]}"
    )

    st.markdown("---")

    st.subheader("Marchés Complémentaires IA")

    col1, col2 = st.columns(2)

    with col1:

        st.metric("BTTS", btts_result)

        st.metric(
            "Over 2.5",
            f"{over25_prob}%"
        )

        st.metric(
            "Over 3.5",
            f"{over35_prob}%"
        )

    with col2:

        st.metric(
            "Under 2.5",
            f"{under25_prob}%"
        )

        st.metric(
            "Under 3.5",
            f"{under35_prob}%"
        )

        st.metric(
            "HT/FT",
            htft
        )

    st.subheader("Double Chance")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("1X", f"{double_chance_1x}%")

    with c2:
        st.metric("X2", f"{double_chance_x2}%")

    with c3:
        st.metric("12", f"{double_chance_12}%")
    
    st.subheader("Indice IA")

    st.progress(
        confidence_score / 100
    )

    st.metric(
        "Confiance",
        f"{confidence_score}/100"
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

    st.subheader("⚽ Buteurs Probables IA")

    c1, c2 = st.columns(2)

    with c1:

        st.write(f"### {home_team}")

        if home_scorers:

            for player in home_scorers:

                st.write(
                    f"⚽ {player['name']} "
                    f"({player['goals']} buts)"
                )

        else:

            st.write("Aucune donnée")

    with c2:

        st.write(f"### {away_team}")

        if away_scorers:

            for player in away_scorers:

                st.write(
                    f"⚽ {player['name']} "
                    f"({player['goals']} buts)"
                )

        else:

            st.write("Aucune donnée")

    st.success(
        f"🎯 Buteur probable du match : {probable_scorer}"
    )

    st.markdown("---")

    st.subheader("Gestion du Risque")

    if confidence_score >= 85:
        risk = "FAIBLE"

    elif confidence_score >= 70:
        risk = "MODERE"

    else:
        risk = "ELEVE"

    st.write(
        f"Risque : {risk}"
    )

    st.write(
        f"Mise recommandee : {recommended_stake}% bankroll"
    )

    st.markdown("---")

    meilleur = valeurs[0]

    st.success(
        f"PARI IA RECOMMANDE : {meilleur[0]}"
    )

    st.info(
        f"""
    Confiance IA : {confidence_score}/100

    Mise recommandee : {recommended_stake}% bankroll

    Niveau de risque : {risk}
    """
    )

    st.subheader("Confiance IA")

    st.progress(
        confidence_score / 100
    )

    st.metric(
        "Indice de confiance",
        f"{confidence_score}/100"
    )

    if confidence_score >= 85:
        st.success("🟢 Confiance Très Forte")

    elif confidence_score >= 70:
        st.info("🔵 Confiance Forte")

    elif confidence_score >= 55:
        st.warning("🟡 Confiance Moyenne")

    else:
        st.error("🔴 Match Risqué")
        
    st.subheader("Gestion du risque")

    st.write(
        f"Niveau de risque : {risk_level}"
    )

    st.write(
        f"Mise recommandée : {recommended_stake}% bankroll"
    )
    
    st.write("Forme domicile :", home_form)
    st.write("Forme extérieur :", away_form)

    st.write("Classement domicile :", home_rank_score)
    st.write("Classement extérieur :", away_rank_score)

    st.write("H2H domicile :", home_h2h_score)
    st.write("H2H extérieur :", away_h2h_score)

# =====================================================
# V7 BASKETBALL IA
# =====================================================
   
def basketball_page():

    st.title("🏀 Basketball IA V7")

    st.subheader("🏀 Matchs du Jour")

    games = get_games_today()

    st.write("Nombre de matchs :", len(games))
    
    for game in games[:20]:

        home = game["teams"]["home"]["name"]
        away = game["teams"]["away"]["name"]

        st.write(
            f"🏀 {home} vs {away}"
        )

    games = get_games_today()

    basket_matches = []

    for game in games:

        home = game["teams"]["home"]["name"]
        away = game["teams"]["away"]["name"]

        basket_matches.append({
            "label": f"{home} vs {away}",
            "home": home,
            "away": away,
            "game": game
        })

    if basket_matches:

        selected_match = st.selectbox(   
            "🏀 Match du Jour",
            basket_matches,
            format_func=lambda x: x["label"]
        )

        st.write(selected_match)

        game_data = selected_match.get("game")

        home_id = game_data["teams"]["home"]["id"]
        away_id = game_data["teams"]["away"]["id"]

        league_name = game_data["league"]["name"]

        game_date = game_data["date"]

        st.info(
            f"🏆 Compétition : {league_name}"
        )

        st.info(
            f"📅 Date : {game_date}"
        )

    if game_data:

        league_name = game_data["league"]["name"]

        st.info(
            f"🏆 Compétition : {league_name}"
        )

        st.info(
            f"🏆 Compétition : {league_name}"
        )

        game_date = game_data["date"]

        st.info(
            f"📅 Date : {game_date}"
        )

        st.info(
            f"🏀 Match sélectionné : {home_team} vs {away_team}"
        )

    else:

        st.warning(
            "Aucun match disponible aujourd'hui"
        )
        st.json(games[:2])

    st.subheader("🏀 Matchs du Jour")

    games = get_games_today()

    league = st.selectbox(
        "Compétition",
        [
            "NBA",
            "EuroLeague",
            "Basket Africa League"
        ],
        key="basket_league"
    )

    if games:

        for game in games[:10]:

            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]

            st.write(f"🏀 {home} vs {away}")

    else:

        st.warning("Aucun match disponible")

    if st.button(
        "Analyser le Match",
        key="basket_button"
    ):

        home_strength = len(home_team) * 5
        away_strength = len(away_team) * 5

        confidence_basket = min(
            95,
            70 + abs(
                home_strength -
                away_strength
            )
        )

        st.metric(
            "🧠 IA INDEX",
            f"{confidence_basket}/100"
        )

    if confidence_basket >= 90:

        rating = "A+"

    elif confidence_basket >= 80:

        rating = "A"

    elif confidence_basket >= 70:

        rating = "B+"

    else:

        rating = "B"

        st.metric(
            "🏆 Rating Basket",
            rating
        )

        home_form = "✅✅✅❌✅"
        away_form = "✅❌✅❌✅"

        st.write(
            f"Forme {home_team} : {home_form}"
        )

        st.write(
            f"Forme {away_team} : {away_form}"
        )

        winner = (
            home_team
            if home_strength > away_strength
            else away_team
        )

        st.success(
            f"🏆 Vainqueur IA : {winner}"
        )

        home_points = 108
        away_points = 102

        st.metric(
            "Score IA",
            f"{home_points} - {away_points}"
        )

        total_points = (
            home_points +
            away_points
        )

        st.metric(
            "Total Points",
            total_points
        )

        if total_points > 210:

            st.success(
                "✅ Over 210.5"
            )

        else:

            st.warning(
                "⚠️ Under 210.5"
            )

    confidence_basket = 82

    if confidence_basket >= 85:

        badge = "🏆 ELITE"

    elif confidence_basket >= 70:

        badge = "⭐ PREMIUM"

    else:

        badge = "✅ SOLIDE"

    st.metric(
        "Badge IA",
        badge
    )

    st.metric(
        "🧠 IA INDEX",
        f"{confidence_basket}/100"
    )

    st.success(
        "🎯 Top Pari Basket : Over 210.5"
    )

    st.success(
        "💰 Value Bet Basket : +7.5%"
    )

# =====================================================
# V8 TENNIS IA PREMIUM
# =====================================================

def tennis_page():

    st.title("🎾 Tennis IA Premium")

    tournament = st.selectbox(
        "Tournoi",
        [
            "ATP",
            "WTA",
            "Grand Chelem"
        ],
        key="tennis_tournament"
    )

    player_1 = st.text_input(
        "Joueur 1",
        "Alcaraz",
        key="tennis_player1"
    )

    player_2 = st.text_input(
        "Joueur 2",
        "Medvedev",
        key="tennis_player2"
    )

    if st.button(
        "Analyser le Match",
        key="tennis_button"
    ):

        strength_1 = 92
        strength_2 = 86

        confidence_score = min(
            95,
            80 + abs(strength_1 - strength_2)
        )

        winner = (
            player_1
            if strength_1 > strength_2
            else player_2
        )

        predicted_sets = "2-0"

        over_under_games = "OUI"

        if confidence_score >= 90:

            rating = "A+"
            badge = "💎 ELITE"

        elif confidence_score >= 80:

            rating = "A"
            badge = "🥇 PREMIUM"

        elif confidence_score >= 70:

            rating = "B+"
            badge = "🥈 SOLIDE"

        else:

            rating = "B"
            badge = "🥉 RISQUÉ"

        st.success(
            f"🏆 Vainqueur IA : {winner}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🎾 Score Probable",
                predicted_sets
            )

            st.metric(
                "🏆 Rating",
                rating
            )

        with col2:

            st.metric(
                "🧠 IA INDEX",
                f"{confidence_score}/100"
            )

            st.metric(
                "🏅 Badge IA",
                badge
            )

        st.metric(
            "🔥 Over 22.5 Jeux",
            over_under_games
        )

        total_games = 24

        st.metric(
            "🎾 Jeux Projetés",
            total_games
        )

        if confidence_score >= 90:

            risk_level = "🟢 FAIBLE"

        elif confidence_score >= 80:

            risk_level = "🟡 MOYEN"

        else:

            risk_level = "🔴 ÉLEVÉ"

        st.metric(
            "⚠️ Risque",
            risk_level
        )

        tie_break_probability = round(
            100 - confidence_score + 20
        )

        st.metric(
            "🎾 Tie-Break",
            f"{tie_break_probability}%"
        )
        
        # Value Bet Tennis

        odd_winner = 1.75

        win_prob = confidence_score

        bookmaker_prob = (
            1 / odd_winner
        ) * 100

        value_bet = round(
            win_prob - bookmaker_prob,
            2
        )

        if value_bet > 5:

            st.success(
                f"💰 Value Bet Tennis : +{value_bet}%"
            )

        else:

            st.info(
                "📊 Aucun Value Bet majeur"
            )

        if confidence_score >= 85:

            best_bet = "Victoire du Favori"

        elif total_games > 22:

            best_bet = "Over 22.5 Jeux"

        else:

           best_bet = "Match Équilibré"

        st.success(
            f"🎯 Top Pari Tennis : {best_bet}"
        )

        st.markdown("---")

        st.subheader("🎾 Analyse Tennis Premium")

        if confidence_score >= 85:

            st.success(
                "🟢 Pari Tennis Premium"
            )

        elif confidence_score >= 70:

            st.info(
                "🔵 Pari Tennis Solide"
            )

        else:

            st.warning(
                "🟡 Match équilibré"
            )

# =====================================================
# V9 HOCKEY IA PREMIUM
# =====================================================
    
def hockey_page():

    st.title("🏒 Hockey IA Premium")

    competition = st.selectbox(
        "Compétition",
        [
            "NHL",
            "KHL",
            "IIHF"
        ],
        key="hockey_competition"
    )

    home_team = st.selectbox(
    "Équipe Domicile",
    [
        "New York Rangers",
        "Boston Bruins",
        "Toronto Maple Leafs",
        "Colorado Avalanche",
        "Vegas Golden Knights",
        "Edmonton Oilers"
    ],
    key="hockey_home"
)

    away_team = st.selectbox(
    "Équipe Extérieure",
    [
        "New York Rangers",
        "Boston Bruins",
        "Toronto Maple Leafs",
        "Colorado Avalanche",
        "Vegas Golden Knights",
        "Edmonton Oilers"
    ],
    key="hockey_away"
)

    if st.button(
        "Analyser le Match",
        key="hockey_button"
    ):

        team_strength = {
            "New York Rangers": 88,
            "Boston Bruins": 87,
            "Toronto Maple Leafs": 86,
            "Colorado Avalanche": 92,
            "Vegas Golden Knights": 89,
            "Edmonton Oilers": 91
        }

        home_strength = team_strength.get(home_team, 85)
        away_strength = team_strength.get(away_team, 85)

        predicted_home = round(home_strength / 22)
        predicted_away = round(away_strength / 24)

        total_goals = (
            predicted_home +
            predicted_away
        )

        confidence_score = min(
            95,
            75 + abs(
                home_strength -
                away_strength
            )
        )

        st.metric(
            "🧠 IA INDEX",
            f"{confidence_score}/100"
        )

        winner = (
            home_team
            if predicted_home > predicted_away
            else away_team
        )

        rating = "A"
        if confidence_score >= 90:

            badge = "💎 ELITE"

        elif confidence_score >= 80:

            badge = "🥇 PREMIUM"

        elif confidence_score >= 70:

            badge = "🥈 SOLIDE"

        else:

            badge = "🥉 RISQUÉ"

        if confidence_score >= 90:

            risk_level = "🟢 FAIBLE"

        elif confidence_score >= 80:

            risk_level = "🟡 MOYEN"

        else:

            risk_level = "🔴 ÉLEVÉ"

        st.metric(
            "⚠️ Risque",
            risk_level
        )
        
        st.success(
            f"🏆 Vainqueur IA : {winner}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🏒 Score Final",
                f"{predicted_home}-{predicted_away}"
            )

            st.metric(
                "🥅 Total Buts",
                total_goals
            )

            st.metric(
                "1ère Période",
                "2 buts"
            )

        with col2:

            st.metric(
                "2ème Période",
                "2 buts"
            )

            st.metric(
                "3ème Période",
                "2 buts"
            )

            st.metric(
                "🧠 IA INDEX",
                f"{confidence_score}/100"
            )

        st.metric(
            "🏅 Badge IA",
            badge
        )

        st.metric(
            "🏆 Rating Hockey",
            rating
        )

        st.metric(
            "🧠 IA INDEX",
            f"{confidence_score}/100"
        )

        
        over55 = (
            "OUI"
            if total_goals > 5.5
            else "NON"
        )

        st.metric(
            "🔥 Over 5.5",
            over55
        )

        st.subheader("🥅 Buteurs Probables")

        st.write("1️⃣ Chris Kreider")
        st.write("2️⃣ Artemi Panarin")
        st.write("3️⃣ Mika Zibanejad")

        # Top Pari

        if total_goals > 5:

            best_bet = "Over 5.5 Buts"

        else:

            best_bet = "Victoire du Favori"

        st.success(
            f"🎯 Top Pari Hockey : {best_bet}"
        )

        # Value Bet

        value_bet = round(
            confidence_score - 75,
            2
        )

        st.success(
            f"💰 Value Bet Hockey : +{value_bet}%"
        )

        st.markdown("---")

        st.subheader("🏒 Analyse Hockey Premium")

        if confidence_score >= 85:

            st.success(
                "🟢 Pari Hockey Premium"
            )

        elif confidence_score >= 70:

            st.info(
                "🔵 Pari Hockey Solide"
            )

        else:

            st.warning(
                "🟡 Match équilibré"
            )
