from api_bet365 import get_soccer_live

matches = get_soccer_live()

for match in matches:

    print(
        f"{match['home']} vs {match['away']}"
    )

    print(
        f"Score : {match['score']}"
    )

    print(
        f"Status : {match['status']}"
    )

    print("-" * 30)
