"""
## App: Pagina Principal RGA Data Sceience 01
## Autor: RGA
Description
- EDA sobre estadisticas avanzadas de la NBA
- Implementación de Modelos de Clasificación/Segmentación
- "basketball_reference_scraper" API(Técnicas de Scrapping) para recuperar los conjuntos de datos de www.basketball-reference.com
"""
# Packages
import streamlit as st

# ScrappingWEB-EDA Pkgs
import pandas as pd
import numpy as np
import os
from os import remove
import base64
# from lxml import etree
# Plotting Pkgs
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
import seaborn as sns
from PIL import Image,ImageFilter,ImageEnhance

import functions_01 as f01

BASE_URL = 'https://www.basketball-reference.com/'
STAT_TYPES = ['per_game', 'totals', 'per_minute', 'advanced', 'per_poss', 'play-by-play', 'advanced_box_score']
ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']

# Función de github, para scrapear las tablas de estadisticas de Players de "basketball_reference.com"
def get_players_stats(season: int, stat_type: str, header: int = 0, filter_games=True, remove_duplicates=True):
    
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



if __name__ == "__main__":
        
    st.set_page_config(layout="wide") # NO se puede configurar este parametro varias veces..solo una.
    # main()
    
    # DATA (Scrapping con funciones que raspan de "basketball-reference.com")
    # Recuperando los datos de players "totals","Advanced" para la temporada actual, y unir la col "PER" a tabla "totals"
    if 'df_players' not in st.session_state:
        BASE_URL = 'https://www.basketball-reference.com/'
        STAT_TYPES = ['per_game', 'totals', 'per_minute', 'advanced', 'per_poss', 'play-by-play', 'advanced_box_score']
        ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']
        
        df_players_totals = get_players_stats(2022,'totals')
        df_players_advanced = get_players_stats(2022,'advanced')
        
        df_players = pd.concat([df_players_totals, df_players_advanced['PER']], axis=1)
        st.session_state.df_players = df_players
    
    page = st.sidebar.selectbox(
        "Navegador de paginas:",
        [
            "Home",
            "Players - EDA",
            "Players - Scouting",
            "Teams - EDA"
        ]
    )
    
    if page == "Home": 
        st.title("HOME.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
        # teams_stats()

    #Second Page
    if page == "Players - EDA":
        st.title("Players - EDA.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
        # players_stats()
        f01.players_eda()

    if page == "Players - Scouting":
        st.title("Players - Scouting.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
   
    if page == "Teams - EDA":
        st.title("Teams - EDA.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
        
        f01.teams_eda()
