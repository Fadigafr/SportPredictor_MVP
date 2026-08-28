import json
import os
import sqlite3
from datetime import datetime
from api_football import api_get
from api_hockey import (
    get_hockey_fixture_by_id
)
from api_basketball import (
    get_basketball_fixture_by_id
)
from database import (
    save_prediction_db,
    load_predictions_db,
    update_prediction_result
)
from api_bet365 import (
    get_soccer_live,
    is_finished,
    get_score
)

def validate_bet365_football():

    matches = get_soccer_live()

    for match in matches:

        if not is_finished(match):
            continue

        print(
            f"FT : "
            f"{match['home']} vs {match['away']}"
        )
    
def save_prediction(
    sport,
    match,
    prediction,
    ai_index,
    odd=1.80,
    fixture_id=None
):

    save_prediction_db(
        date=datetime.now().strftime("%Y-%m-%d"),
        sport=sport,
        match=match,
        fixture_id=fixture_id,
        prediction=prediction,
        ai_index=ai_index,
        odd=odd,
        result="PENDING"
    ) 

def load_predictions():

    return load_predictions_db()

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

def validate_football_results_bet365():

    bets = load_predictions()

    live_matches = get_soccer_live()

    updated = False

    for bet in bets:

        if bet.get("sport") != "Football":
            continue

        if bet.get("result") != "PENDING":
            continue

        fixture_id = str(
            bet.get("fixture_id")
        )

        for match in live_matches:

            if str(match["fixture_id"]) != fixture_id:
                continue

            if not is_finished(match):
                continue

            home_score, away_score = get_score(match)

            prediction = bet.get("prediction")

            if prediction == "1":

                result = (
                    "WIN"
                    if home_score > away_score
                    else "LOSS"
                )

            elif prediction == "2":

                result = (
                    "WIN"
                    if away_score > home_score
                    else "LOSS"
                )

            elif prediction == "N":

                result = (
                    "WIN"
                    if home_score == away_score
                    else "LOSS"
                )

            else:

                result = "LOSS"

            update_prediction_result(
                bet["id"],
                result
            )

            updated = True

    return updated

    print("MATCHES LIVE :", len(live_matches))
    
    for bet in bets:

        print(
            "PREDICTION:",
            bet.get("match"),
            bet.get("fixture_id")
        )

    for match in live_matches:

        print(
            "LIVE:",
            match["fixture_id"],
            match["home"],
            "vs",
            match["away"]
        )
    
def validate_football_results():

    bets = load_predictions()

    live_matches = get_soccer_live()

    updated = False

    for bet in bets:

        if bet.get("sport") != "Football":
            continue

        if bet.get("result") != "PENDING":
            continue

        fixture_id = str(
            bet.get("fixture_id")
        )

        for match in live_matches:

            if str(match["fixture_id"]) != fixture_id:
                continue

            if not is_finished(match):
                continue

            home_score, away_score = get_score(match)

            prediction = bet.get("prediction")

            if prediction == "1":

                result = (
                    "WIN"
                    if home_score > away_score
                    else "LOSS"
                )

            elif prediction == "2":

                result = (
                    "WIN"
                    if away_score > home_score
                    else "LOSS"
                )

            elif prediction == "N":

                result = (
                    "WIN"
                    if home_score == away_score
                    else "LOSS"
                )

            else:

                result = "LOSS"

            update_prediction_result(
                bet["id"],
                result
            )

            updated = True

    return updated
    
def get_ai_reliability():

    bets = load_predictions()

    groups = {
        "90+": {"wins": 0, "total": 0},
        "80+": {"wins": 0, "total": 0},
        "70+": {"wins": 0, "total": 0},
        "<70": {"wins": 0, "total": 0}
    }

    for bet in bets:

        if bet.get("result") not in ["WIN", "LOSS"]:
            continue

        ai = bet.get("ai_index", 0)

        if ai >= 90:
            group = "90+"

        elif ai >= 80:
            group = "80+"

        elif ai >= 70:
            group = "70+"

        else:
            group = "<70"

        groups[group]["total"] += 1

        if bet["result"] == "WIN":
            groups[group]["wins"] += 1

    reliability = {}

    for group, stats in groups.items():

        if stats["total"] > 0:

            reliability[group] = round(
                stats["wins"] /
                stats["total"] * 100,
                1
            )

        else:

            reliability[group] = 0

    return reliability

def get_learning_stats():

    bets = load_predictions()

    stats = {
        "1": {"win": 0, "loss": 0},
        "N": {"win": 0, "loss": 0},
        "2": {"win": 0, "loss": 0},
        "HOME": {"win": 0, "loss": 0},
        "AWAY": {"win": 0, "loss": 0}
    }

    for bet in bets:

        if bet["result"] not in ["WIN", "LOSS"]:
            continue

        prediction = bet["prediction"]

        if prediction not in stats:

            stats[prediction] = {
                "win": 0,
                "loss": 0
            }

        if bet["result"] == "WIN":

            stats[prediction]["win"] += 1

        else:

            stats[prediction]["loss"] += 1

    return stats

