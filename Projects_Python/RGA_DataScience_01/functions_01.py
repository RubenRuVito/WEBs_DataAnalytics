import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image
import urllib.request as urlreq
import os
import base64
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as plygo
import altair as alt # Para editar los graficos de streamlit
#from matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from nba_api.stats import endpoints
from nba_api.stats.static import players
from nba_api.stats.static import teams

st.set_option('deprecation.showPyplotGlobalUse', False) # Para que no visualice los Warning de Visualización de graficos..

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

def add_logo2(logo_path, width, height):
    """Read and return a resized logo"""
    urlreq.urlretrieve(logo_path, "logo_team.png")
    # svg_code = open("logo_svg.svg", 'rt').read()
    # svg2png(bytestring=svg_code, write_to="logo_svg.png")
    logo = Image.open("logo_team.png")
    modified_logo = logo.resize((width, height))
    return modified_logo

def add_logo3(logo_path, width, height):
    """Read and return a resized logo"""
    urlreq.urlretrieve(logo_path, "player_image.png")
    # svg_code = open("logo_svg.svg", 'rt').read()
    # svg2png(bytestring=svg_code, write_to="logo_svg.png")
    logo = Image.open("player_image.png")
    modified_logo = logo.resize((width, height))
    return modified_logo


# Función de github, para scrapear las tablas de estadisticas de Players de "basketball_reference.com"
# Streamlit NBA Analyzer..
# https://github.com/tta13/NBA-Stats-Explorer
# https://github.com/tta13/NBA-Stats-Explorer/blob/main/nbanalyzer/basketball_reference_api.py
def get_players_stats(season: str, stat_type: str, header: int = 0, filter_games=True, remove_duplicates=True):

    BASE_URL = 'https://www.basketball-reference.com/'
    STAT_TYPES = ['per_game', 'totals', 'per_minute', 'advanced', 'per_poss', 'play-by-play', 'advanced_box_score']
    ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']
    
    season = "20" + season.split("-")[1]

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
    
    # Se filtran los jugadores con un minimo de partidos jugados.."Un minimo de maxGameplay dividido 2 'G' "..
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

