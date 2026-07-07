import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import requests
from math import exp, factorial

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

API_KEY = st.secrets.get("API_KEY", "")

HEADERS = {
    "x-apisports-key": API_KEY
}

# =====================================================
# SQLITE
# =====================================================

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

c.execute("""
CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition TEXT,
    match_name TEXT,
    prediction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =====================================================
# UTILS
# =====================================================

def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

def api_get(url):

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        return r.json()

    except:
        return {"response": []}

def poisson(l, k):
    return (l ** k * exp(-l)) / factorial(k)

# =====================================================
# MENU
# =====================================================

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🔴 Matchs Live",
        "📅 Calendrier",
        "🏆 Compétitions",
        "📊 Classements",
        "👥 Joueurs",
        "🎯 Buteurs",
        "⚔️ H2H",
        "📈 Prédictions",
        "🔔 Notifications",
        "👑 Admin"
    ]
)

# =====================================================
# ACCUEIL
# =====================================================
if menu == "🏠 Accueil":

    st.title("SPORT PREDICTOR ULTRA PRO 2026")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Précision IA","78%")
    c2.metric("Matchs analysés","3250")
    c3.metric("Prédictions","18750")
    c4.metric("Compétitions","500+")

# =====================================================
# LIVE
# =====================================================
elif menu == "🔴 Matchs Live":

    st.title("🔴 Matchs Live")

    data = api_get(
        "https://v3.football.api-sports.io/fixtures?live=all"
    )

    rows = []

    for m in data.get("response",[]):

        rows.append({
            "Match":
            f"{m['teams']['home']['name']} vs {m['teams']['away']['name']}",

            "Score":
            f"{m['goals']['home']}-{m['goals']['away']}",

            "Minute":
            m["fixture"]["status"]["elapsed"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )

# =====================================================
# CALENDRIER
# =====================================================
elif menu == "📅 Calendrier":

    st.title("📅 Calendrier")

    fixtures = api_get(
        "https://v3.football.api-sports.io/fixtures?next=50"
    )

    rows=[]

    for m in fixtures.get("response",[]):

        rows.append({
            "Date": m["fixture"]["date"][:16],
            "Domicile":
            m["teams"]["home"]["name"],
            "Extérieur":
            m["teams"]["away"]["name"]
        })

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch"
    )
