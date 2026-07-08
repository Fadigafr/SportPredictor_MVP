import hashlib
import streamlit as st

def h(x):

    return hashlib.sha256(
        x.encode()
    ).hexdigest()

def login_page():

    st.subheader("Connexion")
