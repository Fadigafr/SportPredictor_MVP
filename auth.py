import hashlib
import streamlit as st
from database import get_conn

def h(txt):
    return hashlib.sha256(
        txt.encode()
    ).hexdigest()

def login():

    conn = get_conn()
    c = conn.cursor()

    mode = st.sidebar.radio(
        "Accès",
        ["Connexion","Inscription"]
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
                    INSERT INTO users(
                        email,
                        password
                    )
                    VALUES (?,?)
                    """,
                    (email,h(password))
                )

                conn.commit()

                st.success(
                    "Compte créé"
                )

            except:

                st.error(
                    "Email déjà utilisé"
                )

    if mode == "Connexion":

        if st.sidebar.button("Connexion"):

            user = c.execute(
                """
                SELECT *
                FROM users
                WHERE email=?
                AND password=?
                """,
                (
                    email,
                    h(password)
                )
            ).fetchone()

            if user:

                st.session_state.user = email

                st.rerun()
