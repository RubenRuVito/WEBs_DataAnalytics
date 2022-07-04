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
  # st.write(sns.scatterplot(data=st.session_state.df_players, x=st.session_state.df_players['MP'], y=st.session_state.df_players['PTS'],
  #                         hue=st.session_state.df_players['Player'], legend=False))
  # st.pyplot() # LO visualiza muy GRANDE, encontrar parametrización correcta..
  
  fig = plygo.Figure(data=plygo.Scatter(x=st.session_state.df_players['MP'], y=st.session_state.df_players['PTS'], mode='markers', \
                                        marker_color=st.session_state.df_players['Player'].index, text=st.session_state.df_players['Player']))
  fig.update_layout(width=1200, height=500, title='Relación Puntos y Minutos por Jugadores')
  fig.update_traces(textposition="bottom right") # Para poner el Parametro "text" fijo en la grafica
  fig.update_xaxes(title_text='MP - Minutos Jugados Totales (Temp.Regular)')
  fig.update_yaxes(title_text='PTS - Puntos Totales (Temp.Regular)')
  st.plotly_chart(fig)
  
  fig = plygo.Figure(data=plygo.Scatter(x=st.session_state.df_players['PTS'], y=st.session_state.df_players['PER'], mode='markers', \
                                        marker_color=st.session_state.df_players['Player'].index, text=st.session_state.df_players['Player']))
  fig.update_layout(width=1200, height=500, title='Relación Puntos y PER por Jugadores')
  fig.update_traces(textposition="bottom right") # Para poner el Parametro "text" fijo en la grafica
  fig.update_xaxes(title_text='PTS - Puntos Totales (Temp.Regular)')
  fig.update_yaxes(title_text='PER - Player Efficiency Rating (Temp.Regular)')
  st.plotly_chart(fig)
  
  mod_lr = LinearRegression(fit_intercept=True)
