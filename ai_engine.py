from api_basketball import get_games_today
from api_hockey import get_hockey_fixtures
from api_tennis import get_all_fixtures

# ai_engine.py

def get_today_predictions():

    predictions = []

    # Football
    try:

        predictions.append({
            "sport": "Football",
            "match": "PSG vs Marseille",
            "ai_index": 92,
            "confidence": "ELITE"
        })

    except Exception:
        pass

    # Basketball
    try:

        games = get_games_today()

        for game in games[:5]:

            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]

            ai_index = 80

            predictions.append({
                "sport": "Basketball",
                "match": f"{home} vs {away}",
                "ai_index": ai_index,
                "confidence": get_ai_level(ai_index)
            })

    except Exception:
        pass

    # Tennis
    try:

        tennis_data = get_all_fixtures()

        for match in tennis_data.get("data", [])[:5]:

            player1 = match["player1"]["name"]
            player2 = match["player2"]["name"]

            ai_index = 78

            predictions.append({
                "sport": "Tennis",
                "match": f"{player1} vs {player2}",
                "ai_index": ai_index,
                "confidence": get_ai_level(ai_index)
            })

    except Exception:
        pass

    # Hockey
    try:

        games = get_hockey_fixtures()

        for game in games[:5]:

            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]

            ai_index = 76

            predictions.append({
                "sport": "Hockey",
                "match": f"{home} vs {away}",
                "ai_index": ai_index,
                "confidence": get_ai_level(ai_index)
            })

    except Exception:
        pass

    return predictions

def get_top_predictions():

    predictions = get_today_predictions()

    return sorted(
        predictions,
        key=lambda x: x["ai_index"],
        reverse=True
    )

def calculate_ai_index(
    poisson_score,
    form_score,
    h2h_score,
    bookmaker_score,
    scorer_score,
    home_score
):
    ai_index = (

        poisson_score * 0.25 +

        form_score * 0.25 +

        h2h_score * 0.15 +

        bookmaker_score * 0.15 +

        scorer_score * 0.10 +

        home_score * 0.10

    )

    return round(ai_index, 2)

def calculate_btts(
    predicted_home_goals,
    predicted_away_goals
):

    return (
        predicted_home_goals > 0
        and
        predicted_away_goals > 0
    )
    btts_result = calculate_btts(
        predicted_home_goals,
        predicted_away_goals
    )

    ou_result = calculate_over_under(
        predicted_home_goals,
        predicted_away_goals
    )
    ai_index = calculate_ai_index(
        poisson_score,
        form_score,
        h2h_score,
        bookmaker_score,
        scorer_score,
        home_score
    )

def calculate_over_under(
    home_goals,
    away_goals
):

    total = home_goals + away_goals

    return {
        "over25": total >= 3,
        "under25": total < 3
    }

def get_ai_level(ai_index):

    if ai_index >= 85:
        return "🔥 ELITE BET"

    elif ai_index >= 70:
        return "✅ BET FORT"

    elif ai_index >= 55:
        return "⚠️ BET MOYEN"

    return "❌ RISQUE ÉLEVÉ"

def get_value_bets():

    value_bets = []

    for bet in get_top_predictions():

        ai_prob = bet["ai_index"]

        book_prob = max(
            50,
            ai_prob - 12
        )

        value = round(
            ai_prob - book_prob,
            1
        )

        value_bets.append({
            "sport": bet["sport"],
            "match": bet["match"],
            "ai_prob": ai_prob,
            "book_prob": book_prob,
            "value": value
        })

    return sorted(
        value_bets,
        key=lambda x: x["value"],
        reverse=True
    )

def get_multisport_combo():

    top_predictions = get_top_predictions()

    combo = top_predictions[:5]

    return combo

def get_optimized_combo():

    predictions = get_top_predictions()

    combo = []
    sports_used = set()

    for bet in predictions:

        if bet["sport"] not in sports_used:

            combo.append(bet)
            sports_used.add(bet["sport"])

    return combo
