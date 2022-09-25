
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

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}


def main():
    st.title("PRACTICAS CON STREAMLIT Y NBA_API")
    st.write("- Recuperar los datos y estadisticas de TEAMS y PLAYERS.")
    st.write("- Los datos se obtienen en diferentes dimensiones y tipos debido a los metodos de la APi.")
    
    my_bar = st.progress(0)

    for percent_complete in range(30):
         time.sleep(0.1)
         my_bar.progress(percent_complete + 1)
    
    with st.spinner('Wait for it...'):
        time.sleep(3)
    
    # Pinta un Spinner de carga mientras se esta ejecutando el "for", una vez termina el for desaparece y pasa a la siguiente instrucción..
    with st.spinner('Wait for it2...'):
        for percent_complete2 in range(30):
            #st.spinner('Wait for it2...')
            time.sleep(0.1)
            #my_bar.progress(percent_complete + 1)
            percent_complete2 += 1


def teams_stats():
    # Estadisticas generales por equipos en la tempRegular actual..
    time.sleep(1)
    df_teams = pd.DataFrame(endpoints.LeagueDashTeamStats(proxy='127.0.0.1:80', headers=custom_headers, timeout=50).get_data_frames()[0])
    # time.sleep(1)
    # df_teams = pd.DataFrame(data_teams[0])

    st.markdown("ESTADISTICAS POR EQUIPOS - Temporada Regular (21/22).")
    st.write(df_teams)

def players_stats():

    time.sleep(1)
    df_players = pd.DataFrame(endpoints.LeagueDashPlayerStats(proxy='127.0.0.1:80', headers=custom_headers, timeout=50).get_data_frames()[0])
    # time.sleep(1)
    # df_players = pd.DataFrame(data_players[0])

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
