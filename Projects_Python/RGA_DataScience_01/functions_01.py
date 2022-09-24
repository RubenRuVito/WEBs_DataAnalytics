import streamlit as st
import pandas as pd
import numpy as np
import re
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

    df_players_stats = pd.DataFrame(endpoints.LeagueDashPlayerStats(season=st.session_state.temporada).get_data_frames()[0])
    players_names = df_players_stats.PLAYER_NAME.tolist()
    # team_abbrev = df_players.TEAM_ABBREVIATION.tolist()
    players_names.sort()
    player_select = st.sidebar.selectbox("Player", players_names)

    # st.markdown(f"ESTADISTICAS POR JUGADORES - Temporada Regular ({st.session_state.temporada}).")

    if player_select:

        id_player = int(df_players_stats[df_players_stats.PLAYER_NAME == player_select].PLAYER_ID.values)
        # st.text(int(df_players_stats[df_players_stats.PLAYER_NAME == player_select].PLAYER_ID.values))

        df_player_info = endpoints.CommonPlayerInfo(player_id=id_player).get_data_frames()[0]
        
        # player_img = add_logo3(logo_path="https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png", width=150, height=160)
        player_img = add_logo3(logo_path=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{int(df_players_stats[df_players_stats.PLAYER_NAME == player_select].PLAYER_ID.values)}.png", width=150, height=160)
        # st.sidebar.image(player_img)

        col1, col2, col3 = st.sidebar.columns([1,3,1])
        with col1:
            st.write("")
        with col2:
            st.image(player_img)
        with col3:
            st.write("")
        
        c1, c2, c3 = st.columns([1.4,1.2,1])

        with c1:
            st.markdown(f"<h1 style='text-align: left; color: ; font-family:commanders'>&#9679 {player_select}</h1>",unsafe_allow_html=True) # - \
                # Conferencia {df_team_info._get_value(0,'TEAM_CONFERENCE').upper() + ' [Rank ' + str(df_team_info._get_value(0,'CONF_RANK')) + 'º]'} - \
                # División {df_team_info._get_value(0,'TEAM_DIVISION').upper() + ' [Rank ' + str(df_team_info._get_value(0,'DIV_RANK')) + 'º]'}</h2>",unsafe_allow_html=True)

            # data_teams = endpoints.LeagueDashTeamStats(season=st.session_state.temporada).get_data_frames()
            # df_teams = pd.DataFrame(data_teams[0])
            type_stats = st.radio("",("Totales","Por Game", "Por 100 Posesiones", "Por 36 Minutos"), horizontal=True)
        # if type_stats == "Totales":
            # df_players_stats = pd.DataFrame(endpoints.LeagueDashPlayerStats(season=st.session_state.temporada).get_data_frames()[0])
        if type_stats == "Por Game":
            df_players_stats = pd.DataFrame(endpoints.LeagueDashPlayerStats(season=st.session_state.temporada, per_mode_detailed="PerGame").get_data_frames()[0])
        if type_stats == "Por 100 Posesiones":
            df_players_stats = pd.DataFrame(endpoints.LeagueDashPlayerStats(season=st.session_state.temporada, per_mode_detailed="Per100Possessions").get_data_frames()[0])
        if type_stats == "Por 36 Minutos":
            df_players_stats = pd.DataFrame(endpoints.LeagueDashPlayerStats(season=st.session_state.temporada, per_mode_detailed="Per36").get_data_frames()[0])

        with c2:
            # st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>{team_select.upper()}</h2>",unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 \
                {df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'TEAM_CITY') + ' ' + df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'TEAM_NAME')}</h2>",unsafe_allow_html=True)
            st.write(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 \
                #{df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'JERSEY') + ' &nbsp;&nbsp;&#9658 ' + df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'POSITION')}</h2>",unsafe_allow_html=True)
            # st.write(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 {df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'POSITION')}</h2>",unsafe_allow_html=True)
        
        with c3:
            st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 \
                {df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'LAST_AFFILIATION')}</h2>",unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 \
                {df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'COUNTRY')}</h2>",unsafe_allow_html=True)

        if st.checkbox("Ver Tabla de Datos de Jugadores."):
            st.write(df_players_stats)

        df_player_bio = endpoints.LeagueDashPlayerBioStats(season=st.session_state.temporada).get_data_frames()[0]

        # st.write(int(id_player))
        # st.write(type(id_player),"-",len(id_player))
        # st.write(type(df_player_bio.PLAYER_ID),"-",len(df_player_bio.PLAYER_ID))

        # Instrucciones para tranformar el valor de la estatura de "['6-10']" a "6' Pies 10'' Pulgadas"...
        # Y tb obtener la medida en mtros y centimetros..
        estatura = str(df_player_bio.loc[df_player_bio.PLAYER_ID == id_player, "PLAYER_HEIGHT"].values)
        # st.text(estatura)
        # st.text([int(s) for s in re.findall(r'-?\d+\.?\d*', estatura)][0])
        # st.text([int(s) for s in re.findall(r'-?\d+\.?\d*', estatura)][1]*-1)

        pies = [int(s) for s in re.findall(r'-?\d+\.?\d*', estatura)][0]
        pulgadas = [int(s) for s in re.findall(r'-?\d+\.?\d*', estatura)][1] * -1

        estatura = str(pies) + "'" + str(pulgadas) + "''"
        estatura2 = (pies * 30.48) + (pulgadas * 2.54)
        # st.text(estatura)
        # st.text(83*2.54)
        # st.text(int(df_player_bio[df_player_bio.PLAYER_ID == id_player].PLAYER_WEIGHT.values))

        m1, m2, m3 = st.sidebar.columns((1,1,1))

        m1.write(f'<h3>Edad: </h3>{str(int(df_player_bio.loc[df_player_bio.PLAYER_ID == id_player, "AGE"].values))}', unsafe_allow_html=True)
        # m2.write(f'<h3>Estatura: </h3>{str(df_player_bio.loc[df_player_bio.PLAYER_ID == id_player, "PLAYER_HEIGHT"].values), estatura, estatura2}', unsafe_allow_html=True)
        m2.write(f'<h3>Estatura: </h3>{estatura} - {round(estatura2, 2)} cm', unsafe_allow_html=True)
        m3.write(f'<h3>Envergadura: </h3>{round(int(df_player_bio[df_player_bio.PLAYER_ID == id_player].PLAYER_HEIGHT_INCHES.values) * 2.54,2)} cm', unsafe_allow_html=True)
        
        m4, m5, m6 = st.sidebar.columns((1,1,1))

        m4.write(f'<h3>Peso: </h3>{round(int(df_player_bio[df_player_bio.PLAYER_ID == id_player].PLAYER_WEIGHT.values) * 0.45359237,2)} kg', unsafe_allow_html=True)
        m5.write(f'<h3>Universidad: </h3>{df_player_bio[df_player_bio.PLAYER_ID == id_player].COLLEGE.values}', unsafe_allow_html=True)
        m6.write(f'<h3>Año Draft: </h3>{df_player_bio[df_player_bio.PLAYER_ID == id_player].DRAFT_YEAR.values}', unsafe_allow_html=True)

        st.text("------------------------------------------------------------------")

        df_players_stats_adv = endpoints.LeagueDashPlayerStats(season=st.session_state.temporada, measure_type_detailed_defense="Advanced").get_data_frames()[0]

        m1, m11, m12, m13, m2, m3, m31, m32, m33, m5, m6, m7 = st.columns((1.2,1.2,1,1,0.5,0.5,1,1,1,1,1,1))
    
        m1.metric("PTS", "{:,}".format(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].PTS.values),2)), \
            "{:,}".format(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].PTS.values)-float(df_players_stats.PTS.mean()),2)))
            
        # format(int(df_team_details._get_value(0, 'ARENACAPACITY')), ',d')
        m11.metric("MINUTS", "{:,}".format(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].MIN.values),2)), \
            "{:,}".format(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].MIN.values)-float(df_players_stats.MIN.mean()),2)))

        m12.metric("+ / -", "{:,}".format(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].PLUS_MINUS.values),2)), \
            "{:,}".format(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].PLUS_MINUS.values)-int(df_players_stats.PLUS_MINUS.mean()),2)))
        
        m13.metric("NET_RATING", "{:,}".format(round(float(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].NET_RATING.values),2)), \
            "{:,}".format(round(float(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].NET_RATING.values)-int(df_players_stats_adv.NET_RATING.mean()),2)))

        m2.metric("WINS",str(int(df_players_stats[df_players_stats.PLAYER_ID == id_player].W.values)), \
            int(df_players_stats[df_players_stats.PLAYER_ID == id_player].W.values)-int(df_players_stats.W.mean()))
            
        m3.metric("LOST", str(int(df_players_stats[df_players_stats.PLAYER_ID == id_player].L.values)), \
            int(df_players_stats[df_players_stats.PLAYER_ID == id_player].L.values)-int(df_players_stats.L.mean()))

        m31.metric('WL_PCT', str(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].W_PCT.values * 100),2))+'%', \
            str(round((float(df_players_stats[df_players_stats.PLAYER_ID == id_player].W_PCT.values)-float(df_players_stats.W_PCT.mean())) * 100,2))+'%')

        m32.metric("EFG_PCT(F)", str(round(float(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].EFG_PCT.values *100),2))+'%', \
            str(round((float(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].EFG_PCT.values)-float(df_players_stats_adv.EFG_PCT.mean())) *100,2))+'%')
        
        m33.metric("PIE(F)", str(round(float(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].PIE.values *100),2))+'%', \
            str(round((float(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].PIE.values)-float(df_players_stats_adv.PIE.mean())) *100,2))+'%')
        
        m5.metric('FG_PCT', str(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG_PCT.values * 100),2))+'%', \
            str(round((float(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG_PCT.values)-float(df_players_stats.FG_PCT.mean())) * 100,2))+'%')
        
        m6.metric('FG3_PCT', str(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG3_PCT.values * 100),2))+'%', \
            str(round((float(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG3_PCT.values)-float(df_players_stats.FG3_PCT.mean())) * 100,2))+'%')

        m7.metric('FT_PCT', str(round(float(df_players_stats[df_players_stats.PLAYER_ID == id_player].FT_PCT.values * 100),2))+'%', \
            str(round((float(df_players_stats[df_players_stats.PLAYER_ID == id_player].FT_PCT.values)-float(df_players_stats.FT_PCT.mean())) * 100,2))+'%')

        st.text("------------------------------------------------------------------")

        c1,c2,c3 = st.columns([0.5,4,0.5]) # Entre corchetes se define que tamaño en ancho tendrá la columna, con 
                                       # respecto a las demás..
        
        with c1:
            st.write("<h3> ATAQUE. </h3>", unsafe_allow_html=True)
            st.metric("OFF_RATING", df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].OFF_RATING.values, int(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].OFF_RATING.values)-int((df_players_stats_adv.OFF_RATING.mean())))
            st.metric("FG_Made", df_players_stats[df_players_stats.PLAYER_ID == id_player].FGM.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].FGM.values)-int((df_players_stats.FGM.mean())))
            st.metric("FG3_Convertidos", df_players_stats[df_players_stats.PLAYER_ID == id_player].FG3M.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG3M.values)-int((df_players_stats.FG3M.mean())))
            # st.metric("FG3_Convertidos 02", int(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG3M.values) / int(df_players_stats[df_players_stats.PLAYER_ID == id_player].GP.values), int(df_players_stats[df_players_stats.PLAYER_ID == id_player].FG3M.values)-int((df_players_stats.FG3M.mean())))
            st.metric("FT_Made", df_players_stats[df_players_stats.PLAYER_ID == id_player].FTM.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].FTM.values)-int((df_players_stats.FTM.mean())))
            st.metric("Rebotes", df_players_stats[df_players_stats.PLAYER_ID == id_player].OREB.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].OREB.values)-int((df_players_stats.OREB.mean())))
            st.metric("Asistencias", df_players_stats[df_players_stats.PLAYER_ID == id_player].AST.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].AST.values)-int((df_players_stats.AST.mean())))
            

            # st.write("<h3> DEFENSA. </h3>", unsafe_allow_html=True)
            # st.metric("Rebotes", df_players_stats[df_players_stats.PLAYER_ID == id_player].DREB.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].DREB.values)-int((df_players_stats.DREB.mean())))
            # st.metric("Perdidas", df_players_stats[df_players_stats.PLAYER_ID == id_player].TOV.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].TOV.values)-int((df_players_stats.TOV.mean())))
            # st.metric("Robos", df_players_stats[df_players_stats.PLAYER_ID == id_player].STL.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].STL.values)-int((df_players_stats.STL.mean())))
            # st.metric("Bloqueos", df_players_stats[df_players_stats.PLAYER_ID == id_player].BLK.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].BLK.values)-int((df_players_stats.BLK.mean())))
            # st.metric("Faltas Personales", df_players_stats[df_players_stats.PLAYER_ID == id_player].PF.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].PF.values)-int((df_players_stats.PF.mean())))

        with c2:
            # st.write(int(df_players_stats[df_players_stats.PLAYER_ID == id_player].PLAYER_ID.values))
            # df_player_stsyears = endpoints.PlayerGameLogs(player_id_nullable=int(df_players_stats[df_players_stats.PLAYER_ID == id_player].PLAYER_ID.values), season_nullable=st.session_state.temporada).get_data_frames()[0]
            # df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=str(int(df_players_stats[df_players_stats.PLAYER_ID == id_player].PLAYER_ID.values))).get_data_frames()[1]
            if type_stats == "Totales":
                df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=id_player).get_data_frames()[1]
            if type_stats == "Por Game":
                df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=id_player, per_mode_detailed="PerGame").get_data_frames()[1]
            if type_stats == "Por 100 Posesiones":
                df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=id_player, per_mode_detailed="Per100Possessions").get_data_frames()[1]
            if type_stats == "Por 36 Minutos":
                df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=id_player, per_mode_detailed="Per36").get_data_frames()[1]

            if st.checkbox("Ver Tabla de Datos del Jugador."):
                st.dataframe(df_player_stsyears)
            
            # Preparando datos para graficar..
            # Ofensivas.
            df_psy_off = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','FGM','FG3M','FTM','OREB','AST','PTS']].set_index('GROUP_VALUE')
            df_psy_off = df_psy_off.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
            df_psy_off_plot_altair = df_psy_off.reset_index().melt(df_psy_off.index.names, var_name='Offensive Measure', value_name='y')
            # Defensivas.
            df_psy_def = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']].set_index('GROUP_VALUE')
            df_psy_def = df_psy_def.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
            df_psy_def_plot_altair = df_psy_def.reset_index().melt(df_psy_def.index.names, var_name='Defensive Measure', value_name='y')


            type_graph = st.radio("Tipos de Gráficas:",("Plotly","Altair"), horizontal=True)
            if type_graph == "Plotly":
                # Probando Gráficas..
                # st.dataframe(df_psy.reset_index())
                # Ofensivo.
                fig = px.line(df_psy_off.reset_index(), x=df_psy_off.reset_index().index, y=df_psy_off.columns.values, \
                title='Progresión del Jugador - Métricas Ofensivas por Temporadas.', template='plotly_dark')
                fig.update_layout(width=1000, height=400, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
                        tickmode = 'array',
                        tickvals = df_psy_off.reset_index().index,
                        ticktext = df_psy_off.reset_index()['GROUP_VALUE']), \
                    yaxis_title = "Count", \
                    legend_title = "Ataque")
                fig.update_traces(line=dict(width=3)) # Grosor de la linea
                fig.update_traces(mode="markers+lines", hovertemplate=None)
                fig.update_layout(hovermode="x unified")
                st.plotly_chart(fig, config= {'displayModeBar': False}, use_container_width=True)

                # Defensivo
                # fig = px.line(df_psy.loc[:,['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']], x=df_psy.index, y=df_psy.loc[:,['DREB','TOV','STL','BLK','PLUS_MINUS']].columns.values,
                fig = px.line(df_psy_def.reset_index(), x=df_psy_def.reset_index().index, y=df_psy_def.columns.values, \
                title='Progresión del Jugador - Métricas Defensivas por Temporadas.', template='plotly_dark')
                fig.update_layout(width=1200, height=400, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
                        tickmode = 'array',
                        tickvals = df_psy_def.reset_index().index,
                        ticktext = df_psy_def.reset_index()['GROUP_VALUE']), \
                    yaxis_title = "Count", \
                    legend_title = "Defensa")
                fig.update_traces(line=dict(width=3)) # Grosor de la linea
                fig.update_traces(mode="markers+lines", hovertemplate=None)
                fig.update_layout(hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)
            
            if type_graph == "Altair":

                # Preparamos los datos para el input del tipo de gráficas "Altair"..
                # ***Los jugadores que juegan en 2 o más equipos en una tempo (valor = "TOT"),
                # - Se filtra la fila con el valor "TOT", xa no contabilizarla y en función de las metricas se SUM(), o MEAN()
                # - Para estas graficas de métricas de cantidad en acciones defensivas u ofensivas, se utiliza el Sumarizar
                # para la temporada que el jugador ha jugado en 2 o más equipo (Debido a un traspaso..evidentemente)
                # Métricas Ofensivas.
                # df_psy = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','FGM','FG3M','FTM','OREB','AST','PTS']].set_index('GROUP_VALUE')
                # df_psy = df_psy.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
                # df_psy_plot_altair = df_psy.reset_index().melt(df_psy.index.names, var_name='Offensive Measure', value_name='y')
                
                # st.dataframe(df_psy_plot_altair)

                plot_line_chart = alt.Chart(df_psy_off_plot_altair) \
                        .mark_line().encode(alt.X('GROUP_VALUE', title='Temporada'), \
                        alt.Y('y', title='Count'), color='Ataque:N', \
                        tooltip=[alt.Tooltip("GROUP_VALUE", title='Temporada'),"Ataque", \
                        alt.Tooltip("y", title='Count')]).properties( \
                            title='Prograsión del Jugador - Métricas Ofensivas por Temporadas.', width=1200, height=350).interactive()
                
                st.altair_chart(plot_line_chart, use_container_width=True)

                # Métricas Defensivas.
                # df_psy = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']].set_index('GROUP_VALUE')
                # df_psy = df_psy.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
                # df_psy_plot_altair = df_psy.reset_index().melt(df_psy.index.names, var_name='Defensive Measure', value_name='y')
                
                # st.dataframe(df_psy_plot_altair)

                plot_line_chart = alt.Chart(df_psy_def_plot_altair) \
                        .mark_line().encode(alt.X('GROUP_VALUE', title='Temporada'), \
                        alt.Y('y', title='Count'), color='Defensa:N', \
                        tooltip=[alt.Tooltip("GROUP_VALUE", title='Temporada'),"Defensa", \
                        alt.Tooltip("y", title='Count')]).properties( \
                            title='Progresión del Jugador - Métricas Defensivas por Temporadas.', width=1200, height=350).interactive()

                st.altair_chart(plot_line_chart, use_container_width=True)

        with c3:
            # st.write(f"<h3> RANKINGS </h3>", unsafe_allow_html=True)  
            st.write("<h3> DEFENSA. </h3>", unsafe_allow_html=True)
            st.metric("DEF_RATING", df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].DEF_RATING.values, int(df_players_stats_adv[df_players_stats_adv.PLAYER_ID == id_player].DEF_RATING.values)-int((df_players_stats_adv.DEF_RATING.mean())))
            st.metric("Rebotes", df_players_stats[df_players_stats.PLAYER_ID == id_player].DREB.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].DREB.values)-int((df_players_stats.DREB.mean())))
            st.metric("Perdidas", df_players_stats[df_players_stats.PLAYER_ID == id_player].TOV.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].TOV.values)-int((df_players_stats.TOV.mean())))
            st.metric("Robos", df_players_stats[df_players_stats.PLAYER_ID == id_player].STL.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].STL.values)-int((df_players_stats.STL.mean())))
            st.metric("Bloqueos", df_players_stats[df_players_stats.PLAYER_ID == id_player].BLK.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].BLK.values)-int((df_players_stats.BLK.mean())))
            st.metric("Faltas Personales", df_players_stats[df_players_stats.PLAYER_ID == id_player].PF.values, int(df_players_stats[df_players_stats.PLAYER_ID == id_player].PF.values)-int((df_players_stats.PF.mean())))

