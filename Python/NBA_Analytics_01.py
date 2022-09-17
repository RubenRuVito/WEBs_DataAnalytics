"""
## App: NBA EDA App
## Autor: RGA
Description
- EDA sobre estadisticas avanzadas de la NBA
- "basketball_reference_scraper" API para recuperar los conjuntos de datos
"""
import streamlit as st

# EDA Pkgs
import pandas as pd
import numpy as np
import os
from os import remove
import base64
from lxml import etree

# Plotting Pkgs
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image,ImageFilter,ImageEnhance

# Api Data NBA
# from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc

# Funciones y variables para scrappear datos..

BASE_URL = 'https://www.basketball-reference.com/'
STAT_TYPES = ['per_game', 'totals', 'per_minute', 'advanced', 'per_poss', 'play-by-play', 'advanced_box_score']
ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']

#@cache
def get_players_stats(season: int, stat_type: str, header: int = 0, filter_games=True, remove_duplicates=True):
	
	url = f'{BASE_URL}leagues/NBA_{str(season)}_{stat_type}.html'
	print(f'GET {url}')
	html = pd.read_html(url, header = header)
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

# https://www.basketball-reference.com/leagues/NBA_2022_ratings.html#ratings
def get_teams_stats(season: int, stat_type: str, header: int = 1, filter_games=True, remove_duplicates=True):
	
	url = f'{BASE_URL}leagues/NBA_{str(season)}_{stat_type}.html#ratings'
	print(f'GET {url}')
	html = pd.read_html(url, header = header)
	df = html[0]
	
	return df
	

def main():
	st.title("NBA EDA App")
	st.subheader("EDA Web App with Streamlit ")
	st.markdown("""
		#### Description
		+ This is a simple Exploratory Data Analysis of the NBA tables stats built with Streamlit.
		#### Purpose
		+ To show a simple EDA of NBA using Streamlit framework. 
		""")

	# Your code goes below
	# Our Dataset
	my_dataset = "iris.csv"

	# To Improve speed and cache data
	@st.cache(persist=True)
	# def data_teams_misc(year):
	# 	#df = pd.read_csv(os.path.join(dataset))
	# 	#df = sns.data_load('iris')
	# 	#df_teams = get_team_misc('GSW',year)
	# 	playerstats = load_data(selected_year, selected_stat)
	# 	return pd.DataFrame(df_teams)
	
	def data_teams(year: int, stats_type: str):
		df_teams_stats = get_teams_stats(year, stats_type)
		return pd.DataFrame(df_teams_stats)
	
	def data_players(year: int, stats_type: str):
		df_players_stats = get_players_stats(year, stats_type)
		return pd.DataFrame(df_players_stats)

	# Load Our Dataset
	#df = data_teams_misc(2022)
	df_teams = data_teams(2022, 'ratings')
	df = data_players(2022, 'totals')
	df2 = data_players(2022, 'advanced')
	
	st.markdown(""" ## TEAMS - Stats Ratings: """)
	
	# Show Dataset Teams
	if st.checkbox("Preview DataFrame Teams"):
		if st.button("Head"):
			st.write(df_teams.head())
		if st.button("Tail"):
			st.write(df_teams.tail())
		else:
			st.write(df_teams.head(2))
			
	# Show Entire Dataframe
	if st.checkbox("Show All DataFrame Teams"):
		st.dataframe(df_teams)

	# Show All Column Names
	if st.checkbox("Show All Column Name Teams"):
		st.text("Columns:")
		st.write(df_teams.columns)

	# Show Dimensions and Shape of Dataset
	data_dim_teams = st.radio('What Dimension Do You Want to Show Teams',('Rowst','Columnst'))
	if data_dim_teams == 'Rowst':
		st.text("Showing Length of Rows")
		st.write(len(df_teams))
	if data_dim_teams == 'Columnst':
		st.text("Showing Length of Columns")
		st.write(df_teams.shape[1])

	# Show Summary of Dataset
	if st.checkbox("Show Summary of Dataset Teams"):
		st.write(df_teams.describe())

