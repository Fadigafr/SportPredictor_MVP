import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from math import exp, factorial
import requests
import streamlit as st

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

API_KEY = st.secrets["ae93ad8f2d8d02fd33378e042e988d37"]

HEADERS = {
    "x-apisports-key": API_KEY
}
# =======================
# STYLE
# =======================

st.markdown("""
<style>

.stApp{
 background:#0f1117;
 color:white;
}

.block-container{
 padding-top:1rem;
}

.match-card{
 background:#1a1d24;
 border-radius:18px;
 padding:18px;
 margin-bottom:12px;
 border:1px solid #2a2f38;
}

.score{
 font-size:42px;
 color:#FFD700;
 font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =======================
# HASH
# =======================

def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

# =======================
# POISSON
# =======================

def poisson(l,k):
    return (l**k * exp(-l))/factorial(k)

# =======================
# SQLITE
# =======================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =======================
# SESSION
# =======================

if "user" not in st.session_state:
    st.session_state.user = None

# =======================
# LOGIN
# =======================

st.sidebar.title("🔐 Accès")

mode = st.sidebar.radio(
    "",
    ["Login","Inscription"]
)

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input(
    "Mot de passe",
    type="password"
)

if mode == "Inscription":

    if st.sidebar.button("Créer compte"):

        try:

            c.execute(
                """
                INSERT INTO users(email,password)
                VALUES(?,?)
                """,
                (
                    email,
                    h(password)
                )
            )

            conn.commit()

            st.success("✅ Compte créé")

        except:
            st.error("Email déjà utilisé")

if mode == "Login":

    if st.sidebar.button("Connexion"):

        user = c.execute(
            """
            SELECT *
            FROM users
            WHERE email=? AND password=?
            """,
            (
                email,
                h(password)
            )
        ).fetchone()

        if user:

            st.session_state.user = email

            st.success("Connexion OK")

            st.rerun()

# =======================
# LOGOUT
# =======================

if st.session_state.user:

    st.sidebar.success(
        f"✅ {st.session_state.user}"
    )

    if st.sidebar.button("🚪 Déconnexion"):

        st.session_state.user = None

        st.rerun()

# =======================
# MENU
# =======================

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🔴 Live",
        "📅 Avant Match",
        "⚽ Football",
        "🎾 Tennis",
        "🏒 Hockey",
        "🏆 Compétitions",
        "📊 Classements",
        "👥 Joueurs",
        "📈 Prédictions IA",
        "📉 Statistiques",
        "⭐ Favoris",
        "🔔 Alertes",
        "👑 Admin"
    ]
)

# =======================
# ACCUEIL
# =======================
if menu == "🏠 Accueil":

    st.title("🏆 SPORT PREDICTOR ULTRA PRO 2026")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Précision IA","78%")
    c2.metric("Matchs analysés","3250")
    c3.metric("Prédictions","18750")
    c4.metric("VIP","245")

#league_id = 39
season = 2026

url = (
    f"https://v3.football.api-sports.io/standings"
    f"?league={league_id}&season={season}"
)

data = requests.get(
    url,
    headers=HEADERS
).json()
table = []

for team in data["response"][0]["league"]["standings"][0]:

    table.append({
        "Pos": team["rank"],
        "Club": team["team"]["name"],
        "Pts": team["points"]
    })

st.dataframe(table, width="stretch")
team_id = 33

url = (
    f"https://v3.football.api-sports.io/players"
    f"?team={team_id}&season=2026"
)

response = requests.get(
    url,
    headers=HEADERS
).json()
Joueur
Photo
Âge
Nationalité
Club
Position

=======================
# LIVE
# =======================

elif menu == "🔴 Live":

    st.title("🔴 Matchs en direct")

    st.markdown("""
    <div class="match-card">

    <div class="live">
    LIVE 78'
    </div>

    <h2>
    Liverpool vs Arsenal
    </h2>

    <div class="score">
    2 - 1
    </div>

    Victoire Liverpool : 58%

    Nul : 22%

    Arsenal : 20%

    </div>
    """, unsafe_allow_html=True)

elif menu == "🔴 Live":

    st.title("🔴 Matchs en direct")

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    response = requests.get(
        url,
        headers=HEADERS
    ).json()

    for match in response["response"]:

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]

        minute = match["fixture"]["status"]["elapsed"]

        st.markdown(
            f"""
### 🔴 {home} {hg} - {ag} {away}

Minute : {minute}'
"""
        )

# =======================
# AVANT MATCH
# =======================

elif menu == "📅 Avant Match":

    st.title("📅 Calendrier")

    st.write("PSG vs Monaco")
    st.write("Liverpool vs Chelsea")
    st.write("Real Madrid vs Barcelone")

elif menu == "📅 Avant Match":

    st.title("📅 Matchs à venir")

    url = "https://v3.football.api-sports.io/fixtures?next=50"

    response = requests.get(
        url,
        headers=HEADERS
    ).json()

    for match in response["response"]:

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        date = match["fixture"]["date"]

        st.write(f"{date[:16]} | {home} vs {away}")

elif menu == "🏆 Compétitions":

    url = (
        "https://v3.football.api-sports.io/leagues"
    )

    data = requests.get(
        url,
        headers=HEADERS
    ).json()

    leagues = []

    for l in data["response"]:

        leagues.append({
            "Ligue": l["league"]["name"],
            "Pays": l["country"]["name"]
        })

    st.dataframe(leagues, width="stretch")

league_id = 39
season = 2026

url = (
    f"https://v3.football.api-sports.io/standings"
    f"?league={league_id}&season={season}"
)

data = requests.get(
    url,
    headers=HEADERS
).json()

# =======================
# Prediction IA
# =======================

elif menu == "📈 Prédictions IA":

    st.title("🤖 Analyse IA")

    buts_dom = st.number_input(
        "Buts domicile",
        0.0,
        5.0,
        1.8
    )

    buts_ext = st.number_input(
        "Buts extérieur",
        0.0,
        5.0,
        1.2
    )

    total = buts_dom + buts_ext

    st.metric(
        "Over 2.5",
        f"{round((total/2.5)*50,1)}%"
    )

    btts = min(
        round(
            buts_dom*buts_ext*25,
            1
        ),
        95
    )

    st.metric(
        "BTTS",
        f"{btts}%"
    )

    scores=[]

    for home in range(6):

        for away in range(6):

            p = (
                poisson(buts_dom,home)
                *
                poisson(buts_ext,away)
            )

            scores.append(
                (
                    f"{home}-{away}",
                    round(p*100,2)
                )
            )

    scores=sorted(
        scores,
        key=lambda x:x[1],
        reverse=True
    )

    st.subheader("🎯 Scores Exacts")

    st.table(scores[:5])

url = (
    "https://v3.football.api-sports.io/players/topscorers"
    "?league=39&season=2026"
)
/predictions
fixture_id = 123456

url = (
    "https://v3.football.api-sports.io/predictions"
    f"?fixture={fixture_id}"
)

prediction = requests.get(
    url,
    headers=HEADERS
).json()


# =======================
# Statistiques avancées
# =======================

elif menu == "📉 Statistiques":

    onglet = st.selectbox(
        "Analyse",
        [
            "xG",
            "Forme",
            "H2H",
            "Possession",
            "Tirs",
            "Buteurs"
        ]
    )

    if onglet == "xG":

        st.metric("xG domicile",1.92)
        st.metric("xG extérieur",1.14)

    elif onglet == "Forme":

        st.write("✅ ✅ ✅ ❌ ✅")

    elif onglet == "H2H":

        st.write("3V - 1N - 1D")

    elif onglet == "Possession":

        st.write("58%")

    elif onglet == "Tirs":

        st.write("15 tirs | 6 cadrés")

    elif onglet == "Buteurs":

        data = {
            "Rang":["🥇","🥈","🥉"],
            "Joueur":["Haaland","Mbappé","Kane"]
        }

        st.dataframe(
            pd.DataFrame(data),
            width="stretch"
        )

# =======================
# Admin
# =======================

elif menu == "👑 Admin":

    st.title("👑 Dashboard Admin")

    users = pd.read_sql_query(
        """
        SELECT
            id,
            email,
            created_at
        FROM users
        ORDER BY id DESC
        """,
        conn
    )

    st.dataframe(
        users,
        width="stretch"
    )

    st.metric(
        "Nombre utilisateurs",
        len(users)
    )