# ------INI BackUp 01
    # time.sleep(1)
    # data_players = endpoints.leaguedashplayerstats.LeagueDashPlayerStats(season=st.session_state.temporada, timeout=40).get_data_frames()
    # df_players = pd.DataFrame(data_players[0])

    # # st.markdown(f"ESTADISTICAS POR JUGADORES - Temporada Regular ({st.session_state.temporada}).")
    # if st.checkbox("Ver Tabla de Datos:"):
    #         st.dataframe(df_players)
    
    # # st.write(df_players)

    # players = df_players.PLAYER_NAME.tolist()
    # # team_abbrev = df_players.TEAM_ABBREVIATION.tolist()
    # player_select = st.sidebar.selectbox("Player", players)

    # # df_players.PLAYER_NAME
    # # df_players.W_PCT.tolist()

    # if player_select:

    #     st.text(int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values))
    #     # player_img = add_logo3(logo_path="https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png", width=150, height=160)
    #     player_img = add_logo3(logo_path=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values)}.png", width=150, height=160)
    #     # st.sidebar.image(player_img)

    #     col1, col2, col3 = st.sidebar.columns([1,3,1])
    #     with col1:
    #         st.write("")
    #     with col2:
    #         st.image(player_img)
    #     with col3:
    #         st.write("")
        
    #     st.markdown(f"<h2 style='text-align: left; color: white; font-family:commanders'>{player_select} STATS (KPIs) -\
    #         {df_players[df_players.PLAYER_NAME == player_select].TEAM_ABBREVIATION.values}</h2>", unsafe_allow_html=True)

    #     df_player_bio = endpoints.leaguedashplayerbiostats.LeagueDashPlayerBioStats().get_data_frames()[0]
        
    #     if st.checkbox("Ver Tabla de Datos2:"):
    #         st.dataframe(df_player_bio)
        
    #     m1, m2, m3, m4, m5, m6 = st.columns((1,1,1,1,1,1))

    #     m1.metric("Edad:", df_player_bio[df_player_bio.PLAYER_NAME == player_select].AGE.values)
    #     m2.metric("Estatura:", str(df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_HEIGHT.values)) # \
    #         # + "'" + df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_HEIGHT.values.split("-")[1] + "''"))
    #     m3.metric("Embergadura:", str(df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_HEIGHT_INCHES.values))
    #     m4.metric("Peso:", str(df_player_bio[df_player_bio.PLAYER_NAME == player_select].PLAYER_WEIGHT.values))
    #     m5.metric("Universidad:", str(df_player_bio[df_player_bio.PLAYER_NAME == player_select].COLLEGE.values))
    #     m6.metric("Año Draft:", str(df_player_bio[df_player_bio.PLAYER_NAME == player_select].DRAFT_YEAR.values))

    #     st.text("--------------------------------------")

    #     m1, m2, m3, m4, m5, m6 = st.columns((1,1,1,1,1,1))
    
    #     # m1.metric(label='PTS', value=df_teams[df_teams.TEAM_NAME == team_select].PTS.values)
    #     m1.metric("PTS", df_players[df_players.PLAYER_NAME == player_select].PTS.values, int(df_players[df_players.PLAYER_NAME == player_select].PTS.values)-int((df_players.PTS.mean())))
        
    #     m2.metric("Wins",str(int(df_players[df_players.PLAYER_NAME == player_select].W.values))+" Victorias", int(df_players[df_players.PLAYER_NAME == player_select].W.values)-int((df_players.W.mean())))
        
    #     m3.metric("Lost", str(int(df_players[df_players.PLAYER_NAME == player_select].L.values))+" Derrotas", int(df_players[df_players.PLAYER_NAME == player_select].L.values)-int((df_players.L.mean())))
        
    #     m4.metric('WL_PCT', str(float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)), float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)-float((df_players.W_PCT.mean())))
        
    #     m5.metric('FG_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values)-float((df_players.FG_PCT.mean())))
        
    #     m6.metric('FG3_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values)-float((df_players.FG3_PCT.mean())))

    #     st.text("--------------------------------------")

    #     c1,c2,c3 = st.columns([1,4,1]) # Entre corchetes se define que tamaño en ancho tendrá la columna, con 
    #                                    # respecto a las demás..
        
    #     with c1:
    #         # m1, m2, m3, m4, m5, m6 = st.columns()
    
    #         # m1.metric(label='PTS', value=df_teams[df_teams.TEAM_NAME == team_select].PTS.values)
    #         st.metric(f"PTS [Media->{int(df_players.PTS.mean())}]", df_players[df_players.PLAYER_NAME == player_select].PTS.values, int(df_players[df_players.PLAYER_NAME == player_select].PTS.values)-int((df_players.PTS.mean())))
            
    #         st.metric("Wins",str(int(df_players[df_players.PLAYER_NAME == player_select].W.values))+" Victorias", int(df_players[df_players.PLAYER_NAME == player_select].W.values)-int((df_players.W.mean())))
            
    #         st.metric("Lost", str(int(df_players[df_players.PLAYER_NAME == player_select].L.values))+" Derrotas", int(df_players[df_players.PLAYER_NAME == player_select].L.values)-int((df_players.L.mean())))

    #     with c2:
    #         # st.write(int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values))
    #         # df_player_stsyears = endpoints.PlayerGameLogs(player_id_nullable=int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values), season_nullable=st.session_state.temporada).get_data_frames()[0]
    #         df_player_stsyears = endpoints.PlayerDashboardByYearOverYear(player_id=str(int(df_players[df_players.PLAYER_NAME == player_select].PLAYER_ID.values))).get_data_frames()[1]
            
    #         if st.checkbox("Ver Tabla de Datos del Jugador."):
    #             st.dataframe(df_player_stsyears)

    #         # Preparamos los datos para el input del tipo de gráficas "Altair"..
    #         # ***Los jugadores que juegan en 2 o más equipos en una tempo (valor = "TOT"),
    #         # - Se filtra la fila con el valor "TOT", xa no contabilizarla y en función de las metricas se SUM(), o MEAN()
    #         # - Para estas graficas de métricas de cantidad en acciones defensivas u ofensivas, se utiliza el Sumarizar
    #         # para la temporada que el jugador ha jugado en 2 o más equipo (Debido a un traspaso..evidentemente)
            
    #         # Métricas Ofensivas.
    #         df_psy = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','FGM','FG3M','FTM','OREB','AST','PTS']].set_index('GROUP_VALUE')
    #         df_psy = df_psy.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
    #         df_psy_plot_altair = df_psy.reset_index().melt(df_psy.index.names, var_name='Offensive Measure', value_name='y')
            
    #         # st.dataframe(df_psy_plot_altair)

    #         plot_line_chart = alt.Chart(df_psy_plot_altair) \
    #                   .mark_line().encode(alt.X('GROUP_VALUE', title='Temporada'), \
    #                   alt.Y('y', title='Count'), color='Offensive Measure:N', \
    #                   tooltip=[alt.Tooltip("GROUP_VALUE", title='Temporada'),"Offensive Measure", \
    #                   alt.Tooltip("y", title='Count')]).properties( \
    #                     title='Métricas Ofensivas por Temporadas.').interactive()

    #         st.altair_chart(plot_line_chart, use_container_width=True)

    #         # Métricas Defensivas.
    #         df_psy = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']].set_index('GROUP_VALUE')
    #         df_psy = df_psy.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
    #         df_psy_plot_altair = df_psy.reset_index().melt(df_psy.index.names, var_name='Defensive Measure', value_name='y')
            
    #         # st.dataframe(df_psy_plot_altair)

    #         plot_line_chart = alt.Chart(df_psy_plot_altair) \
    #                   .mark_line().encode(alt.X('GROUP_VALUE', title='Temporada'), \
    #                   alt.Y('y', title='Count'), color='Defensive Measure:N', \
    #                   tooltip=[alt.Tooltip("GROUP_VALUE", title='Temporada'),"Defensive Measure", \
    #                   alt.Tooltip("y", title='Count')]).properties( \
    #                     title='Métricas Defensivas por Temporadas.').interactive()

    #         st.altair_chart(plot_line_chart, use_container_width=True)

    #         # Probando Gráficas..
    #         # st.dataframe(df_psy.reset_index())

    #         # fig = px.line(df_psy.loc[:,['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']], x=df_psy.index, y=df_psy.loc[:,['DREB','TOV','STL','BLK','PLUS_MINUS']].columns.values,
    #         fig = px.line(df_psy.reset_index(), x=df_psy.reset_index().index, y=df_psy.columns.values, \
    #           title='Métricas Defensivas por Temporadas.', template='plotly_dark')
    #         fig.update_layout(width=1000, height=400, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
    #                 tickmode = 'array',
    #                 tickvals = df_psy.reset_index().index,
    #                 ticktext = df_psy.reset_index()['GROUP_VALUE']), \
    #             yaxis_title = "Count", \
    #             legend_title = "Defensive Measure")
    #         fig.update_traces(line=dict(width=3)) # Grosor de la linea
    #         fig.update_traces(mode="markers+lines", hovertemplate=None)
    #         fig.update_layout(hovermode="x unified")
    #         st.plotly_chart(fig, use_container_width=True)

    #     with c3:  
    #         st.metric('WL_PCT', str(float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)), float(df_players[df_players.PLAYER_NAME == player_select].W_PCT.values)-float((df_players.W_PCT.mean())))
            
    #         st.metric('FG_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG_PCT.values)-float((df_players.FG_PCT.mean())))
            
    #         st.metric('FG3_PCT', float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values), float(df_players[df_players.PLAYER_NAME == player_select].FG3_PCT.values)-float((df_players.FG3_PCT.mean())))
