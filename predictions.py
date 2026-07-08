import pandas as pd
import streamlit as st

from api_football import api_get

from math import exp,factorial

def poisson(l,k):
    return (l**k*exp(-l))/factorial(k)

def predictions_page():

    st.header("📈 Centre de Prédictions")

    leagues = api_get(
        "https://v3.football.api-sports.io/leagues"
    )

    league_dict = {}

    for l in leagues.get("response",[]):

        league_dict[
            l["league"]["name"]
        ] = l["league"]["id"]

    if not league_dict:
        st.warning("Aucune ligue disponible")
        return

    competition = st.selectbox(
        "🏆 Compétition",
        sorted(
            league_dict.keys()
        )
    )

    league_id = league_dict[competition]

    fixtures = api_get(
        f"https://v3.football.api-sports.io/fixtures?league={league_id}&season=2026&next=20"
    )

    matchs = {}

    for m in fixtures.get("response",[]):

        nom = (
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}"
        )

        matchs[nom] = m["fixture"]["id"]

    if not matchs:
        st.warning("Aucun match")
        return

    match_name = st.selectbox(
        "⚽ Match",
        list(matchs.keys())
    )

    fixture_id = matchs[match_name]

    st.subheader("📊 Statistiques Match")

    stats = api_get(
        f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
    )

    if len(stats.get("response",[])) >= 2:

        home = stats["response"][0]
        away = stats["response"][1]

        rows=[]

        for i in range(
            min(
                len(home["statistics"]),
                len(away["statistics"])
            )
        ):

            rows.append({
                "Statistique":
                home["statistics"][i]["type"],

                "Domicile":
                home["statistics"][i]["value"],

                "Extérieur":
                away["statistics"][i]["value"]
            })

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch"
        )

    st.subheader(
        "🎯 Buteurs Probables"
    )

    st.dataframe(
        pd.DataFrame({
            "Joueur":[
                "Haaland",
                "Mbappé",
                "Kane"
            ],
            "Probabilité":[
                "68%",
                "61%",
                "55%"
            ]
        }),
        width="stretch"
    )

    st.subheader(
        "✅ BTTS"
    )

    st.metric(
        "BTTS",
        "67%"
    )

    st.subheader(
        "🎲 Score Exact Poisson"
    )

    scores=[]

    for h in range(6):

        for a in range(6):

            p = (
                poisson(1.8,h)
                *
                poisson(1.2,a)
            ) * 100

            scores.append(
                (
                    f"{h}-{a}",
                    round(p,2)
                )
            )

    scores=sorted(
        scores,
        key=lambda x:x[1],
        reverse=True
    )

    st.table(scores[:10])

    st.subheader("🤖 Analyse IA")

    st.info("""
✅ Victoire domicile probable

✅ Over 2.5 conseillé

✅ BTTS conseillé

🎲 Score exact :
2-1

Confiance : 78%
""")

fixture_info = api_get(
    f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
)

home_id = fixture_info["response"][0]["teams"]["home"]["id"]
away_id = fixture_info["response"][0]["teams"]["away"]["id"]

home_last = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
)
st.subheader("🏠 5 derniers matchs domicile")

rows = []

for m in home_last["response"]:

    rows.append({
        "Date": m["fixture"]["date"][:10],
        "Match":
            f"{m['teams']['home']['name']} vs "
            f"{m['teams']['away']['name']}",
        "Score":
            f"{m['goals']['home']}-{m['goals']['away']}"
    })

st.dataframe(
    pd.DataFrame(rows),
    width="stretch"
)
away_last = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
)

st.subheader("📈 Forme récente")

col1,col2 = st.columns(2)

col1.success("✅ ✅ ❌ ✅ ✅")
col2.success("✅ ❌ ✅ ✅ ❌")
V = 3
N = 1
D = 0

st.subheader("⚽ Moyenne de buts")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Buts domicile",
    "1.80"
)

col2.metric(
    "Buts extérieur",
    "1.25"
)

col3.metric(
    "Total",
    "3.05"
)

st.subheader("✅ BTTS")

st.metric(
    "Probabilité",
    "67%"
)

 st.subheader("⚽ Over / Under")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Over 1.5",
    "91%"
)

col2.metric(
    "Over 2.5",
    "76%"
)

col3.metric(
    "Over 3.5",
    "48%"
)

st.subheader("⚽ Over / Under")

col1,col2,col3 = st.columns(3)

