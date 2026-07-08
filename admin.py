import streamlit as st
import pandas as pd

from database import get_conn

def admin_page():

    st.header("👑 Administration")

    menu = st.selectbox(
        "Menu",
        [
            "📊 Dashboard",
            "👥 Utilisateurs",
            "📜 Historique"
        ]
    )

    conn = get_conn()

    if menu == "📊 Dashboard":

        users = pd.read_sql_query(
            "SELECT * FROM users",
            conn
        )

        preds = pd.read_sql_query(
            "SELECT * FROM predictions",
            conn
        )

        c1,c2 = st.columns(2)

        c1.metric(
            "Utilisateurs",
            len(users)
        )

        c2.metric(
            "Prédictions",
            len(preds)
        )

    elif menu == "👥 Utilisateurs":

        users = pd.read_sql_query(
            "SELECT * FROM users",
            conn
        )

        st.dataframe(
            users,
            width="stretch"
        )

    elif menu == "📜 Historique":

        hist = pd.read_sql_query(
            """
            SELECT *
            FROM predictions
            ORDER BY id DESC
            """,
            conn
        )

        st.dataframe(
            hist,
            width="stretch"
        )
