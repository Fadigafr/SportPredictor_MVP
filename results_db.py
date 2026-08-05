import json
import os
from datetime import datetime
from api_football import api_get

DB_FILE = "predictions_history.json"

def save_prediction(
    sport,
    match,
    prediction,
    ai_index,
    odd=1.80,
    fixture_id=None
):

    print("SAVE PREDICTION EXECUTED")
    
    if os.path.exists(DB_FILE):

        with open(DB_FILE, "r") as f:
            data = json.load(f)

    else:

        data = []
        
    exists = any(
        bet["sport"] == sport
        and bet["match"] == match
        and bet["prediction"] == prediction
        and bet["result"] == "PENDING"
        for bet in data
    )

    if exists:
        return

    data.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sport": sport,
        "match": match,
        "fixture_id": fixture_id,
        "prediction": prediction,
        "ai_index": ai_index,
        "odd": odd,
        "result": "PENDING"
    })

    print(data)
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_predictions():

    if not os.path.exists(DB_FILE):
        return []

    with open(DB_FILE, "r") as f:
        return json.load(f)

def calculate_real_stats():

    bets = load_predictions()

    wins = 0
    losses = 0

    for bet in bets:

        if bet["result"] == "WIN":
            wins += 1

        elif bet["result"] == "LOSS":
            losses += 1

    total = wins + losses

    if total > 0:

        win_rate = round(
            wins / total * 100,
            1
        )

    else:

        win_rate = 0

    roi = win_rate

    return {
        "wins": wins,
        "losses": losses,
        "total": total,
        "win_rate": win_rate,
        "roi": roi
    }

def get_stats_by_sport():

    bets = load_predictions()

    sports = {}

    for bet in bets:

        sport = bet["sport"]

        if sport not in sports:

            sports[sport] = {
                "wins": 0,
                "losses": 0
            }

        if bet["result"] == "WIN":

            sports[sport]["wins"] += 1

        elif bet["result"] == "LOSS":

            sports[sport]["losses"] += 1

    return sports

def validate_football_results():

    bets = load_predictions()

    updated = False

    for bet in bets:

        if bet.get("sport") != "Football":
            continue

        if bet.get("result") != "PENDING":
            continue

        fixture_id = bet.get("fixture_id")

        if not fixture_id:
            continue

        try:

            data = api_get(
                f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
            )

            if not data.get("response"):
                continue

            match_data = data["response"][0]

            status = match_data["fixture"]["status"]["short"]

            if status != "FT":
                continue

            home_winner = match_data["teams"]["home"]["winner"]
            away_winner = match_data["teams"]["away"]["winner"]

            prediction = bet.get("prediction")

            if prediction == "1" and home_winner:

                bet["result"] = "WIN"

            elif prediction == "2" and away_winner:

                bet["result"] = "WIN"

            elif prediction == "N":

                goals_home = match_data["goals"]["home"]
                goals_away = match_data["goals"]["away"]

                if goals_home == goals_away:
                    bet["result"] = "WIN"
                else:
                    bet["result"] = "LOSS"

            else:

                bet["result"] = "LOSS"

            updated = True

        except Exception as e:

            print("Validation error:", e)

    if updated:

        with open(DB_FILE, "w") as f:

            json.dump(
                bets,
                f,
                indent=4
            )
    
