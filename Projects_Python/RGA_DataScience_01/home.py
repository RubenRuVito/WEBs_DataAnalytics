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





if __name__ == "__main__":
        
    st.set_page_config(layout="wide") # NO se puede configurar este parametro varias veces..solo una.
    # main()
    
    page = st.sidebar.selectbox(
        "Navegador de paginas:",
        [
            "Home",
            "Players - EDA",
            "Players - Scouting"
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

    if page == "Players - Scouting":
        st.title("Players - Scouting.")
        st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
        st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
    
