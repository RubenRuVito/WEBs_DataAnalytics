import streamlit as st

def players_eda():
  st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
  st.write(st.session_state.df_players)
  
  mod_lr = linear_model.LinnearReggresion(fit_intercept=True)
