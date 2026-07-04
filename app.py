import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from math import exp, factorial

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Sport Predictor Ultra",
    layout="wide"
)

# --------------------------------------------------
# FONCTIONS
# --------------------------------------------------

def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

def poisson(l, k):
    return (l ** k * exp(-l)) / factorial(k)

# --------------------------------------------------
# SQLITE
# --------------------------------------------------

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

# --------------------------------------------------
# SESSION
# --------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

m = st.sidebar.radio(
    "Accès",
    ["Login", "Inscription"]
)

e = st.text_input("Email")
p = st.text_input(
    "Mot de passe",
    type="password"
)

if m == "Inscription":

    if st.button("Créer compte"):

        try:

            c.execute(
                """
                INSERT INTO users(email,password)
                VALUES(?,?)
                """,
                (e, h(p))
            )

            conn.commit()

            st.success("✅ Compte créé")

        except sqlite3.IntegrityError:

            st.error("❌ Email déjà utilisé")

if m == "Login":

    if st.button("Connexion"):

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

# --------------------------------------------------
# DECONNEXION
# --------------------------------------------------

if st.session_state.user:

    st.sidebar.success(
        f"✅ {st.session_state.user}"
    )

    if st.sidebar.button("🚪 Déconnexion"):

        st.session_state.user = None

        st.rerun()

# --------------------------------------------------
# MENU PRINCIPAL
# --------------------------------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "⚽ Football",
        "🎾 Tennis",
        "🏒 Hockey",
        "🏆 Compétitions",
        "📊 Classements",
        "👥 Joueurs",
        "📺 Live",
        "📅 Avant-match",
        "📈 Prédictions",
        "📉 Statistiques Avancées",
        "👑 Admin"
    ]
)

# --------------------------------------------------
# ACCUEIL
# --------------------------------------------------

if menu == "🏠 Accueil":

    st.title("🏠 Sport Predictor")

    col1, col2, col3 = st.columns(3)

    col1.metric("Précision IA", "78%")
    col2.metric("Matchs analysés", "3250")
    col3.metric("Pronostics", "18750")

# --------------------------------------------------
# FOOTBALL
# --------------------------------------------------

elif menu == "⚽ Football":

    st.title("⚽ Football")

    st.write("Calendrier, statistiques et compétitions")

# --------------------------------------------------
# TENNIS
# --------------------------------------------------

elif menu == "🎾 Tennis":

    st.title("🎾 Tennis")

# --------------------------------------------------
# HOCKEY
# --------------------------------------------------

elif menu == "🏒 Hockey":

    st.title("🏒 Hockey")

# --------------------------------------------------
# COMPETITIONS
# --------------------------------------------------

elif menu == "🏆 Compétitions":

    st.title("🏆 Compétitions")

# --------------------------------------------------
# CLASSEMENTS
# --------------------------------------------------

elif menu == "📊 Classements":

    st.title("📊 Classements")

# --------------------------------------------------
# JOUEURS
# --------------------------------------------------

elif menu == "👥 Joueurs":

    st.title("👥 Joueurs")

# --------------------------------------------------
# LIVE
# --------------------------------------------------

elif menu == "📺 Live":

    st.title("🔴 Matchs en direct")

    st.write("""
⚽ Liverpool 2-1 Arsenal

⚽ Real Madrid 1-0 Barcelone

⚽ PSG 3-1 Marseille
""")

# --------------------------------------------------
# AVANT MATCH
# --------------------------------------------------

elif menu == "📅 Avant-match":

    st.title("📅 Calendrier & Analyse")

    st.write("""
Arsenal vs Chelsea

Liverpool vs Tottenham

Real Madrid vs Atletico
""")

# --------------------------------------------------
# PREDICTIONS
# --------------------------------------------------

elif menu == "📈 Prédictions":

    st.title("📈 Prédictions IA")

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
        f"{round((total/2.5)*50,1)}%"
    )

    btts = min(
        round(buts_dom * buts_ext * 25, 1),
        95
    )

    st.metric("BTTS", f"{btts}%")

    scores = []

    for home in range(6):

        for away in range(6):

            p_score = (
                poisson(buts_dom, home)
                * poisson(buts_ext, away)
                * 100
            )

            scores.append(
                (
                    f"{home}-{away}",
                    round(p_score, 2)
                )
            )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    st.subheader("Score Exact")

    st.table(scores[:5])

# --------------------------------------------------
# STATS AVANCEES
# --------------------------------------------------

elif menu == "📉 Statistiques Avancées":

    st.title("📉 Statistiques Avancées")

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

        st.metric("xG Domicile", 1.92)
        st.metric("xG Extérieur", 1.14)

    elif onglet == "Forme":

        st.write("✅ ✅ ✅ ❌ ✅")

    elif onglet == "H2H":

        st.write("3V - 1N - 1D")

    elif onglet == "Possession":

        st.write("58 %")

    elif onglet == "Tirs":

        st.write("15 tirs | 6 cadrés")

    elif onglet == "Buteurs":

        data = {
            "Rang": ["🥇", "🥈", "🥉"],
            "Joueur": ["Haaland", "Mbappé", "Kane"]
        }

        st.dataframe(
            pd.DataFrame(data),
            width="stretch"
        )

# --------------------------------------------------
# ADMIN
# --------------------------------------------------

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
