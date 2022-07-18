import streamlit as st
import pandas as pd
import numpy as np
import os
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as plygo
import altair as alt # Para editar los graficos de streamlit
#from matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_option('deprecation.showPyplotGlobalUse', False) # Para que no visualice los Warning de Visualización de graficos..

def players_eda():
  st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
  st.write(st.session_state.df_players)
  
  st.line_chart(st.session_state.df_players['PTS'])
  
  st.write(type(st.session_state.df_players))
  st.write(st.session_state.df_players.loc[:,['Player','PTS']].sort_values(by=['PTS']))
  
  # Ordenando por PTS y reseteando el indice
  df_players = st.session_state.df_players.loc[:,['Player','PTS']].sort_values(by=['PTS'])
  df_players.reset_index(inplace=True)
  st.write(df_players)
  # Pinta el grafico ordenando por el nombre de jugador "Player", por muchas transformaciones que se hagan..
  plot_line_chart = alt.Chart(df_players).mark_line(interpolate='basis').encode(alt.X('Player', title='Players'), \
                                                                                alt.Y('PTS', title='Puntos (Temp.Regular)')). \
                                          properties(title='Puntos Juagadores Temporada Regular', width=1400, height=500)

  st.altair_chart(plot_line_chart) # use_container_width=True

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
  
def teams_eda():
  st.write(os.getcwd())
  df_games_full = pd.read_csv('Projects_Python/RGA_DataScience_01/data/df_games_qpoints_2021-22.csv', index_col=0)
  st.write(df_games_full)
  
  # Haciendo 2click en categoria de la leyenda, se aisla los datos de esa categoria..
  fig = px.line(df_games_full, x='GAME_DATE_EST', y='PTS', color='TEAM_NICKNAME')
  # https://plotly.com/python/figure-labels/
  fig.update_layout(width=1200, height=500, font=dict(size=15), title='Puntuaciones por partido Temp.Regular(2021-22)')
  st.plotly_chart(fig)
  
  st.write(print(df_games_full.info()))
  fig = px.line(df_games_full, x='GAME_ID', y='PTS', color='TEAM_NICKNAME')
  fig.update_layout(width=1200, height=500, font=dict(size=15), title='Puntuaciones por partido Temp.Regular(2021-22)')
  st.plotly_chart(fig)
  
  # Gráfica de Radar con 2 Equipos
  
  # Preparar 2 muestras(filas de datos con en PlayerName en el index del DF) xa incluir en el metodo de grafica..
  df_teams_radar = df_games_full.iloc[3:5,[3,7,8,9,10]]

  # df_teams_radar.columns
  # df_teams_radar.index.values
  # df_teams_radar.iloc[0].values # Retorna los valores de cada atributo/columna de la fila con indice "n"

  fig = pgo.Figure()

  for ind in range(len(df_teams_radar.index.values)):
      print(ind)
      fig.add_trace(pgo.Scatterpolar(r=df_teams_radar.iloc[ind].values,
                                      theta=df_teams_radar.columns,
                                      fill='toself',
                                      #name="TypeWine-%s"%datasets.load_wine().target_names[ind],
                                      name="Team-%s"%df_teams_radar.index[ind], # Recupera los rownames del dataframe..
                                      showlegend=True,)
                                      )

  fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 40])),
                               title="Promedio Puntos por Cuartos y OT")
  st.plotly_chart(fig)
  
  # NUevo objet DF agrupado por equipos y utilizar el método de agregación del promedio o media de puntos en cada quarto y OT
  df_games_full_01 = df_games_full.loc[:,['TEAM_ABBREVIATION','PTS_QTR1','PTS_QTR2','PTS_QTR3','PTS_QTR4','PTS_OT1','PTS_OT2','PTS_OT3','PTS']]. \
                                  groupby('TEAM_ABBREVIATION').mean()
  
  st.write(df_games_full_01)
  
  fig = px.line(df_games_full_01)
  # https://plotly.com/python/figure-labels/
  fig.update_layout(width=1200, height=500, font=dict(size=15), title='Promedio de puntuaciones por partido, por cuartos y OT')
  st.plotly_chart(fig)
  
  fig = px.bar(df_games_full_01.iloc[:,0:4])
  fig.update_layout(width=1200, height=500, font=dict(size=19),
                  title='Promedio Puntos por Cuarto de cada Team en Temp.Regular(2021-2022)')
  st.plotly_chart(fig)
  
  fig = px.bar(df_games_full_01.iloc[:,7])
  fig.update_layout(width=1200, height=500, font=dict(size=19),
                  title='Promedio Puntos por Cuarto de cada Team en Temp.Regular(2021-2022)')
  st.plotly_chart(fig)
  
  
