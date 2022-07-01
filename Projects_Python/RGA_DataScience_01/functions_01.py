import streamlit as st
from sklearn.linear_model import LinnearRegression

def players_eda():
  st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
  st.write(st.session_state.df_players)
  
  st.line_chart(st.session_state.df_players['PTS'])
  
  mod_lr = LinnearReggresion(fit_intercept=True)