def get_ai_learning_stats():

    predictions = load_predictions()

    wins = len([
        p for p in predictions
        if p.get("result") == "WIN"
    ])

    losses = len([
        p for p in predictions
        if p.get("result") == "LOSS"
    ])

    pending = len([
        p for p in predictions
        if p.get("result") == "PENDING"
    ])

    total = len(predictions)

    success_rate = (
        round((wins / (wins + losses)) * 100, 1)
        if (wins + losses) > 0
        else 0
    )

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "pending": pending,
        "success_rate": success_rate
    }

def get_learning_bonus():

    stats = get_ai_learning_stats()

    rate = stats["success_rate"]

    if rate >= 80:
        return 8

    elif rate >= 70:
        return 5

    elif rate >= 60:
        return 3

    elif rate >= 50:
        return 1

    return -3

def get_ai_confidence_level():

    stats = get_ai_learning_stats()

    rate = stats["success_rate"]

    if rate >= 80:
        return "🔥 IA ELITE"

    elif rate >= 70:
        return "🚀 IA PREMIUM"

    elif rate >= 60:
        return "✅ IA STABLE"

    elif rate >= 50:
        return "⚠ IA EN APPRENTISSAGE"

    return "🔧 IA À OPTIMISER"
def get_prediction_success_rate(prediction):

    stats = get_learning_stats()

    wins = stats[prediction]["win"]

    losses = stats[prediction]["loss"]

    total = wins + losses

    if total == 0:
        return 50

    return round(
        wins / total * 100,
        1
    )

def get_global_success_rate():

    predictions = load_predictions()

    validated = [
        p for p in predictions
        if p.get("result") in ["WIN", "LOSS"]
    ]

    if len(validated) == 0:
        return 0

    wins = len([
        p for p in validated
        if p.get("result") == "WIN"
    ])

    return round((wins / len(validated)) * 100, 2)

def validate_hockey_results():

    bets = load_predictions()

    for bet in bets:

        if bet.get("sport") != "Hockey":
            continue

        if bet.get("result") != "PENDING":
            continue

        fixture_id = bet.get("fixture_id")

        if not fixture_id:
            continue

        try:

            game_data = get_hockey_fixture_by_id(
                fixture_id
            )

            if not game_data:
                continue

            status = game_data["status"]["short"]

            if status not in ["FT", "AOT", "POST"]:
                continue

            home_score = game_data["scores"]["home"]
            away_score = game_data["scores"]["away"]

            prediction = bet["prediction"]

            if (
                prediction == "HOME"
                and home_score > away_score
            ):

                update_prediction_result(
                    bet["id"],
                    "WIN"
                )

            elif (
                prediction == "AWAY"
                and away_score > home_score
            ):

                update_prediction_result(
                    bet["id"],
                    "WIN"
                )

            else:

                update_prediction_result(
                    bet["id"],
                    "LOSS"
                )

        except Exception as e:

            print(
                "Hockey validation error:",
                e
            )

    print(
        "🏀 Basketball Validation Running"
    )
def validate_basketball_results():

    predictions = load_predictions_db()

    for bet in predictions:

        if bet.get("sport") != "Basketball":
            continue

        if bet.get("result") != "PENDING":
            continue

        fixture_id = bet.get("fixture_id")

        if not fixture_id:
            continue

        try:

            print(
                f"🏀 Validation Basket | Fixture={fixture_id}"
            )
            game = get_basketball_fixture_by_id(
                fixture_id
            )

            if not game:
                continue

            status = game["status"]["short"]

            print(
                f"🏀 Status={status}"
            )

            if status != "FT":
                continue

            home_score = (
                game["scores"]["home"]["total"]
            )

            away_score = (
                game["scores"]["away"]["total"]
            )

            print(
                f"🏀 Score={home_score}-{away_score}"
            )

            prediction = bet["prediction"]

            result = "LOSS"

            if (
                prediction == "HOME"
                and home_score > away_score
            ):
                result = "WIN"

            elif (
                prediction == "AWAY"
                and away_score > home_score
            ):
                result = "WIN"
                
            update_prediction_result(
                bet["id"],
                result
            )

        except Exception as e:

            print(
                f"Basket validation error: {e}"
            )

def get_prediction_stats(
    prediction_type
):

    bets = load_predictions()

    wins = 0
    losses = 0

    for bet in bets:

        if bet.get(
            "prediction"
        ) != prediction_type:
            continue

        if bet.get(
            "result"
        ) == "WIN":

            wins += 1

        elif bet.get(
            "result"
        ) == "LOSS":

            losses += 1

    total = wins + losses

    if total == 0:

        return {
            "wins": 0,
            "losses": 0,
            "success_rate": 50
        }

    return {
        "wins": wins,
        "losses": losses,
        "success_rate": round(
            wins / total * 100,
            1
        )
    }

def count_predictions():

    predictions = load_predictions()

    return len(predictions)

    print("get_global_success_rate OK")

def get_learning_summary():

    stats = get_ai_learning_stats()

    return {
        "success_rate": stats["success_rate"],
        "bonus": get_learning_bonus(),
        "total_predictions": stats["total"]
    }
