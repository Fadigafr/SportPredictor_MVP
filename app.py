import streamlit as st, requests, pandas as pd

st.set_page_config(page_title="Sport Predictor", layout="wide")
API_KEY = st.secrets.get("API_KEY","")
headers={"x-apisports-key":API_KEY}

st.title("⚽ Sport Predictor MVP")

league=st.number_input("ID Ligue", value=39)
season=st.number_input("Saison", value=2025)

if st.button("Charger les matchs"):
    url=f"https://v3.football.api-sports.io/fixtures?league={league}&season={season}&next=20"
    r=requests.get(url,headers=headers,timeout=30)
    data=r.json()
    rows=[]
    for m in data.get('response',[]):
        rows.append({
            'Date':m['fixture']['date'][:10],
            'Domicile':m['teams']['home']['name'],
            'Extérieur':m['teams']['away']['name']
        })
    if rows:
        st.dataframe(pd.DataFrame(rows),use_container_width=True)
    else:
        st.warning('Aucune donnée')

st.subheader('Module de prédiction (base)')
st.write('Over/Under, BTTS et Score exact à développer avec les statistiques avancées.')