# --------------------------
	st.markdown(""" ## PLAYERS - Stats Totals: """)
	
	# Show Dataset Players
	if st.checkbox("Preview DataFrame Players"):
		if st.button("Head"):
			st.write(df.head())
		if st.button("Tail"):
			st.write(df.tail())
		else:
			st.write(df.head(2))

	# Show Entire Dataframe
	if st.checkbox("Show All DataFrame Players"):
		st.dataframe(df)

	# Show All Column Names
	if st.checkbox("Show All Column Name Players"):
		st.text("Columns:")
		st.write(df.columns)

	# Show Dimensions and Shape of Dataset
	data_dim = st.radio('What Dimension Do You Want to Show',('Rows','Columns'))
	if data_dim == 'Rows':
		st.text("Showing Length of Rows")
		st.write(len(df))
	if data_dim == 'Columns':
		st.text("Showing Length of Columns")
		st.write(df.shape[1])

	# Show Summary of Dataset
	if st.checkbox("Show Summary of Dataset Players"):
		st.write(df.describe())
		
 # --------------------------
	st.markdown(""" ## PLAYERS - Stats ADVANCED: """)
	
	# Show Dataset Players
	if st.checkbox("Preview DataFrame Players 2"):
		if st.button("Head"):
			st.write(df2.head())
		if st.button("Tail"):
			st.write(df2.tail())
		else:
			st.write(df2.head(2))

	# Show Entire Dataframe
	if st.checkbox("Show All DataFrame Players 2"):
		st.dataframe(df2)

	# Show All Column Names
	if st.checkbox("Show All Column Name Players 2"):
		st.text("Columns:")
		st.write(df2.columns)

	# Show Dimensions and Shape of Dataset
	data_dim = st.radio('What Dimension Do You Want to Show 2',('Rows','Columns'))
	if data_dim == 'Rows':
		st.text("Showing Length of Rows")
		st.write(len(df2))
	if data_dim == 'Columns':
		st.text("Showing Length of Columns")
		st.write(df2.shape[1])

	# Show Summary of Dataset
	if st.checkbox("Show Summary of Dataset Players 2"):
		st.write(df2.describe())

# Selection of Columns
#    species_option = st.selectbox('Select Columns',('W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'eFG%', 'TOV%', 'ORB%', 
# 'FT/FGA', 'eFG%', 'TOV%', 'DRB%', 'FT/FGA', 'Arena', 'Attendance'))
#   if species_option == 'sepal_length':
#    	st.write(df['sepal_length'])
#    elif species_option == 'sepal_width':
#    	st.write(df['sepal_width'])
#    elif species_option == 'petal_length':
#    	st.write(df['petal_length'])
#    elif species_option == 'petal_width':
#   	st.write(df['petal_width'])
#    elif species_option == 'species':
#    	st.write(df['species'])
#    else:
#    	st.write("Select A Column")

	# Show Plots
	if st.checkbox("Simple Bar Plot with Matplotlib "):
		df.plot(kind='bar')
		st.pyplot()

	# Show Correlation Plots
	if st.checkbox("Simple Correlation Plot with Matplotlib "):
		plt.matshow(df.corr())
		st.pyplot()

	# Show Correlation Plots with Sns
	if st.checkbox("Simple Correlation Plot with Seaborn "):
		st.write(sns.heatmap(df.corr(),annot=True))
		# Use Matplotlib to render seaborn
		st.pyplot()
	
	if st.checkbox("Correlations by RGA"):
		corr = df.corr()
		mask = np.zeros_like(corr)
		mask[np.triu_indices_from(mask)] = True
		with sns.axes_style("white"):
			f, ax = plt.subplots(figsize=(7, 5))
			ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
			st.pyplot(f)

	# Show Plots
	if st.checkbox("Bar Plot of Groups or Counts"):
		v_counts = df.groupby('')
		st.bar_chart(v_counts)

	# Iris Image Manipulation
#    @st.cache
#    def load_image(img):
#    	im =Image.open(os.path.join(img))
#    	return im

	# Select Image Type using Radio Button
 #   species_type = st.radio('What is the Iris Species do you want to see?',('Setosa','Versicolor','Virginica'))

#    if species_type == 'Setosa':
#    	st.text("Showing Setosa Species")
#    	st.image(load_image('imgs/iris_setosa.jpg'))
#    elif species_type == 'Versicolor':
#    	st.text("Showing Versicolor Species")
#    	st.image(load_image('imgs/iris_versicolor.jpg'))
#    elif species_type == 'Virginica':
#    	st.text("Showing Virginica Species")
#    	st.image(load_image('imgs/iris_virginica.jpg'))

# 	Show Image or Hide Image with Checkbox
#    if st.checkbox("Show Image/Hide Image"):
#    	my_image = load_image('iris_setosa.jpg')
#    	enh = ImageEnhance.Contrast(my_image)
#    	num = st.slider("Set Your Contrast Number",1.0,3.0)
#    	img_width = st.slider("Set Image Width",300,500)
#    	st.image(enh.enhance(num),width=img_width)

	# About
	if st.button("About App"):
		st.subheader("Iris Dataset EDA App")
		st.text("Built with Streamlit")
		st.text("Thanks to the Streamlit Team Amazing Work")

	if st.checkbox("By"):
		st.text("Jesse E.Agbe(JCharis)")
		st.text("Jesus Saves@JCharisTech")

if __name__ == "__main__":
	main()

