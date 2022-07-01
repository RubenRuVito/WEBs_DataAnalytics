import streamlit as st
import seaborn as sns
from sklearn.linear_model import LinearRegression

def players_eda():
  st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
  st.write(st.session_state.df_players)
  
  st.line_chart(st.session_state.df_players['PTS'])
  
  fig, ax = plt.subplots()
  sns.scatterplot(data=st.session_state.df_players, x=st.session_state.df_players['MP'], y=st.session_state.df_players['PTS'],
                  hue=st.session_state.df_players['Player'], ax=ax)
  st.pyplot(fig)
  
  mod_lr = LinearReggresion(fit_intercept=True)
