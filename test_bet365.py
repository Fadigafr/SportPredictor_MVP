from api_bet365 import get_soccer_live

matches = get_soccer_live()

for match in matches:

    print(
        match["home"],
        "vs",
        match["away"]
    )

    print(
        match["status"]
    )

    print(
        match["score"]
    )