col1.metric(
    "Over 1.5",
    "91%"
)

col2.metric(
    "Over 2.5",
    "76%"
)

col3.metric(
    "Over 3.5",
    "48%"
)

st.subheader("⚔️ Confrontations directes")
   
st.subheader("🎯 Buteurs Probables")

buteurs = pd.DataFrame({
    "Joueur":[
        "Mbappé",
        "Haaland",
        "Salah"
    ],
    "Probabilité":[
        "68%",
        "61%",
        "54%"
    ]
})

st.dataframe(
    buteurs,
    width="stretch"
)

st.subheader("🤖 Analyse IA")
st.info(f"""
🏟 Match :
{match_name}

📈 Forme récente :

Domicile : 4V 1D

Extérieur : 3V 1N 1D

⚽ Moyenne buts :
3.05

✅ BTTS :
67%

⚽ Over 2.5 :
76%

🎲 Score exact :

2-1

🎯 Buteurs probables :

Mbappé
Haaland
Salah

🤖 Conclusion :

L'équipe domicile présente une meilleure dynamique.

Le modèle recommande :

✅ Victoire domicile

✅ BTTS

✅ Over 2.5

✅ Score exact 2-1

🎯 Confiance :
78%
""")

fixture = api_get(
    f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
)

home_id = fixture["response"][0]["teams"]["home"]["id"]
away_id = fixture["response"][0]["teams"]["away"]["id"]

# =====================================================
# H2H
# =====================================================

st.subheader("⚔️ Historique H2H")

h2h = api_get(
    f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={home_id}-{away_id}"
)

rows = []

home_wins = 0
away_wins = 0
draws = 0

for game in h2h.get("response", [])[:10]:

    hg = game["goals"]["home"]
    ag = game["goals"]["away"]

    rows.append({
        "Date": game["fixture"]["date"][:10],
        "Match":
            f"{game['teams']['home']['name']} vs "
            f"{game['teams']['away']['name']}",
        "Score": f"{hg}-{ag}"
    })

    if hg > ag:
        home_wins += 1

    elif hg < ag:
        away_wins += 1

    else:
        draws += 1

if rows:

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏠 Victoires Domicile",
        home_wins
    )

    col2.metric(
        "🤝 Nuls",
        draws
    )

    col3.metric(
        "🛫 Victoires Extérieur",
        away_wins
    )

else:

    st.warning(
        "Aucun historique H2H disponible."
    )
    
home_last5 = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={home_id}&last=5"
)

away_last5 = api_get(
    f"https://v3.football.api-sports.io/fixtures?team={away_id}&last=5"
)

def calcul_forme(matches, team_id):

    points = 0
    buts_marques = 0
    buts_encaisses = 0

    for m in matches["response"]:

        home = m["teams"]["home"]["id"]
        away = m["teams"]["away"]["id"]

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]

        if team_id == home:

            buts_marques += hg
            buts_encaisses += ag

            if hg > ag:
                points += 3
            elif hg == ag:
                points += 1

        else:

            buts_marques += ag
            buts_encaisses += hg

            if ag > hg:
                points += 3
            elif ag == hg:
                points += 1

    return {
        "points": points,
        "buts_marques": buts_marques,
        "buts_encaisses": buts_encaisses
    }
    home_stats = calcul_forme(
    home_last5,
    home_id
)

away_stats = calcul_forme(
    away_last5,
    away_id
)
home_btts = calcul_btts(home_last5)

away_btts = calcul_btts(away_last5)

btts_final = round(
    (home_btts + away_btts) / 2,
    1
)

home_over25 = calcul_over25(home_last5)

away_over25 = calcul_over25(away_last5)

over25_final = round(
    (home_over25 + away_over25) / 2,
    1
)

st.metric(
    "Points Domicile",
    home_stats["points"]
)

st.metric(
    "Points Extérieur",
    away_stats["points"]
)

def calcul_btts(matches):

    if not matches.get("response"):
        return 0

    total = len(matches["response"])
    ok = 0

    for m in matches["response"]:

        if (
            m["goals"]["home"] > 0
            and
            m["goals"]["away"] > 0
        ):
            ok += 1

    return round(
        (ok / total) * 100,
        1
    )

def calcul_over25(matches):

    if not matches.get("response"):
        return 0

    total = len(matches["response"])
    ok = 0

    for m in matches["response"]:

        buts = (
            m["goals"]["home"]
            +
            m["goals"]["away"]
        )

        if buts >= 3:
            ok += 1

    return round(
        ok / total * 100,
        1
    )

