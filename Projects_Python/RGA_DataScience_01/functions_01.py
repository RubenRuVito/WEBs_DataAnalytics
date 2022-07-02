import streamlit as st
import seaborn as sns
import plotly.graph_objects as plygo
#from matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_option('deprecation.showPyplotGlobalUse', False) # Para que no visualice los Warning de Visualización de graficos..

def players_eda():
  st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
  st.write(st.session_state.df_players)
  
  st.line_chart(st.session_state.df_players['PTS'])
  
  #fig = plt.figure(figsize=(10, 4))
  st.write(sns.scatterplot(data=st.session_state.df_players, x=st.session_state.df_players['MP'], y=st.session_state.df_players['PTS'],
                           hue=st.session_state.df_players['Player'], legend=False))
  st.pyplot()
  
  fig = plygo.Figure(data=plygo.Scatter(x=st.session_state.df_players['MP'], y=st.session_state.df_players['PTS'], mode='markers', \
                                        marker_color=st.session_state.df_players['Player'].index, text=st.session_state.df_players['Player']))
  fig.update_layout(figsize=(14,8))
  st.plotly_chart(fig)
  
  mod_lr = LinearRegression(fit_intercept=True)
