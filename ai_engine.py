from ai_engine import (
    calculate_ai_index,
    calculate_btts,
    calculate_over_under,
    get_ai_level
)

# ai_engine.py

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

  
