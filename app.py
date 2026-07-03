import streamlit as st, requests, pandas as pd, sqlite3, hashlib
import streamlit as st, pandas as pd, numpy as np
st.set_page_config(page_title="Sport Predictor V3",layout="wide")
st.title("⚽ Sport Predictor V3")

st.sidebar.header("Accès")
st.sidebar.info("Admin: admin@gmail.com / admin123")

page=st.sidebar.selectbox("Module",["Prédictions","xG","Accès"])

if page=="Prédictions":
    hg=st.number_input("Moy. buts domicile",0.0,10.0,1.8)
    ag=st.number_input("Moy. buts extérieur",0.0,10.0,1.2)
    total=hg+ag
    over15=min(round((total/1.5)*50,1),99)
    over25=min(round((total/2.5)*50,1),99)
    over35=min(round((total/3.5)*50,1),99)
    st.metric("Over 1.5 %",over15)
    st.metric("Over 2.5 %",over25)
    st.metric("Over 3.5 %",over35)
    st.success(f"BTTS estimé : {min(round((hg*ag)*25,1),95)}%")

if page=="xG":
    tirs=st.number_input("Tirs",0,50,12)
    cadrés=st.number_input("Tirs cadrés",0,30,5)
    xg=round((tirs*0.08)+(cadrés*0.12),2)
    st.metric("xG estimé",xg)
    st.write("Version simple. Peut être remplacée par les données xG réelles API-Football selon votre abonnement.")

if page=="Accès":
    st.code('Email : admin@gmail.com
Mot de passe : admin123')

st.set_page_config(layout="wide")
API_KEY=st.secrets.get("API_KEY","")
H={"x-apisports-key":API_KEY}
conn=sqlite3.connect("users.db",check_same_thread=False)
c=conn.cursor(); c.execute("CREATE TABLE IF NOT EXISTS users(email text unique,password text)"); conn.commit()
def h(x): return hashlib.sha256(x.encode()).hexdigest()
if 'user' not in st.session_state: st.session_state.user=None
if not st.session_state.user:
 m=st.sidebar.radio('Accès',['Login','Inscription'])
 e=st.text_input('Email'); p=st.text_input('Mot de passe',type='password')
 if m=='Inscription' and st.button('Créer'):
  c.execute('INSERT OR IGNORE INTO users VALUES(?,?)',(e,h(p))); conn.commit(); st.success('Compte créé')
 if m=='Login' and st.button('Connexion'):
  r=c.execute('SELECT * FROM users WHERE email=? AND password=?',(e,h(p))).fetchone()
  if r: st.session_state.user=e; st.rerun()
else:
 st.sidebar.success(st.session_state.user)
 page=st.sidebar.selectbox('Menu',['Matchs','Over/Under','Buteurs probables'])
 if page=='Matchs':
  lg=st.number_input('Ligue',39)
  ss=st.number_input('Saison',2025)
  if st.button('Charger'):
   d=requests.get(f'https://v3.football.api-sports.io/fixtures?league={lg}&season={ss}&next=20',headers=H).json()
   rows=[{'Date':x['fixture']['date'][:16],'Domicile':x['teams']['home']['name'],'Extérieur':x['teams']['away']['name'],'FixtureId':x['fixture']['id']} for x in d.get('response',[])]
   st.dataframe(pd.DataFrame(rows),use_container_width=True)
 if page=='Over/Under':
  fid=st.number_input('Fixture ID',value=0)
  if st.button('Voir cotes') and fid:
   r=requests.get(f'https://v3.football.api-sports.io/odds?fixture={int(fid)}',headers=H).json()
   st.json(r)
   st.info('Cherchez dans la réponse les marchés Over/Under 1.5, 2.5, 3.5 selon le bookmaker disponible.')
 if page=='Buteurs probables':
  team=st.number_input('ID Equipe',33)
  league=st.number_input('Ligue ',39)
  season=st.number_input('Saison ',2025)
  if st.button('Analyser joueurs'):
   r=requests.get(f'https://v3.football.api-sports.io/players?team={int(team)}&league={int(league)}&season={int(season)}',headers=H).json()
   rows=[]
   for p in r.get('response',[]):
     name=p['player']['name']
     stats=p['statistics'][0]
     goals=stats.get('goals',{}).get('total') or 0
     games=stats.get('games',{}).get('appearences') or 1
     score=round((goals/max(games,1))*100,2)
     rows.append([name,goals,games,score])
   df=pd.DataFrame(rows,columns=['Joueur','Buts','Matchs','Indice buteur'])
   df=df.sort_values('Indice buteur',ascending=False).head(10)
   st.dataframe(df,use_container_width=True)
   st.success('Les joueurs avec le meilleur indice sont les buteurs probables.')
