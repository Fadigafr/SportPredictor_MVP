import streamlit as st

def admin_page():

    st.header("👑 Dashboard Admin")

    admin_menu = st.selectbox(
        "Administration",
        [
            "📊 Dashboard",
            "👥 Utilisateurs",
            "📜 Historique",
            "⚙️ Paramètres"
        ]
    )

    if admin_menu == "📊 Dashboard":

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Utilisateurs", 0)
        c2.metric("VIP", 0)
        c3.metric("Matchs", 0)
        c4.metric("Prédictions", 0)
