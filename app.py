import streamlit as st

from auth import login_page
from admin import admin_page
from predictions import predictions_page

st.set_page_config(
    page_title="SPORT PREDICTOR ULTRA PRO 2026",
    layout="wide"
)

st.title("🏆 SPORT PREDICTOR ULTRA PRO 2026")

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

if menu == "🏠 Accueil":

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Précision IA", "78%")
    c2.metric("Matchs analysés", "3250")
    c3.metric("Prédictions", "18750")
    c4.metric("Compétitions", "500+")

elif menu == "📈 Prédictions":

    predictions_page()

elif menu == "👑 Admin":

    admin_page()

else:

    st.info(f"Module : {menu} en cours de développement")
