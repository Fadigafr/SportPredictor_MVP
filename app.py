import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from math import exp, factorial

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

# =======================
# STYLE
# =======================

st.markdown("""
<style>

.stApp{
    background-color:#0f1117;
    color:white;
}

div[data-testid="stMetric"]{
    background:#1c2028;
    padding:15px;
    border-radius:15px;
}

.match-card{
    background:#1a1d24;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
    border:1px solid #2e3440;
}

.live{
    color:#ff4b4b;
    font-weight:bold;
}

.score{
    color:#FFD700;
    font-size:40px;
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
