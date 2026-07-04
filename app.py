import streamlit as st
import pandas as pd
import sqlite3
import hashlib

st.set_page_config(page_title="Sport Predictor Ultra",layout="wide")

# Fonction de hash du mot de passe
def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

# Base SQLite
conn = sqlite3.connect("users.db", check_same_thread=False)
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

# Interface connexion
m = st.sidebar.radio(
    "Accès",
    ["Login", "Inscription"]
)

e = st.text_input("Email")
p = st.text_input("Mot de passe", type="password")

# Inscription
if m == "Inscription" and st.button("Créer compte"):

    try:

        c.execute(
            """
            INSERT INTO users(email, password)
            VALUES (?, ?)
            """,
            (e, h(p))
        )

        conn.commit()

        st.success("✅ Compte créé")

    except sqlite3.IntegrityError:

        st.error("❌ Email déjà utilisé")

# Initialisation session
if "user" not in st.session_state:
    st.session_state.user = None

# Connexion
if m == "Login" and st.button("Connexion"):

    user = c.execute(
        """
        SELECT *
        FROM users
        WHERE email=? AND password=?
        """,
        (e, h(p))
    ).fetchone()

    if user:

        st.session_state.user = e

        st.success("✅ Connexion réussie")

        st.rerun()

    else:

        st.error("❌ Identifiants incorrects")

# Déconnexion
if st.session_state.user:

    st.sidebar.success(
        f"✅ {st.session_state.user}"
    )

    if st.sidebar.button("🚪 Déconnexion"):

        st.session_state.user = None

        st.rerun()
        
menu=st.sidebar.radio("Navigation",["🏠 Accueil","⚽ Football","🎾 Tennis","🏒 Hockey","🏆 Compétitions","📊 Classements","👥 Joueurs","📈 Prédictions","📉 Statistiques Avancées","👑 Admin"])
if menu=="🏠 Accueil":
 st.title("🏠 Sport Predictor")
 st.metric("Précision IA","78%")
elif menu=="⚽ Football":
 st.title("Football")
elif menu=="🎾 Tennis":
 st.title("Tennis")
elif menu=="🏒 Hockey":
 st.title("Hockey")
elif menu=="🏆 Compétitions":
 st.title("Compétitions")
elif menu=="📊 Classements":
 st.title("Classements")
elif menu=="👥 Joueurs":
 st.title("Joueurs")
elif menu=="📈 Prédictions":
 st.title("Prédictions")
 st.metric("Over 2.5","78%")
 st.metric("BTTS","67%")
elif menu == "📉 Statistiques Avancées":

    st.title("📉 Statistiques Avancées")

    onglet = st.selectbox(
        "Analyse",
        ["xG", "Forme", "H2H", "Possession", "Tirs", "Buteurs"]
    )

    if onglet == "xG":
        st.metric("xG Domicile", 1.92)
        st.metric("xG Extérieur", 1.14)

    elif onglet == "Forme":
        st.write("✅ ✅ ✅ ❌ ✅")

    elif onglet == "H2H":
        st.write("5 derniers matchs : 3V - 1N - 1D")

    elif onglet == "Possession":
        st.write("Possession moyenne : 58%")

    elif onglet == "Tirs":
        st.write("Tirs : 15 | Cadrés : 6")

    elif onglet == "Buteurs":

        data = {
            "Rang": ["🥇", "🥈", "🥉"],
            "Joueur": ["Haaland", "Mbappé", "Kane"]
        }

        st.dataframe(
            pd.DataFrame(data),
            width="stretch"
        )

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "⚽ Football",
        "📺 Live",
        "📅 Avant-match",
        "📈 Prédictions",
        "👑 Admin"
    ]
)

if menu == "📺 Live":

    st.title("🔴 Matchs en direct")

    st.info("API-Football Live Fixtures")

    # URL API
    # /fixtures?live=all

    st.write("""
    ⚽ Liverpool 2-1 Arsenal

    🔴 78'

    ⚽ Real Madrid 1-0 Barça

    🔴 62'
    """)

elif menu == "📅 Avant-match":

    st.title("📅 Calendrier & Analyses")

    st.subheader("Matchs à venir")

    st.write("""
    Arsenal vs Chelsea

    Liverpool vs Tottenham

    Real Madrid vs Atletico
    """)

elif menu == "📈 Prédictions":

    st.title("🤖 Analyse IA")

    equipe1 = st.text_input("Equipe domicile")
    equipe2 = st.text_input("Equipe extérieure")

    forme1 = st.number_input("Forme domicile (%)",0,100,70)
    forme2 = st.number_input("Forme extérieur (%)",0,100,55)

    if st.button("Analyser"):
        avantage = forme1 - forme2

        if avantage > 10:

            prediction = "Victoire domicile"

        elif avantage < -10:

            prediction = "Victoire extérieur"

        else:

            prediction = "Match équilibré"

        st.success(prediction)
        analyse = f'''
{equipe1} possède une forme récente de {forme1}%.

{equipe2} possède une forme récente de {forme2}%.

Le modèle estime :

✅ {prediction}

✅ Over 2.5 probable

✅ BTTS possible
'''

        st.info(analyse)

st.subheader("⚽ Over / Under")

buts_dom = st.number_input(
    "Moyenne buts domicile",
    0.0,
    5.0,
    1.8
)

buts_ext = st.number_input(
    "Moyenne buts extérieur",
    0.0,
    5.0,
    1.2
)

total = buts_dom + buts_ext

st.metric(
    "Over 2.5",
    f"{round((total/2.5)*50,1)} %"
)
btts = min(
    round(
        buts_dom * buts_ext * 25,
        1
    ),
    95
)

st.metric(
    "BTTS",
    f"{btts}%"
)
from math import exp,factorial

def poisson(l,k):
    return (l**k*exp(-l))/factorial(k)

scores=[]

for h in range(6):

    for a in range(6):

        p = poisson(
            buts_dom,
            h
        ) * poisson(
            buts_ext,
            a
        )

        scores.append(
            (
                f"{h}-{a}",
                round(
                    p*100,
                    2
                )
            )
        )

scores = sorted(
    scores,
    key=lambda x:x[1],
    reverse=True
)

st.table(scores[:5])

st.subheader("🎯 Buteurs Probables")

data = {
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
}

st.dataframe(
    pd.DataFrame(data),
    width="stretch"
)

elif menu=="👑 Admin":
 st.title("Dashboard Admin")
 st.metric("Utilisateurs",125)
menu = st.sidebar.selectbox(
    "Menu",
    [
        "🏠 Accueil",
        "👑 Admin"
    ]
)
if menu == "👑 Admin":

    st.title("👑 Dashboard Admin")

    users = pd.read_sql_query(
        """
        SELECT
            id,
            email
        FROM users
        ORDER BY id DESC
        """,
        conn
    )

    st.subheader("👥 Utilisateurs inscrits")

    st.dataframe(
        users,
        width="stretch"
    )

    st.metric(
        "Nombre utilisateurs",
        len(users)
    )

if menu == "👑 Admin":

    st.title("👑 Dashboard Admin")

    users = pd.read_sql_query(
        "SELECT id,email FROM users",
        conn
    )

    st.subheader("👥 Utilisateurs inscrits")

    st.dataframe(users, width="stretch")

    st.metric(
        "Nombre d'utilisateurs",
        len(users)
    )
