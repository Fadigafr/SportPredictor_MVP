from api_bet365 import get_soccer_live

if st.button("TEST SPORTS"):

    data = get_live_events_sports()
    st.write(type(data))
    st.json(data)
    
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
