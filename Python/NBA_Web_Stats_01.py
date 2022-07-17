
# PRACTICAS CON STREAMLIT Y NBA_API

# Importando librerias
import streamlit as st
import nba_api
import pandas as pd
import numpy as np
import time
# from sklearn import linear_model
import requests
from matplotlib import pyplot as plt
from nba_api.stats import endpoints
from nba_api.stats.static import players
from nba_api.stats.static import teams


def main():
    st.title("PRACTICAS CON STREAMLIT Y NBA_API")
    st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
    st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
    
    my_bar = st.progress(0)

    for percent_complete in range(100):
         time.sleep(0.1)
         my_bar.progress(percent_complete + 1)


def teams_stats():
    # Estadisticas generales por equipos en la tempRegular actual..
    data_teams = endpoints.LeagueDashTeamStats(timeout=600).get_data_frames()
    df_teams = pd.DataFrame(data_teams[0])

    st.markdown("ESTADISTICAS POR EQUIPOS - Temporada Regular (21/22).")
    st.write(df_teams)

def players_stats():

    data_players = endpoints.leaguedashplayerstats.LeagueDashPlayerStats(timeout=600).get_data_frames()
    df_players = pd.DataFrame(data_players[0])

    st.markdown("ESTADISTICAS POR JUGADORES - Temporada Regular (21/22).")
    st.write(df_players)


if __name__ == "__main__":
    
    st.set_page_config(layout="wide") # Configuración de tipo de pagina a visualizar (Solo se puede parametrizar una vez)

    main()

    page = st.sidebar.selectbox(
        "Navegador de paginas:",
        [
            "TEAMS.",
            "PLAYERS."
        ]
    )

    #First Page
    if page == "TEAMS.":
        # st.set_page_config(layout="centered") # NO se puede configurar este parametro varias veces..solo una.
        teams_stats()

    #Second Page
    if page == "PLAYERS.":
        # st.set_page_config(layout="wide")
        players_stats()