h2h = api_get(
 *  f"https://v3.football.api-sports*io/fixtures/headtohead?h2h={home_i*}-{away_id}"
)
st.subheader("⚔️ *istorique H2H")

rows = []

for game in h2h.get("response", [])[:10]:

    rows.append({
        "Date":
            game["fixture"]["date"][:10],

        "Match":
            f"{game['teams']['home']['name']} vs "
            f"{game['teams']['away']['name']}",

        "Score":
            f"{game['goals']['home']}-"
            f"{game['goals']['away']}"
    })


st.da*aframe(
    pd.DataFrame(rows),
  * width="stretch"
)
home_wins = 0
away_wins = 0
draws * 0

for game in h2h["response"]:

*   hg = game["goals"]["home"]
    *g = game["goals"]["away"]

    if *g > ag:
        home_wins += 1

  * elif hg < ag:
        away_wins +* 1

    else:
        draws += 1
 *
 col1,col*,col3 = st.columns(3)

col1.metric*
    "🏠 Victoires",
    home_wins*)

col2.metric(
    "🤝 Nuls",
   *draws
)

col3.metric(
    "🛫 Vict*ires",
    away_wins
)

home_avg = (
    home_stats["buts*marques"] / 5
)

away_avg = (
    away_stats["buts_marques"] / 5
)

poisson(
    home_avg,
    h
)
*
poisson(
    away_avg,
    a
)

st.info(f"""
🏠 Forme domicile :
{home_stats['points']} points

🛫 Forme extérieur :
{away_stats['points']} points

⚽ BTTS :
{btts_final}%

⚽ Over 2.5 :
{over25_final}%

⚔️ H2H :
{home_wins}V - {draws}N - {away_wins}V

🎲 Score Exact :
{scores[0][0]}

🤖 Recommandation :

Victoire domicile probable

BTTS conseillé

Over 2.5 conseillé
""")
 
odds = api_get(
    f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"
)
st.subheader("💰 Cotes Bookmakers")

col1,col2,col3 = st.columns(3)

col1.metric("🏠 1", "1.85")
col2.metric("🤝 X", "3.40")
col3.metric("🛫 2", "4.10")

home_odd = 1.85
draw_odd = 3.40
away_odd = 4.10

home_prob = round((1/home_odd)*100,1)
draw_prob = round((1/draw_odd)*100,1)
away_prob = round((1/away_odd)*100,1)
forme_home = home_stats["points"]
forme_away = away_stats["points"]

ia_score_home = (
    home_prob * 0.5
    +
    forme_home * 2
)

ia_score_away = (
    away_prob * 0.5
    +
    forme_away * 2
)

players = api_get(
    f"https://v3.football.api-sports.io/players?team={home_id}&season=2026"
)
players_away = api_get(
    f"https://v3.football.api-sports.io/players?team={away_id}&season=2026"
)

buteurs = []

for p in players["response"]:

    stats = p["statistics"][0]

    buts = (
        stats["goals"]["total"]
        or 0
    )

    buteurs.append({
        "joueur":
        p["player"]["name"],

        "buts":
        buts
    })
buteurs = sorted(
    buteurs,
    key=lambda x:x["buts"],
    reverse=True
)

st.subheader(
    "🎯 Buteurs Probables"
)

top = pd.DataFrame(
    buteurs[:5]
)

st.dataframe(
    top,
    width="stretch"
)

prob = round(
    (buts / matchs_joues)
    * 100,
    1
)

st.subheader("🤖 Analyse IA Finale")

analyse = f"""
🏟 Match : {match_name}

📈 Forme Domicile : {home_stats['points']} pts

📈 Forme Extérieur : {away_stats['points']} pts

⚔️ H2H :
{home_wins}V - {draws}N - {away_wins}V

✅ BTTS : {btts_final}%

⚽ Over 2.5 : {over25_final}%

🎲 Score Exact recommandé :
{scores[0][0]}

🎯 Buteurs probables :

{buteurs[0]['joueur'] if len(buteurs) > 0 else '-'}

{buteurs[1]['joueur'] if len(buteurs) > 1 else '-'}

{buteurs[2]['joueur'] if len(buteurs) > 2 else '-'}

🤖 Conclusion :

Victoire domicile probable.

BTTS conseillé.

Over 2.5 conseillé.
"""

st.info(analyse)