def players_stats():

    time.sleep(1)
    data_players = endpoints.leaguedashplayerstats.LeagueDashPlayerStats(season=st.session_state.temporada, timeout=40).get_data_frames()
    df_players = pd.DataFrame(data_players[0])

    # st.markdown(f"ESTADISTICAS POR JUGADORES - Temporada Regular ({st.session_state.temporada}).")
    if st.checkbox("Ver Tabla de Datos:"):
            st.dataframe(df_players)
    
    # st.write(df_players)

    players = df_players.PLAYER_NAME.tolist()
    # team_abbrev = df_players.TEAM_ABBREVIATION.tolist()
    player_select = st.sidebar.selectbox("Player", players)

    # df_players.PLAYER_NAME
    # df_players.W_PCT.tolist()

    if player_select:

        st.text(int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values))
        # player_img = add_logo3(logo_path="https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png", width=150, height=160)
        player_img = add_logo3(logo_path=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values)}.png", width=150, height=160)
        # st.sidebar.image(player_img)

        col1, col2, col3 = st.sidebar.columns([1,3,1])
        with col1:
            st.write("")
        with col2:
            st.image(player_img)
        with col3:
            st.write("")
        
        st.markdown(f"<h2 style='text-align: left; color: white; font-family:commanders'>{player_select} STATS (KPIs) -\
            {df_players[df_players.PLAYER_NAME == player_select].TEAM_ABBREVIATION.values}</h2>", unsafe_allow_html=True)

        df_player_bio = endpoints.leaguedashplayerbiostats.LeagueDashPlayerBioStats().get_data_frames()[0]
        
        if st.checkbox("Ver Tabla de Datos2:"):
            st.dataframe(df_player_bio)
        
        m1, m2, m3, m4, m5, m6 = st.columns((1,1,1,1,1,1))

        m1.metric("Edad:", df_player_bio[df_player_bio.PLAYER_NAME == player_select].AGE.values)
        m2.metric("Estatura:", int(df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_HEIGHT.values))
        m3.metric("Embergadura:", df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_HEIGHT_INCHES.values)
        m4.metric("Peso:", df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_WEIGHT.values)
        m5.metric("Universidad:", df_player_bio[df_player_bio.PLAYER_NAME == player_select].COLLEGE.values)
        m6.metric("Año Draft:", df_player_bio[df_player_bio.PLAYER_NAME == player_select].DRAFT_YEAR.values)

        st.text("--------------------------------------")

        m1, m2, m3, m4, m5, m6 = st.columns((1,1,1,1,1,1))
    
        # m1.metric(label='PTS', value=df_teams[df_teams.TEAM_NAME == team_select].PTS.values)
        m1.metric("PTS", df_players[df_players.PLAYER_NAME == player_select].PTS.values, int(df_players[df_players.PLAYER_NAME == player_select].PTS.values)-int((df_players.PTS.mean())))
        
        m2.metric("Wins",str(int(df_players[df_players.PLAYER_NAME == player_select].W.values))+" Victorias", int(df_players[df_players.PLAYER_NAME == player_select].W.values)-int((df_players.W.mean())))
        
        m3.metric("Lost", str(int(df_players[df_players.PLAYER_NAME == player_select].L.values))+" Derrotas", int(df_players[df_players.PLAYER_NAME == player_select].L.values)-int((df_players.L.mean())))
        
        m4.metric('WL_PCT', str(float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)), float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)-float((df_players.W_PCT.mean())))
        
        m5.metric('FG_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values)-float((df_players.FG_PCT.mean())))
        
        m6.metric('FG3_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values)-float((df_players.FG3_PCT.mean())))

        st.text("--------------------------------------")

        c1,c2,c3 = st.columns([1,4,1]) # Entre corchetes se define que tamaño en ancho tendrá la columna, con 
                                       # respecto a las demás..
        
        with c1:
            # m1, m2, m3, m4, m5, m6 = st.columns()
    
            # m1.metric(label='PTS', value=df_teams[df_teams.TEAM_NAME == team_select].PTS.values)
            st.metric(f"PTS [Media->{int(df_players.PTS.mean())}]", df_players[df_players.PLAYER_NAME == player_select].PTS.values, int(df_players[df_players.PLAYER_NAME == player_select].PTS.values)-int((df_players.PTS.mean())))
            
            st.metric("Wins",str(int(df_players[df_players.PLAYER_NAME == player_select].W.values))+" Victorias", int(df_players[df_players.PLAYER_NAME == player_select].W.values)-int((df_players.W.mean())))
            
            st.metric("Lost", str(int(df_players[df_players.PLAYER_NAME == player_select].L.values))+" Derrotas", int(df_players[df_players.PLAYER_NAME == player_select].L.values)-int((df_players.L.mean())))

        with c2:
            # st.write(int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values))
            # df_player_stsyears = endpoints.PlayerGameLogs(player_id_nullable=int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values), season_nullable=st.session_state.temporada).get_data_frames()[0]
            df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=str(int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values))).get_data_frames()[1]
            
            if st.checkbox("Ver Tabla de Datos del Jugador."):
                st.dataframe(df_player_stsyears)

            # Preparamos los datos para el input del tipo de gráficas "Altair"..
            # ***Los jugadores que juegan en 2 o más equipos en una tempo (valor = "TOT"),
            # - Se filtra la fila con el valor "TOT", xa no contabilizarla y en función de las metricas se SUM(), o MEAN()
            # - Para estas graficas de métricas de cantidad en acciones defensivas u ofensivas, se utiliza el Sumarizar
            # para la temporada que el jugador ha jugado en 2 o más equipo (Debido a un traspaso..evidentemente)
            
            # Métricas Ofensivas.
            df_psy = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','FGM','FG3M','FTM','OREB','AST','PTS']].set_index('GROUP_VALUE')
            df_psy = df_psy.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
            df_psy_plot_altair = df_psy.reset_index().melt(df_psy.index.names, var_name='Offensive Measure', value_name='y')
            
            # st.dataframe(df_psy_plot_altair)

            plot_line_chart = alt.Chart(df_psy_plot_altair) \
                      .mark_line().encode(alt.X('GROUP_VALUE', title='Temporada'), \
                      alt.Y('y', title='Count'), color='Offensive Measure:N', \
                      tooltip=[alt.Tooltip("GROUP_VALUE", title='Temporada'),"Offensive Measure", \
                      alt.Tooltip("y", title='Count')]).properties( \
                        title='Métricas Ofensivas por Temporadas.').interactive()

            st.altair_chart(plot_line_chart, use_container_width=True)

            # Métricas Defensivas.
            df_psy = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']].set_index('GROUP_VALUE')
            df_psy = df_psy.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
            df_psy_plot_altair = df_psy.reset_index().melt(df_psy.index.names, var_name='Defensive Measure', value_name='y')
            
            # st.dataframe(df_psy_plot_altair)

            plot_line_chart = alt.Chart(df_psy_plot_altair) \
                      .mark_line().encode(alt.X('GROUP_VALUE', title='Temporada'), \
                      alt.Y('y', title='Count'), color='Defensive Measure:N', \
                      tooltip=[alt.Tooltip("GROUP_VALUE", title='Temporada'),"Defensive Measure", \
                      alt.Tooltip("y", title='Count')]).properties( \
                        title='Métricas Defensivas por Temporadas.').interactive()

            st.altair_chart(plot_line_chart, use_container_width=True)

            # Probando Gráficas..
            # st.dataframe(df_psy.reset_index())

            # fig = px.line(df_psy.loc[:,['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']], x=df_psy.index, y=df_psy.loc[:,['DREB','TOV','STL','BLK','PLUS_MINUS']].columns.values,
            fig = px.line(df_psy.reset_index(), x=df_psy.reset_index().index, y=df_psy.columns.values, \
              title='Métricas Defensivas por Temporadas.', template='plotly_dark')
            fig.update_layout(width=1000, height=400, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
                    tickmode = 'array',
                    tickvals = df_psy.reset_index().index,
                    ticktext = df_psy.reset_index()['GROUP_VALUE']), \
                yaxis_title = "Count", \
                legend_title = "Defensive Measure")
            fig.update_traces(line=dict(width=3)) # Grosor de la linea
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with c3:  
            st.metric('WL_PCT', str(float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)), float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)-float((df_players.W_PCT.mean())))
            
            st.metric('FG_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values)-float((df_players.FG_PCT.mean())))
            
            st.metric('FG3_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values)-float((df_players.FG3_PCT.mean())))

def players_stats_compare():
    st.markdown(f"ESTADISTICAS POR JUGADORES - Temporada Regular ({st.session_state.temporada}).")

    # DATA (Scrapping con funciones que raspan de "basketball-reference.com")
    # Recuperando los datos de players "totals","Advanced" para la temporada actual, y unir la col "PER" a tabla "totals"
    # if 'df_players' not in st.session_state:
    #     BASE_URL = 'https://www.basketball-reference.com/'
    #     STAT_TYPES = ['per_game', 'totals', 'per_minute', 'advanced', 'per_poss', 'play-by-play', 'advanced_box_score']
    #     ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']
        
    #     df_players_totals = get_players_stats(st.session_state.temporada,'totals')
    #     df_players_advanced = get_players_stats(st.session_state.temporada,'advanced')
        
    #     df_players = pd.concat([df_players_totals, df_players_advanced['PER']], axis=1)
    #     st.session_state.df_players = df_players

    df_players_totals = get_players_stats(st.session_state.temporada,'totals')
    df_players_advanced = get_players_stats(st.session_state.temporada,'advanced')
        
    df_players = pd.concat([df_players_totals, df_players_advanced['PER']], axis=1)
    st.session_state.df_players = df_players

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
  
def teams_stats_compare():
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
  
  
