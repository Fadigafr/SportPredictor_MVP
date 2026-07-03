import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
st.set_page_config(page_title="Sport Predictor Ultra",layout="wide")
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
elif menu=="👑 Admin":
 st.title("Dashboard Admin")
 st.metric("Utilisateurs",125)
