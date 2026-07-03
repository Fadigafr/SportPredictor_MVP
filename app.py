import streamlit as st, sqlite3, hashlib, requests, pandas as pd
st.set_page_config(page_title="Sport Predictor Pro",layout="wide")
conn=sqlite3.connect("users.db",check_same_thread=False)
c=conn.cursor(); c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,email TEXT UNIQUE,password TEXT)"); conn.commit()
API_KEY=st.secrets.get("API_KEY","")
headers={"x-apisports-key":API_KEY}
def h(x): return hashlib.sha256(x.encode()).hexdigest()
if "user" not in st.session_state: st.session_state.user=None
menu=st.sidebar.selectbox("Menu",["Login","Inscription"] if not st.session_state.user else ["Dashboard","Statistiques équipes","Déconnexion"])
if menu=="Inscription":
 e=st.text_input('Email'); p=st.text_input('Mot de passe',type='password')
 if st.button('Créer compte'):
  c.execute('INSERT INTO users(email,password) VALUES(?,?)',(e,h(p))); conn.commit(); st.success('Compte créé')
elif menu=="Login":
 e=st.text_input('Email'); p=st.text_input('Mot de passe',type='password')
 if st.button('Connexion'):
  r=c.execute('SELECT * FROM users WHERE email=? AND password=?',(e,h(p))).fetchone()
  if r: st.session_state.user=e; st.rerun()
  else: st.error('Identifiants incorrects')
elif menu=="Déconnexion":
 st.session_state.user=None; st.rerun()
else:
 st.title('⚽ Sport Predictor Pro')
 if menu=="Dashboard":
  league=st.number_input('ID Ligue',39)
  season=st.number_input('Saison',2025)
  if st.button('Matchs à venir'):
   u=f'https://v3.football.api-sports.io/fixtures?league={league}&season={season}&next=20'
   d=requests.get(u,headers=headers,timeout=30).json()
   rows=[{'Date':m['fixture']['date'][:10],'Home':m['teams']['home']['name'],'Away':m['teams']['away']['name']} for m in d.get('response',[])]
   st.dataframe(pd.DataFrame(rows),use_container_width=True)
 if menu=="Statistiques équipes":
  team=st.number_input('ID Equipe',33)
  league=st.number_input('Ligue',39,key='l2')
  season=st.number_input('Saison ',2025,key='s2')
  if st.button('Charger statistiques'):
   u=f'https://v3.football.api-sports.io/teams/statistics?league={league}&season={season}&team={team}'
   d=requests.get(u,headers=headers,timeout=30).json().get('response',{})
   st.json(d)
