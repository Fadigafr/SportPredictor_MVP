# Admin module
elif menu == "👑 Admin":

    st.title("👑 Dashboard Admin")

    admin_menu = st.selectbox(
        "Administration",
        [
            "📊 Dashboard",
            "👥 Utilisateurs",
            "📜 Historique",
            "⚙️ Paramètres"
        ]
    )

    if admin_menu == "👥 Utilisateurs":

        users = pd.read_sql_query(
            """
            SELECT *
            FROM users
            ORDER BY created_at DESC
            """,
            conn
        )

        st.dataframe(
            users,
            width="stretch"
        )
