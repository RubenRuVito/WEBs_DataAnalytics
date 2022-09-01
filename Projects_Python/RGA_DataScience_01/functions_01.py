import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as plygo
import altair as alt # Para editar los graficos de streamlit
#from matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_option('deprecation.showPyplotGlobalUse', False) # Para que no visualice los Warning de Visualización de graficos..

# Función de github, para scrapear las tablas de estadisticas de Players de "basketball_reference.com"
# https://github.com/tta13/NBA-Stats-Explorer/blob/main/nbanalyzer/basketball_reference_api.py
def get_players_stats(season: int, stat_type: str, header: int = 0, filter_games=True, remove_duplicates=True):
  
    BASE_URL = 'https://www.basketball-reference.com/'
    STAT_TYPES = ['per_game', 'totals', 'per_minute', 'advanced', 'per_poss', 'play-by-play', 'advanced_box_score']
    ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']
    
    url = f'{BASE_URL}leagues/NBA_{str(season)}_{stat_type}.html'
    print(f'GET {url}')
    st.text(url)
    html = pd.read_html(url, header = 0)
    df = html[0]

    raw = None
    if 'Age' in df:
        raw = df.drop(df[df.Age == 'Age'].index)
        raw = raw.fillna(0)
    
    player_stats = raw.drop(['Rk'], axis=1) if raw is not None else df.drop(['Rk'])

    cols=[i for i in player_stats.columns if i not in ['Player','Pos', 'Tm']]
    for col in cols:
        try:
            player_stats[col]=pd.to_numeric(player_stats[col])
        except ValueError:
            player_stats[col]=player_stats[col]
    
    # Se filtran los jugadores con un minimo de partidos jugados..
    if filter_games:
        max_games_played = player_stats['G'].max()
        threshold = max_games_played // 2   
        player_stats = player_stats[player_stats['G'] >= threshold]

    if remove_duplicates:
        player_stats.drop_duplicates(subset=['Player'], inplace=True)
        player_stats['Pos'].replace(['SG-PG','SG-SF','SG-PF','SG-C'], 'SG', inplace=True)        
        player_stats['Pos'].replace(['PG-SG','PG-SF','PG-PF','PG-C'], 'PG', inplace=True)
        player_stats['Pos'].replace(['SF-PG','SF-SG','SF-PF','SF-C'], 'SF', inplace=True)
        player_stats['Pos'].replace(['PF-PG','PF-SF','PF-SF','PF-C'], 'PF', inplace=True)
        player_stats['Pos'].replace(['C-PG','C-SF','C-PF','C-SG'], 'C', inplace=True)        
        
    return player_stats

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
  st.write(df_games_full.info())
  st.write(type(df_games_full.GAME_ID))
  fig = px.line(df_games_full, x='GAME_ID', y='PTS', color='TEAM_NICKNAME')
  fig.update_layout(width=1200, height=500, font=dict(size=15), title='Puntuaciones por partido Temp.Regular(2021-22)')
  st.plotly_chart(fig)
  
  # Gráfica de Radar con 2 Equipos
  
  # Preparar 2 muestras de los Games, xa incluir en el metodo de grafica..
  # Muestra las puntuaciones por cuarto para ese partido
  # df_teams_radar = df_games_full.iloc[df_games_full.GAME_ID == 22100001, [4,8,9,10,11]] # filas en posición 3 y 4 y columnas "8..11"
  # df_teams_radar = df_games_full.iloc[0:2, [4,8,9,10,11]]
  
  # df_teams_radar.columns
  # df_teams_radar.index.values
  # df_teams_radar.iloc[0].values # Retorna los valores de cada atributo/columna de la fila con indice "n"

  #fig = plygo.Figure()

  #for ind in range(len(df_teams_radar.index.values)):
  #    print(ind)
  #    fig.add_trace(plygo.Scatterpolar(r=df_teams_radar.iloc[ind].values,
  #                                    theta=df_teams_radar.iloc[:,[8,9,10,11].columns,
  #                                    fill='toself',
  #                                    #name="TypeWine-%s"%datasets.load_wine().target_names[ind],
  #                                    name="Team-%s"%df_teams_radar.index[ind].iloc[:,4], # Recupera los rownames del dataframe..
  #                                    showlegend=True,)
  #                                    )

  #fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 40])),
  #                             title="Promedio Puntos por Cuartos y OT")
  #st.plotly_chart(fig)
  
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
  
  fig = px.bar(df_games_full_01.iloc[:,7].sort_values(ascending=False))
  fig.update_layout(width=1200, height=500, font=dict(size=19),
                  title='Promedio Puntos por Cuarto de cada Team en Temp.Regular(2021-2022)')
  st.plotly_chart(fig)
  
  # Grafica de Barras en Horizontal y ordenado de mayor a menor suma total de puntos por cuarto(seria la media de puntos x partido de cada team)
  # Ojo a los textos de cada eje, xq si se solapan no se pintan..
  fig = px.bar(df_games_full_01.iloc[:,0:4], orientation='h')
  fig.update_layout(width=1100, height=800, font=dict(size=15),
                  title='Promedio Puntos por Cuarto de cada Team en Temp.Regular(2021-2022)')
  fig.update_yaxes(categoryorder='total ascending')
  st.plotly_chart(fig)
  
  # Gráfica de Radar con el DF agrupado por Team para obtener los promedios de cada uno de los Teams
  df_teams_radar = df_games_full_01.iloc[3:5,[0,1,2,3]] # filas en posición 3 y 4

  # df_teams_radar.columns
  # df_teams_radar.index.values
  # df_teams_radar.iloc[0].values # Retorna los valores de cada atributo/columna de la fila con indice "n"

  fig = plygo.Figure()

  for ind in range(len(df_teams_radar.index.values)):
      print(ind)
      fig.add_trace(plygo.Scatterpolar(r=df_teams_radar.iloc[ind].values,
                                      theta=df_teams_radar.columns,
                                      fill='toself',
                                      #name="TypeWine-%s"%datasets.load_wine().target_names[ind],
                                      name="Team-%s"%df_teams_radar.index[ind], # Recupera los rownames del dataframe..
                                      showlegend=True,)
                                      )

  fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 40])),
                               title="Promedio Puntos por Cuartos y OT")
  st.plotly_chart(fig)
  
  
