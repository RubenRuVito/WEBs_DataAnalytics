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
