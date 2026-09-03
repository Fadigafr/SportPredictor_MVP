from api_basketball import get_basketball_games_today
from api_hockey import get_hockey_fixtures
from api_tennis import get_all_fixtures
import json
import os
from datetime import datetime
from results_db import get_learning_bonus
from results_db import (
    get_learning_bonus,
    get_market_bonus
)

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

# =====================================================
# AI INDEX V15.9.1
# =====================================================

def calculate_ai_index(
    poisson_score,
    form_score,
    h2h_score,
    bookmaker_score,
    scorer_score,
    home_score,
    market="1"
):

    # Bonus global IA
    learning_bonus = get_learning_bonus()

    # Bonus spécifique au marché
    market_bonus = get_market_bonus(
        market
    )

    # Score IA de base
    base_ai_index = (

        poisson_score * 0.25 +

        form_score * 0.25 +

        h2h_score * 0.15 +

        bookmaker_score * 0.15 +

        scorer_score * 0.10 +

        home_score * 0.10

    )

    # Score final
    ai_index = (
        base_ai_index
        + learning_bonus
        + market_bonus
    )

    # Limites de sécurité
    ai_index = max(
        0,
        min(ai_index, 100)
    )

    # Logs debug
    print("=" * 50)
    print("AI LEARNING IMPACT")
    print("=" * 50)

    print(
        f"Base AI Index = {round(base_ai_index, 2)}"
    )

    print(
        f"Learning Bonus = {learning_bonus}"
    )

    print(
        f"Market Bonus = {market_bonus}"
    )

    print(
        f"AI Index Final = {round(ai_index, 2)}"
    )

    print("=" * 50)

    return round(
        ai_index,
        2
    )


# =====================================================
# BTTS
# =====================================================

def calculate_btts(
    predicted_home_goals,
    predicted_away_goals
):

    return (
        predicted_home_goals > 0
        and
        predicted_away_goals > 0
    )


# =====================================================
# OVER / UNDER
# =====================================================

def calculate_over_under(
    home_goals,
    away_goals
):

    total = (
        home_goals +
        away_goals
    )

    return {

        "over25": total >= 3,

        "under25": total < 3,

        "total_goals": total

    }


# =====================================================
# AI LEVEL
# =====================================================

def get_ai_level(ai_index):

    if ai_index >= 90:
        return "🏆 SUPER ELITE"

    elif ai_index >= 85:
        return "🔥 ELITE BET"

    elif ai_index >= 70:
        return "✅ BET FORT"

    elif ai_index >= 55:
        return "⚠️ BET MOYEN"

    return "❌ RISQUE ÉLEVÉ"


# =====================================================
# ANALYSE COMPLÈTE MATCH
# =====================================================

def build_match_analysis(
    poisson_score,
    form_score,
    h2h_score,
    bookmaker_score,
    scorer_score,
    home_score,
    predicted_home_goals,
    predicted_away_goals,
    market="1"
):

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
        home_score,
        market
    )

    learning_bonus = get_learning_bonus()

    market_bonus = get_market_bonus(
    "1"
    )

    market_rate = get_market_success_rate(
    "1"
    )

    return {

        "ai_index": ai_index,

        "confidence": get_ai_level(
            ai_index
        ),

        "btts": btts_result,

        "over25": ou_result["over25"],

        "under25": ou_result["under25"],

        "total_goals": ou_result["total_goals"],

        "learning_impact": {

            "global_bonus": get_learning_bonus(),

            "market_bonus": get_market_bonus(
                market
            ),

            "market": market

        }

    }
    
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

def get_football_combo():

    predictions = get_top_predictions()

    football_matches = [
        bet
        for bet in predictions
        if bet["sport"] == "Football"
    ]

    return football_matches
    
def save_prediction(
    sport,
    match,
    prediction,
    ai_index,
    odd
):
    filename = "predictions_history.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sport": sport,
        "match": match,
        "prediction": prediction,
        "ai_index": ai_index,
        "odd": odd,
        "result": "PENDING"
    })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def calculate_performance():

    filename = "predictions_history.json"

    if not os.path.exists(filename):
        return {
            "wins": 0,
            "losses": 0,
            "roi": 0
        }

    with open(filename, "r") as f:
        bets = json.load(f)

    wins = len([
        b for b in bets
        if b["result"] == "WIN"
    ])

    losses = len([
        b for b in bets
        if b["result"] == "LOSS"
    ])

    total = wins + losses

    if total == 0:
        roi = 0
    else:
        roi = round(
            (wins / total) * 100,
            1
        )

    return {
        "wins": wins,
        "losses": losses,
        "roi": roi
    }
    
def get_stats_by_sport():

    {
       "Football": {
           "wins": 25,
           "losses": 8
       },
       "Basketball": {
           "wins": 18,
           "losses": 9
       }
    }
