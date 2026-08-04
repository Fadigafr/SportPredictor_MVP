import json
import os
from datetime import datetime

DB_FILE = "predictions_history.json"

def save_prediction(
    sport,
    match,
    prediction,
    ai_index,
    odd=1.80
):

    if os.path.exists(DB_FILE):

        with open(DB_FILE, "r") as f:
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
    