# --------- Fin Backup 01 ----------

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

def teams_stats():

    # Estadisticas generales por equipos en la tempRegular seleccionadal..
    # st.text(st.session_state.temporada)
  
    # data_teams =  teams.get_teams()# Lista de Objetos Json, con los Equipos de la Temp Actual
    df_teams = pd.DataFrame(teams.get_teams()) # Conviertes en Dframe el objeto data

    #teams = df_teams.drop(labels=["TEAM_NAME"], axis=1).columns.tolist()
    teams_names = df_teams.full_name.tolist()

    team_select = st.sidebar.selectbox("Team", teams_names)

    # st.markdown("ESTADISTICAS POR EQUIPOS - Temporada Regular (21/22).")

    # st.markdown("""
    #             <div class="waveWrapper waveAnimation">
    #             <div class="waveWrapperInner bgTop">
    #                 <div class="wave waveTop" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-top.png')"></div>
    #             </div>
    #             <div class="waveWrapperInner bgMiddle">
    #                 <div class="wave waveMiddle" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-mid.png')"></div>
    #             </div>
    #             <div class="waveWrapperInner bgBottom">
    #                 <div class="wave waveBottom" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-bot.png')"></div>
    #             </div>
    #             </div>
    #             """, unsafe_allow_html=True)

    if team_select:
        # st.text(team_select)
        id_team = int(df_teams[df_teams.full_name == team_select].id.values)
        # Intrucciones para visualizar el logo de cada team en función de la seleccion en el sidebar..
        # Esto puede cambiar en cualquier momento ya que la imagen esta en la red, y no en local..
        # teams_abbre = {'Atlanta Hawks': 'atl','Brooklyn Nets': 'bkn','Boston Celtics': 'bos','Charlotte Hornets': 'cha','Chicago Bulls': 'chi', \
        #     'Cleveland Cavaliers': 'cle','Dallas Mavericks': 'dal','Denver Nuggets': 'den','Detroit Pistons': 'det','Golden State Warriors': 'gsw', \
        #     'Houston Rockets': 'hou','Indiana Pacers': 'ind','LA Clippers': 'lac','Los Angeles Lakers': 'lal','Memphis Grizzlies': 'mem', \
        #     'Miami Heat': 'mia','Milwaukee Bucks': 'mil','Minnesota Timberwolves': 'min','New Orleans Pelicans': 'nop','New York Knicks': 'nyk', \
        #     'Oklahoma City Thunder': 'okc','Orlando Magic': 'orl','Philadelphia 76ers': 'phi','Phoenix Suns': 'phx','Portland Trail Blazers': 'por', \
        #     'Sacramento Kings': 'sac','San Antonio Spurs': 'sas','Toronto Raptors': 'tor','Utah Jazz': 'uta','Washington Wizards': 'was'
        #     }

        # st.text(teams_abbre.get(team_select))
        # A partir de DF general de equipos acceder al valor del Nick y convertirlo en minusculas..
        # st.text(df_teams[df_teams.full_name == team_select]._get_value(0,"abbreviation").lower())
        # st.text(df_teams.loc[df_teams.id == id_team].abbreviation.values[0].lower())
        # team_nick_lower = df_teams[df_teams.full_name == team_select]._get_value(0,"abbreviation").lower()

        # my_logo2 = add_logo2(logo_path=f"https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/{teams_abbre.get(team_select)}.png", width=150, height=150)
        url_logo_teams = "https://www.nba.com/.element/img/1.0/teamsites/logos/teamlogos_500x500/"
        my_logo2 = add_logo2(logo_path=f"{url_logo_teams + df_teams[df_teams.id == id_team].abbreviation.values[0].lower()}.png", width=150, height=150)

        col1, col2, col3 = st.sidebar.columns([1,3,1])

        with col1:
            st.write("")
        with col2:
            st.image(my_logo2)
        with col3:
            st.write("")
        
        # df_team_details = endpoints.TeamDetails(team_id=df_teams[df_teams.full_name == team_select].id).get_data_frames()[0]
        df_team_details = endpoints.TeamDetails(team_id=id_team).get_data_frames()[0]
        df_team_info = endpoints.TeamInfoCommon(team_id=id_team, season_nullable=st.session_state.temporada).get_data_frames()[0]
        df_team_info1 = endpoints.TeamInfoCommon(team_id=id_team, season_nullable=st.session_state.temporada).get_data_frames()[1]

        # st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-family:commanders'>Fundada: { df_team_details._get_value(0, 'YEARFOUNDED') }</h1>", unsafe_allow_html=True)
        # st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-family:commanders'>Ciudad: { df_team_details._get_value(0, 'CITY') }</h1>", unsafe_allow_html=True)
        # st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-family:commanders'>Estadio: { df_team_details._get_value(0, 'ARENA')} \
        #     Capacidad: { format(int(df_team_details._get_value(0, 'ARENACAPACITY')), ',d')} asientos</h1>", unsafe_allow_html=True)
        # st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-family:commanders'>Dueño: { df_team_details._get_value(0, 'OWNER')} \
        #     Manager General: { df_team_details._get_value(0, 'GENERALMANAGER')}</h1>", unsafe_allow_html=True)
        # st.sidebar.markdown(f"<h1 style='text-align: left; color: white; font-family:commanders'>Entrenador: { df_team_details._get_value(0, 'HEADCOACH') }</h1>", unsafe_allow_html=True)
        
        # st.markdown(f"<h2 style='text-align: left; color: #1569C7; font-family:commanders'>{player_select} STATS (KPIs) -\
        #     {df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'TEAM_CITY') + ' ' + df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'TEAM_NAME')} \
        #      - #{df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'JERSEY')} \
        #      - {df_player_info[df_player_info.PERSON_ID == id_player]._get_value(0, 'POSITION')}</h2>", unsafe_allow_html=True)

        c1, c2 = st.columns([1.5,2])

        with c1:
            st.markdown(f"<h1 style='text-align: left; color: ; font-family:commanders'>&#9679 {team_select}</h1>",unsafe_allow_html=True) # - \
                # Conferencia {df_team_info._get_value(0,'TEAM_CONFERENCE').upper() + ' [Rank ' + str(df_team_info._get_value(0,'CONF_RANK')) + 'º]'} - \
                # División {df_team_info._get_value(0,'TEAM_DIVISION').upper() + ' [Rank ' + str(df_team_info._get_value(0,'DIV_RANK')) + 'º]'}</h2>",unsafe_allow_html=True)

            # data_teams = endpoints.LeagueDashTeamStats(season=st.session_state.temporada).get_data_frames()
            # df_teams = pd.DataFrame(data_teams[0])
            type_stats = st.radio("",("Totales","Por Game", "Por 100 Posesiones"), horizontal=True)
            if type_stats == "Totales":
                df_teams_stats = endpoints.LeagueDashTeamStats(season=st.session_state.temporada).get_data_frames()[0]
            if type_stats == "Por Game":
                df_teams_stats = endpoints.LeagueDashTeamStats(season=st.session_state.temporada, per_mode_detailed="PerGame").get_data_frames()[0]
            if type_stats == "Por 100 Posesiones":
                df_teams_stats = endpoints.LeagueDashTeamStats(season=st.session_state.temporada, per_mode_detailed="Per100Possessions").get_data_frames()[0]

        with c2:
            # st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>{team_select.upper()}</h2>",unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 Conferencia {df_team_info._get_value(0,'TEAM_CONFERENCE').upper() + ' - [Rank ' + str(df_team_info._get_value(0,'CONF_RANK')) + 'º]'}</h2>",unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: left; color: ; font-family:commanders'>&#9658 División {df_team_info._get_value(0,'TEAM_DIVISION').upper() + ' - [Rank ' + str(df_team_info._get_value(0,'DIV_RANK')) + 'º]'}</h2>",unsafe_allow_html=True)

        
        if st.checkbox("Ver Tablas de Datos del Jugador."):
            
            # st.dataframe(df_teams_stats)
            st.write(df_teams_stats)

            # Pintar tabla con estilos...***Buscar como hacerla dinamica..
            st.text(list(df_teams_stats.columns))
            # with st.container():
            fig_table = plygo.Figure(data=plygo.Table( \
                header=dict(values=list(df_teams_stats.iloc[:,:8].columns), \
                    fill_color='paleturquoise', align='center', font=dict(color='black', size=12)), \
                    # fill_color='paleturquoise', align='center'), \
                cells=dict(values=[df_teams_stats.iloc[:,num] for num in range(len(df_teams_stats.iloc[:,:8].columns))], \
                    fill_color='lavender', align='left', font=dict(color='black', size=12))))

            fig_table.update_layout(margin=dict(l=3,r=3,b=3,t=3)) # Para ajustar la tabla a todo el contorno del obj plotly

            st.write(fig_table, use_container_width=True)

        # m1, m2, m3 = st.sidebar.columns((1,1,1))

        # m1.write(f"<h3>Fundada: </h3>{df_team_details._get_value(0, 'YEARFOUNDED')}", unsafe_allow_html=True)
        # # m2.write(f'<h3>Estatura: </h3>{str(df_player_bio.loc[df_player_bio.PLAYER_ID == id_player, "PLAYER_HEIGHT"].values), estatura, estatura2}', unsafe_allow_html=True)
        # m2.write(f"<h3>Ciudad: </h3>{df_team_details._get_value(0, 'CITY')} ", unsafe_allow_html=True)
        # m3.write(f"<h3>Estadio: </h3>{df_team_details._get_value(0, 'ARENA')} ", unsafe_allow_html=True)
        # m3.write(f"<h3>Capacidad: </h3>{format(int(df_team_details._get_value(0, 'ARENACAPACITY')), ',d')} asientos", unsafe_allow_html=True)

        # m4, m5, m6 = st.sidebar.columns((1,1,1))

        # m4.write(f"<h3>Dueño: </h3>{df_team_details._get_value(0, 'OWNER')} ", unsafe_allow_html=True)
        # m5.write(f"<h3>Manager General: </h3>{df_team_details._get_value(0, 'GENERALMANAGER')}", unsafe_allow_html=True)
        # m6.write(f"<h3>Entrenador: </h3>{df_team_details._get_value(0, 'HEADCOACH')}", unsafe_allow_html=True)

        m1, = st.sidebar.columns([2])

        m1.write(f"<h3>Fundada: {df_team_details._get_value(0, 'YEARFOUNDED')}</h3>", unsafe_allow_html=True)
        # m2.write(f'<h3>Estatura: </h3>{str(df_player_bio.loc[df_player_bio.PLAYER_ID == id_player, "PLAYER_HEIGHT"].values), estatura, estatura2}', unsafe_allow_html=True)
        m1.write(f"<h3>Ciudad: {df_team_details._get_value(0, 'CITY')}</h3>", unsafe_allow_html=True)
        m1.write(f"<h3>Estadio: {df_team_details._get_value(0, 'ARENA')}</h3>", unsafe_allow_html=True)
        # m1.write(f"<h3>Capacidad: {format(int(df_team_details._get_value(0, 'ARENACAPACITY')), ',d')} asientos</h3>", unsafe_allow_html=True)
        m1.write(f"<h3>Capacidad: {'NoData' if df_team_details._get_value(0, 'ARENACAPACITY') is None else format(int(df_team_details._get_value(0, 'ARENACAPACITY')), ',d') } asientos</h3>", unsafe_allow_html=True)

        # m4, m5, m6 = st.sidebar.columns((1,1,1))

        m1.write(f"<h3>Dueño: {df_team_details._get_value(0, 'OWNER')}</h3>", unsafe_allow_html=True)
        m1.write(f"<h3>Manager General: {df_team_details._get_value(0, 'GENERALMANAGER')}</h3>", unsafe_allow_html=True)
        m1.write(f"<h3>Entrenador: {df_team_details._get_value(0, 'HEADCOACH')}</h3>", unsafe_allow_html=True)

        st.text("------------------------------------------------------------------")
        # type_stats = st.radio("",("Totals","Per Game"), horizontal=True)
        
        # Pruebas..
        # st.text(df_teams_stats.PTS.sum())
        # st.text(df_teams_stats.PTS.mean())
        # st.text(df_teams_stats.PLUS_MINUS.mean())
        # st.text((df_teams_stats.PTS - df_teams_stats.PLUS_MINUS).mean())
        df_teams_stats_adv = endpoints.LeagueDashTeamStats(season=st.session_state.temporada, measure_type_detailed_defense="Advanced").get_data_frames()[0]


        # Otra manera de visualizar las estadisticas medias del TEAM..
        m1, m11, m12, m2, m3, m4, m41, m42, m43, m5, m6, m7 = st.columns((1.1,1.1,1,0.5,0.5,1,1,1,1,1,1,1))

        # todf = pd.read_excel('DataforMock.xlsx',sheet_name = 'metrics')
        # to = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Total Outstanding')]   
        # ch = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Current Handover Average Mins')]   
        # hl = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Hours Lost to Handovers Over 15 Mins')]
        
        # m1.metric(label='PTS', value=df_teams_stats[df_teams_stats.TEAM_ID == id_team].PTS.values)
        m1.metric("PTS Anotados", "{:,}".format(round(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].PTS.values),2)), round(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].PTS.values)-float(df_teams_stats.PTS.mean()),2))

        # Pruebas para formular en .ipynb de Puntos totales y por Cuartos de los GAMES..
        m11.metric("PTS Recibidos", "{:,}".format(round(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].PTS.values - df_teams_stats[df_teams_stats.TEAM_ID == id_team].PLUS_MINUS.values),2)), \
            round(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].PTS.values - df_teams_stats[df_teams_stats.TEAM_ID == id_team].PLUS_MINUS.values)-float((df_teams_stats.PTS - df_teams_stats.PLUS_MINUS).mean()),2))
        
        m12.metric("NET_RATING(+/-)", df_teams_stats[df_teams_stats.TEAM_ID == id_team].PLUS_MINUS.values, round(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].PLUS_MINUS.values)-float(df_teams_stats.PLUS_MINUS.mean()),2))

        # m2.metric(label='Wins',value=str(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].W.values))+" Victorias") #, delta = str(int(ch['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
        m2.metric("WINS",str(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].W.values)), int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].W.values)-int((df_teams_stats.W.mean())))
        # m3.metric(label='Lost',value=str(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].L.values)) +" Derrotas") #, delta = str(int(hl['Previous']))+' Compared to yesterday')
        m3.metric("LOST", str(int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].L.values)), int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].L.values)-int((df_teams_stats.L.mean())))
        # m4.metric(label='WL_PCT',value=str(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].W_PCT.values))) #, delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
        m4.metric('WL_PCT', str(round(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].W_PCT.values * 100),2))+'%', \
            str(round((float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].W_PCT.values)-float(df_teams_stats.W_PCT.mean()))*100,2))+'%')
        # m5.metric(label='FG_PCT',value=str(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG_PCT.values)))
        
        m41.metric("PACE", str(float(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].PACE.values)), \
            str(round((float(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].PACE.values)-float(df_teams_stats_adv.PACE.mean())) *100,2)))

        m42.metric("EFG_PCT(F)", str(round(float(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].EFG_PCT.values *100),2))+'%', \
            str(round((float(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].EFG_PCT.values)-float(df_teams_stats_adv.EFG_PCT.mean())) *100,2))+'%')
        
        m43.metric("PIE(F)", str(round(float(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].PIE.values *100),2))+'%', \
            str(round((float(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].PIE.values)-float(df_teams_stats_adv.PIE.mean())) *100,2))+'%')
        
        m5.metric('FG_PCT', str(round(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG_PCT.values * 100),2))+'%', \
            str(round((float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG_PCT.values)-float(df_teams_stats.FG_PCT.mean()))*100,2))+'%')
        #  m6.metric(label='FG3_PCT',value=str(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3_PCT.values)))
        m6.metric('FG3_PCT', str(round(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3_PCT.values * 100),2))+'%', \
            str(round((float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3_PCT.values)-float(df_teams_stats.FG3_PCT.mean()))*100,2))+'%')

        m7.metric('FT_PCT', str(round(float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FT_PCT.values * 100),2))+'%', \
            str(round((float(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FT_PCT.values)-float(df_teams_stats.FT_PCT.mean()))*100,2))+'%')

        # INfo Stadisticas generales a lo largo de todas las temporadas en activo
        # data_team = endpoints.teamyearbyyearstats.TeamYearByYearStats(team_id=df_teams_stats[df_teams_stats.TEAM_ID == id_team].TEAM_ID.values) # ID Team Seleccionado
        # df_team = data_team.team_stats.get_data_frame() # Se utiliza uno de los metodos de la libreria xa convertirlo en DFrame..

        st.text("------------------------------------------------------------------")

        c1,c2,c3 = st.columns([0.5,4,0.5]) # Entre corchetes se define que tamaño en ancho tendrá la columna, con 
                                       # respecto a las demás..
        
        with c1:
            st.write("<h3> ATAQUE. </h3>", unsafe_allow_html=True)

            st.metric("OFF_RATING", df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].OFF_RATING.values, int(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].OFF_RATING.values)-int((df_teams_stats_adv.OFF_RATING.mean())))
            st.metric("FG_Made", df_teams_stats[df_teams_stats.TEAM_ID == id_team].FGM.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FGM.values)-int((df_teams_stats.FGM.mean())))
            st.metric("FG3_Convertidos", df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3M.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3M.values)-int((df_teams_stats.FG3M.mean())))
            # st.metric("FG3_Convertidos 02", int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3M.values) / int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].GP.values), int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FG3M.values)-int((df_teams_stats.FG3M.mean())))
            st.metric("FT_Made", df_teams_stats[df_teams_stats.TEAM_ID == id_team].FTM.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].FTM.values)-int((df_teams_stats.FTM.mean())))
            st.metric("Rebotes", df_teams_stats[df_teams_stats.TEAM_ID == id_team].OREB.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].OREB.values)-int((df_teams_stats.OREB.mean())))
            st.metric("Asistencias", df_teams_stats[df_teams_stats.TEAM_ID == id_team].AST.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].AST.values)-int((df_teams_stats.AST.mean())))
        

        with c2:

            if type_stats == "Totales":
                df_team_stats_years = endpoints.TeamYearByYearStats(team_id=id_team).get_data_frames()[0]
            if type_stats == "Por Game" or type_stats == "Por 100 Posesiones" :
                df_team_stats_years = endpoints.TeamYearByYearStats(team_id=id_team, per_mode_simple="PerGame").get_data_frames()[0]
            # if type_stats == "Por 100 Posesiones":
            
            if st.checkbox("Ver Tabla de Datos del Jugador."):
                st.write(df_team_stats_years)
                # st.write(df_team_stats_years.loc[:,['YEAR','WINS','LOSSES']].set_index('YEAR'))
                # st.text(df_team_stats_years.loc[:,['WINS','LOSSES']].columns.values)
            
             # Preparando datos para graficar..
            # Ofensivas.
            # df_tsy_off = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','FGM','FG3M','FTM','OREB','AST','PTS']].set_index('GROUP_VALUE')
            # df_psy_off = df_psy_off.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
            # df_psy_off_plot_altair = df_psy_off.reset_index().melt(df_psy_off.index.names, var_name='Offensive Measure', value_name='y')
            # # Defensivas.
            # df_psy_def = df_player_stsyears.loc[df_player_stsyears.TEAM_ABBREVIATION != 'TOT',['GROUP_VALUE','DREB','TOV','STL','BLK','PLUS_MINUS']].set_index('GROUP_VALUE')
            # df_psy_def = df_psy_def.groupby(by='GROUP_VALUE').sum() # Para este caso de métricas de cantidad de acciones del juego Ofensivas se Sumariza
            # df_psy_def_plot_altair = df_psy_def.reset_index().melt(df_psy_def.index.names, var_name='Defensive Measure', value_name='y')

            # NO CONSIGO QUE GRAFIQUE TODOS LOS AÑOS
            #fig = px.line(df_team_stats_years, x='YEAR', y=('WINS','LOSSSES'), color='TEAM_NAME')
            #fig = px.line(df_team_stats_years.loc[:,['YEAR','WINS','LOSSES']].set_index('YEAR')) # # OK
            #fig = px.line(df_team_stats_years.loc[:,['YEAR','WINS','LOSSES']], x='YEAR')
            # fig = px.line(df_team_stats_years, x=str('YEAR'),  y=df_team_stats_years.loc[:,['WINS','LOSSES']].columns.values, hover_data={'YEAR':"%Y"}) # OK
            # fig.update_layout(width=1200, height=500, font=dict(size=15), title='Historico WINS/LOST')
            # st.plotly_chart(fig, use_container_width=True)

            # CONSEGUIDOO!! https://stackoverflow.com/questions/60525196/python-pandas-and-plotly-having-trouble-with-dates-and-display
            # Anotaciones en el gráfico.
            # https://medium.com/nerd-for-tech/enriching-data-visualizations-with-annotations-in-plotly-using-python-6127ff6e0f80
            # https://plotly.com/python/configuration-options/
            
            # Templates configuration
            # Default template: 'plotly'
            # Available templates:
            #     ['ggplot2', 'seaborn', 'simple_white', 'plotly',
            #     'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
            #     'ygridoff', 'gridon', 'none']

            # Win / Lost Historico
            fig = px.line(df_team_stats_years, x=df_team_stats_years.index, y=df_team_stats_years.loc[:,['WINS','LOSSES']].columns.values,
                title='Número de Wins/Lost por Temporada.', template='plotly_dark')
            fig.update_layout(width=1200, height=500, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
                    tickmode = 'array',
                    tickvals = df_team_stats_years.index,
                    ticktext = df_team_stats_years["YEAR"]),
                yaxis_title = "Count",
                legend_title = "W / L")
            fig.update_traces(line=dict(width=3)) # Grosor de la linea
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, config= {'displayModeBar': False}, use_container_width=True)

            # Ataque.
            fig = px.line(df_team_stats_years, x=df_team_stats_years.index, y=df_team_stats_years.loc[:,['FGM','FG3M','FTM','OREB','AST','PTS']].columns.values,
                title='Progresión Team en métricas ofensivas tradicionales.', template='plotly_dark')
            fig.update_layout(width=1200, height=500, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
                    tickmode = 'array',
                    tickvals = df_team_stats_years.index,
                    ticktext = df_team_stats_years["YEAR"]),
                yaxis_title = "Count",
                legend_title = "Ataque.")
            fig.update_traces(line=dict(width=3)) # Grosor de la linea
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, config= {'displayModeBar': False}, use_container_width=True)

            # Defensa.
            fig = px.line(df_team_stats_years, x=df_team_stats_years.index, y=df_team_stats_years.loc[:,['DREB','TOV','STL','BLK','PF']].columns.values,
                title='Progresión Team en métricas defensivas tradicionales.', template='plotly_dark')
            fig.update_layout(width=1200, height=500, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
                    tickmode = 'array',
                    tickvals = df_team_stats_years.index,
                    ticktext = df_team_stats_years["YEAR"]),
                yaxis_title = "Count",
                legend_title = "Defensa.")
            fig.update_traces(line=dict(width=3)) # Grosor de la linea
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, config= {'displayModeBar': False}, use_container_width=True)

            # df_team01 = df_team_stats_years.loc[:,['YEAR','WINS','LOSSES']]
            # st.write(df_team01)

            # fig = px.line(df_team01, x=df_team01.index, y=df_team01.loc[:,['WINS','LOSSES']].columns.values,
            #       title='Número de Wins/Lost por Temporada.', template='plotly_dark')
            # fig.update_layout(width=1200, height=500, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
            #         tickmode = 'array',
            #         tickvals = df_team01.index,
            #         ticktext = df_team01["YEAR"]),
            #     yaxis_title = "Count",
            #     legend_title = "Leyenda")
            # fig.update_traces(line=dict(width=3)) # Grosor de la linea
            # fig.update_traces(mode="markers+lines", hovertemplate=None)
            # fig.update_layout(hovermode="x unified")
            # st.plotly_chart(fig, use_container_width=False)

            # fig = px.line(df_team01, x=df_team01.index, y=df_team01.loc[:,['WINS','LOSSES']].columns.values,
            #       title='Número de Wins/Lost por Temporada.', template='simple_white')
            # fig.add_annotation(
            #     x=26,
            #     y=68,
            #     #xref="Temporada",
            #     #yref="value",
            #     text="ANILLO Celtics",
            #     showarrow=True,
            #     font=dict(
            #         family="Courier New, monospace",
            #         size=16,
            #         color="#ffffff"
            #         ),
            #     align="center",
            #     arrowhead=2,
            #     arrowsize=1,
            #     arrowwidth=2,
            #     arrowcolor="#ff7f0e",
            #     ax=20,
            #     ay=-30,
            #     bordercolor="#c7c7c7",
            #     borderwidth=2,
            #     borderpad=4,
            #     bgcolor="#ff7f0e",
            #     opacity=0.8
            # )
            # fig.update_layout(width=1200, height=500, font=dict(size=15), xaxis_title='Temporada', xaxis = dict(
            #     tickmode = 'array',
            #     tickvals = df_team01.index,
            #     ticktext = df_team01["YEAR"]))
            # fig.update_traces(line=dict(width=5)) # Grosor de la linea
            # st.plotly_chart(fig, config= {'displayModeBar': False})
            #                             #   'displaylogo': False,
            #                             #   'scrollZoom': False,
            #                             #   'editable': True,
            #                             #   'showLink':False,})
        
        with c3:
            st.write("<h3> DEFENSA. </h3>", unsafe_allow_html=True)

            st.metric("DEF_RATING", df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].DEF_RATING.values, int(df_teams_stats_adv[df_teams_stats_adv.TEAM_ID == id_team].DEF_RATING.values)-int((df_teams_stats_adv.DEF_RATING.mean())))
            st.metric("Rebotes", df_teams_stats[df_teams_stats.TEAM_ID == id_team].DREB.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].DREB.values)-int((df_teams_stats.DREB.mean())))
            st.metric("Perdidas", df_teams_stats[df_teams_stats.TEAM_ID == id_team].TOV.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].TOV.values)-int((df_teams_stats.TOV.mean())))
            st.metric("Robos", df_teams_stats[df_teams_stats.TEAM_ID == id_team].STL.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].STL.values)-int((df_teams_stats.STL.mean())))
            st.metric("Bloqueos", df_teams_stats[df_teams_stats.TEAM_ID == id_team].BLK.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].BLK.values)-int((df_teams_stats.BLK.mean())))
            st.metric("Faltas Personales", df_teams_stats[df_teams_stats.TEAM_ID == id_team].PF.values, int(df_teams_stats[df_teams_stats.TEAM_ID == id_team].PF.values)-int((df_teams_stats.PF.mean())))
        



        chart1, chart2 = st.columns(2)

        with chart1:
            st.line_chart(df_team_stats_years.loc[:,['YEAR','WINS','LOSSES']].set_index('YEAR')) # Pinta todos los años
            
            # df_team01 = df_team.loc[:,['YEAR','WINS','LOSSES']].set_index('YEAR')
            # df_team01 = df_team01.reset_index().melt(df_team01.index.names, var_name='category', value_name='y')
            
            # plot_line_chart = alt.Chart(df_team01) \
            #           .mark_line(interpolate='basis').encode(alt.X('YEAR', title='YEAR'), \
            #           alt.Y('y', title='VALUES'), color='category:N').properties( \
            #             title='Número de Wins/Lost Por Temporadas.')

            # st.altair_chart(plot_line_chart)
        
        with chart2:
            st.line_chart(df_team_stats_years.loc[:,['YEAR','PTS','REB','AST']].set_index('YEAR')) # Pinta todos los años

        chart1, chart2 = st.columns(2)

        with chart1:
            df_team01 = df_team_stats_years.loc[:,['YEAR','WINS','LOSSES']].set_index('YEAR')
            df_team01 = df_team01.reset_index().melt(df_team01.index.names, var_name='category', value_name='y')
            
            plot_line_chart = alt.Chart(df_team01) \
                      .mark_line().encode(alt.X('YEAR', title='YEAR'), \
                      alt.Y('y', title='VALUES'), color='category:N', \
                      tooltip=["YEAR","category","y"]).properties( \
                        title='Número de Win/Lost Por Temporadas.').interactive()

            st.altair_chart(plot_line_chart, use_container_width=True)

        with chart2:
            df_team01 = df_team_stats_years.loc[:,['YEAR','PTS','REB','AST']].set_index('YEAR')
            df_team01 = df_team01.reset_index().melt(df_team01.index.names, var_name='category', value_name='y')
            
            plot_line_chart = alt.Chart(df_team01) \
                      .mark_line().encode(alt.X('YEAR', title='Year'), \
                      alt.Y('y', title='Values'), color='category:N', \
                      tooltip=["YEAR","category","y"]).properties( \
                        title='Número de PTS/AST/REB Por Temporadas.').interactive()

            st.altair_chart(plot_line_chart, use_container_width=True)

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

    # -- INI Prueba 01 - Select Teams for compare [] ---------
    # ---- BackUP Prueba 01 ----------------------------------
    # # Gráfica de Radar con el DF agrupado por Team para obtener los promedios de cada uno de los Teams
    # df_teams_radar = df_games_full_01.iloc[3:5,[0,1,2,3]] # filas en posición 3 y 4

    # # df_teams_radar.columns
    # # df_teams_radar.index.values
    # # df_teams_radar.iloc[0].values # Retorna los valores de cada atributo/columna de la fila con indice "n"

    # fig = plygo.Figure()

    # for ind in range(len(df_teams_radar.index.values)):
    #     print(ind)
    #     fig.add_trace(plygo.Scatterpolar(r=df_teams_radar.iloc[ind].values,
    #                                     theta=df_teams_radar.columns,
    #                                     fill='toself',
    #                                     #name="TypeWine-%s"%datasets.load_wine().target_names[ind],
    #                                     name="Team-%s"%df_teams_radar.index[ind], # Recupera los rownames del dataframe..
    #                                     showlegend=True,)
    #                                     )

    # fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 40])),
    #                             title="Promedio Puntos por Cuartos y OT")
    # st.plotly_chart(fig)
    # -- BackUP Prueba 01 ----------------------------------

    c1, c2 = st.columns([1,2])

    with c1:
        team_A = st.selectbox("Team A", df_games_full_01.index.to_list())
        team_B = st.selectbox("Team B", df_games_full_01.index.to_list())

        # df_teams_radar = df_games_full_01.iloc[3:5,[0,1,2,3]] # filas en posición 3 y 4
        df_teams_radar = df_games_full_01.loc[df_games_full_01.index.isin([team_A,team_B]),['PTS_QTR1','PTS_QTR2','PTS_QTR3','PTS_QTR4']] # filas en posición 3 y 4

        st.write(df_teams_radar)
    
    with c2:

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
  
  
