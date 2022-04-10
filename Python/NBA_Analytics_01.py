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

# Plotting Pkgs
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image,ImageFilter,ImageEnhance

# Api Data NBA
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc

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
    def data_teams_misc(year):
    	#df = pd.read_csv(os.path.join(dataset))
        #df = sns.data_load('iris')
        df_teams = get_team_misc('',year)
        return pd.DataFrame(df_teams)
    	

    # Load Our Dataset
    df = data_teams_misc(2022)

    # Show Dataset
    if st.checkbox("Preview DataFrame"):
    	if st.button("Head"):
    		st.write(df.head())
    	if st.button("Tail"):
    		st.write(df.tail())
    	else:
    		st.write(df.head(2))

    # Show Entire Dataframe
    if st.checkbox("Show All DataFrame"):
    	st.dataframe(df)

    # Show All Column Names
    if st.checkbox("Show All Column Name"):
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
    if st.checkbox("Show Summary of Dataset"):
    	st.write(df.describe())

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



    # Show Image or Hide Image with Checkbox
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
