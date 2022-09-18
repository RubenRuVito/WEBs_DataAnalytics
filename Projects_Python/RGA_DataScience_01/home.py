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

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


if __name__ == "__main__":
        
    st.set_page_config(layout="wide") # NO se puede configurar este parametro varias veces..solo una.
    # main()

    my_logo = add_logo(logo_path="Projects_Python/RGA_DataScience_01/image/Nba_logo_PNG3-1.png", width=160, height=80)
    st.sidebar.image(my_logo)

    st.sidebar.markdown("<h2 style='text-align: left; color: white; font-family:commanders'>SPORTS ANALYTICS.</h2>",unsafe_allow_html=True)

    st.session_state.temporada = st.sidebar.selectbox('Temporada',('2022-23','2021-22','2020-21'))

    page = st.sidebar.selectbox(
        "Navegador de paginas:",
        [
            "Intro. 'Sports Analytics'.",
            "Equipos - Stats.",
            "Jugadores - Stats.",
            "Comparando Equipos.",
            "Comparando Jugadores.",
            "Jugadores - Scouting.",
            "Estadísticas Historicas."
        ]
    )
    
    if page == "Intro. 'Sports Analytics'.": 
        st.title("Introducción al análisis de datos deportivos.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
        # teams_stats()

    #Second Page
    if page == "Equipos - Stats.":
        st.title("Estadisticas Equipos.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")

        f01.teams_stats()
    
    if page == "Comparando Equipos.":
        st.title("Análisis gráficos de comparación de las medidas de cada Equipo.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")

        f01.teams_stats_compare()

    if page == "Jugadores - Stats.":
        st.title("Players - Stats.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")

        f01.players_stats()

    if page == "Comparando Jugadores.":
        st.title("Análisis gráficos de comparación de las medidas de cada Jugador.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")

        f01.players_stats_compare()

    if page == "Jugadores - Scouting.":
        st.title("Análisis de Jugadores con tñecnocas de Machine Learning")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
        
    if page == "Análisis Historicos.":
        st.title("Análisis de los datos generados por la NBA a lo largo de su historia.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
