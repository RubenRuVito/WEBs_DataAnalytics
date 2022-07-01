import streamlit as st
import seaborn as sns
import plotly.graph_objects as plygo
#from matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def players_eda():
  st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
  st.write(st.session_state.df_players)
  
  st.line_chart(st.session_state.df_players['PTS'])
  
  #fig = plt.figure(figsize=(10, 4))
  st.write(sns.scatterplot(data=st.session_state.df_players, x=st.session_state.df_players['MP'], y=st.session_state.df_players['PTS'],
                           hue=st.session_state.df_players['Player']), legend=False)
  st.pyplot()
  
  #fig = pgo.Figure(data=pgo.Scatter(x=[1,2,3,4], y=[10,11,12,13], mode='markers', marker=dict(size=[40,60,80,100],
  #                                                                                             color=[1,2,3,4])))
  #st.plotly_chart(fig)
  
  mod_lr = LinearRegression(fit_intercept=True)
