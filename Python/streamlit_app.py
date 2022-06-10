# CRear estructura de proyecto Streamlit
# https://github.com/arnaudmiribel/st
# dentro de la carpeta principal "$ st"
# $ streamlit run myapp.py
# $ conda list -e > requirements.txt # te incluye todas las librerias del entorno global..
# $ pip freeze > requirements.txt

# Crear requirements.txt automaticamente.
# pip install pipreqs
# $ pipreqs [options "--force"] [path_folder_project] crea el requirements.txt en función de las librerias utilizadas en los scripts

# Si al copiar y pegar codigo, existieran problemas de "identation"
# Ctrl+Shift+P or View->Command Palette.
# Type
# >Convert Indentation to Spaces

# Ejemplo de streamlit con varias paginas, seleccionadas a partir de un combo...
# https://pythonwife.com/matplotlib-with-streamlit/

# Un buen ejemplo de EDA de conjuntos de datos..
# https://github.com/anarabiyev/EDA_Streamlit_App

# Cosas sobre "iplot()", pckages plotly & Cufflinks
# https://analyticsindiamag.com/beginners-guide-to-data-visualisation-with-plotly-cufflinks/

"""
## App: Iris EDA App
Author: [Jesse E.Agbe(JCharis)](https://github.com/Jcharis))\n
Source: [Github](https://github.com/Jcharis/Machine-Learning-Web-Apps/tree/master/Iris_EDA_Web_App)
Credits: Streamlit Team,Marc Skov Madsen(For Awesome-streamlit gallery)
Description
This is a simple Exploratory Data Analysis of the Iris Dataset depicting the various 
species built with Streamlit.
We can preview the dataset,column names as well as show some basic plot with matplotlib and
seaborn.
There is also an image manipulation of a specie with changeable contrast and width using st.slider()
Purpose
To show a simple EDA of Iris using Streamlit framework. 
"""
from pickle import TRUE
from turtle import width
from urllib.request import urlopen
import streamlit as st

# EDA Pkgs
import pandas as pd
import numpy as np
import os

# Plotting & data Pkgs
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as pgo
import plotly.graph_objs as pgo2
import seaborn as sns
from PIL import Image,ImageFilter,ImageEnhance
from sklearn import datasets
import cufflinks as cf
from urllib.request import urlopen
import json


#def main():
def homepage():
    st.title("🎈 My new app!")
    st.write("Welcome to your new app. Have fun editing it")
    st.balloons()
    
    st.title("Iris EDA App")
    st.subheader("EDA Web App with Streamlit ")
    st.markdown("""
        #### Description
        + This is a simple Exploratory Data Analysis  of the Iris Dataset depicting the various species built with Streamlit.
        #### Purpose
        + To show a simple EDA of Iris using Streamlit framework. 
        """)

    # Your code goes below
    # Our Dataset
    my_dataset = "iris.csv"

    # To Improve speed and cache data
    # @st.cache(persist=True)
    def explore_data(dataset):
        #df = pd.read_csv(os.path.join(dataset))
        #df = sns.data_load('iris')
        iris_data = sns.load_dataset('iris')
        return pd.DataFrame(iris_data)
        #return df 

    # Load Our Dataset
    data = explore_data(my_dataset)

    # Show Dataset
    if st.checkbox("Preview DataFrame"):
        if st.button("Head"):
            st.write(data.head())
        if st.button("Tail"):
            st.write(data.tail())
        else:
            st.write(data.head(2))

    # Show Entire Dataframe
    if st.checkbox("Show All DataFrame"):
        st.dataframe(data)

    # Show All Column Names
    if st.checkbox("Show All Column Name"):
        st.text("Columns:")
        st.write(data.columns)

    # Show Dimensions and Shape of Dataset
    data_dim = st.radio('What Dimension Do You Want to Show',('Rows','Columns'))
    if data_dim == 'Rows':
        st.text("Showing Length of Rows")
        st.write(len(data))
    if data_dim == 'Columns':
        st.text("Showing Length of Columns")
        st.write(data.shape[1])

    # Show Summary of Dataset
    if st.checkbox("Show Summary of Dataset"):
        st.write(data.describe())

    # Selection of Columns
    species_option = st.selectbox('Select Columns',('sepal_length','sepal_width','petal_length','petal_width','species'))
    if species_option == 'sepal_length':
        st.write(data['sepal_length'])
    elif species_option == 'sepal_width':
        st.write(data['sepal_width'])
    elif species_option == 'petal_length':
        st.write(data['petal_length'])
    elif species_option == 'petal_width':
        st.write(data['petal_width'])
    elif species_option == 'species':
        st.write(data['species'])
    else:
        st.write("Select A Column")

    # Show Plots
    fig, ax = plt.subplots(figsize=(7,5))

    if st.checkbox("Simple Bar Plot with Matplotlib "):
        data.plot(kind='bar')
        #ax.bar(data['petal_length'], data['petal_width'])
        ax.bar(data, height=data['species'])
        st.pyplot(fig)

    # Show Correlation Plots
    if st.checkbox("Simple Correlation Plot with Matplotlib "):
        plt.matshow(data.corr())
        st.pyplot()

    # Show Correlation Plots with Sns
    if st.checkbox("Simple Correlation Plot with Seaborn "):
        st.write(sns.heatmap(data.corr(),annot=True))
        # Use Matplotlib to render seaborn
        st.pyplot()

    # Show Plots
    if st.checkbox("Bar Plot of Groups or Counts"):
        v_counts = data.groupby('species')
        st.bar_chart(v_counts)


    # Iris Image Manipulation
    # @st.cache
    def load_image(img):
        im =Image.open(os.path.join(img))
        return im

    # Select Image Type using Radio Button
    species_type = st.radio('What is the Iris Species do you want to see?',('Setosa','Versicolor','Virginica'))

    if species_type == 'Setosa':
        st.text("Showing Setosa Species")
        st.image(load_image('imgs/iris_setosa.jpg'))
    elif species_type == 'Versicolor':
        st.text("Showing Versicolor Species")
        st.image(load_image('imgs/iris_versicolor.jpg'))
    elif species_type == 'Virginica':
        st.text("Showing Virginica Species")
        st.image(load_image('imgs/iris_virginica.jpg'))



    # Show Image or Hide Image with Checkbox
    if st.checkbox("Show Image/Hide Image"):
        my_image = load_image('iris_setosa.jpg')
        enh = ImageEnhance.Contrast(my_image)
        num = st.slider("Set Your Contrast Number",1.0,3.0)
        img_width = st.slider("Set Image Width",300,500)
        st.image(enh.enhance(num),width=img_width)


    # About
    if st.button("About App"):
        st.subheader("Iris Dataset EDA App")
        st.text("Built with Streamlit")
        st.text("Thanks to the Streamlit Team Amazing Work")

    if st.checkbox("By"):
        st.text("Jesse E.Agbe(JCharis)")
        st.text("Jesus Saves@JCharisTech")

def dashboard_wines():

    ####### Load Dataset #####################

    #wine = datasets.load_wine()
    wine = datasets.load_wine()

    wine_df = pd.DataFrame(data=wine.data, columns=wine.feature_names)
    
    wine_df["WineType"] = [wine.target_names[t] for t in wine.target ]

    #st.set_page_config(layout="wide")

    st.markdown("## Wine Dataset Analysis")   ## Main Title

    ################# Scatter Chart Logic #################

    st.sidebar.markdown("### Scatter Chart: Explore Relationship Between Ingredients :")

    ingredients = wine_df.drop(labels=["WineType"], axis=1).columns.tolist()

    x_axis = st.sidebar.selectbox("X-Axis", ingredients)
    y_axis = st.sidebar.selectbox("Y-Axis", ingredients, index=1)

    if x_axis and y_axis:
        scatter_fig = wine_df.iplot(kind="scatter", x=x_axis, y=y_axis,
                        mode="markers",
                        categories="WineType",
                        asFigure=True, opacity=1.0,
                        xTitle=x_axis.replace("_"," ").capitalize(), yTitle=y_axis.replace("_"," ").capitalize(),
                        title="{} vs {}".format(x_axis.replace("_"," ").capitalize(), y_axis.replace("_"," ").capitalize()),
                        )

    ########## Bar Chart Logic ##################

    st.sidebar.markdown("### Bar Chart: Average Ingredients Per Wine Type : ")

    avg_wine_df = wine_df.groupby(by=["WineType"]).mean()

    bar_axis = st.sidebar.multiselect(label="Bar Chart Ingredient", options=avg_wine_df.columns.tolist(), default=["alcohol","malic_acid"])

    if bar_axis:
        bar_fig = avg_wine_df[bar_axis].iplot(kind="bar",
                            barmode="stack",
                            xTitle="Wine Type",
                            title="Distribution of Average Ingredients Per Wine Type",
                            asFigure=True,
                            opacity=1.0,
                            );
    else:
        bar_fig = avg_wine_df[["alcohol"]].iplot(kind="bar",
                            barmode="stack",
                            xTitle="Wine Type",
                            title="Distribution of Average Alcohol Per Wine Type",
                            asFigure=True,
                            opacity=1.0,
                            );

    ################# Histogram Logic ########################

    st.sidebar.markdown("### Histogram: Explore Distribution of Ingredients : ")

    hist_axis = st.sidebar.multiselect(label="Histogram Ingredient", options=ingredients, default=["malic_acid"])
    bins = st.sidebar.radio(label="Bins :", options=[10,20,30,40,50], index=1)

    if hist_axis:
        hist_fig = wine_df.iplot(kind="hist",
                                keys=hist_axis,
                                xTitle="Ingredients",
                                bins=bins,
                                title="Distribution of Ingredients",
                                asFigure=True,
                                opacity=1.0
                                );
    else:
        hist_fig = wine_df.iplot(kind="hist",
                                keys=["alcohol"],
                                xTitle="Alcohol",
                                bins=bins,
                                title="Distribution of Alcohol",
                                asFigure=True,
                                opacity=1.0
                                );


    #################### Pie Chart Logic ##################################

    wine_cnt = wine_df.groupby(by=["WineType"]).count()[['alcohol']].rename(columns={"alcohol":"Count"}).reset_index()

    pie_fig = wine_cnt.iplot(kind="pie", labels="WineType", values="Count",
                            title="Wine Samples Distribution Per WineType",
                            hole=0.4,
                            asFigure=True)


    ##################### Layout Application ##################

    container1 = st.container()
    col1, col2 = st.columns(2)

    with container1:
        with col1:
            scatter_fig
        with col2:
            bar_fig


    container2 = st.container()
    col3, col4 = st.columns(2)

    with container2:
        with col3:
            hist_fig
        with col4:
            pie_fig

def change_size_plots():

# https://plotly.com/python/setting-graph-size/
# https://github.com/databyjp # PUTO GENIO!!!
# https://coderzcolumn.com/tutorials/data-science/how-to-plot-radar-charts-in-python-plotly

    st.markdown("### Gráfica tamaño dinamico & Grafico de Radar")
    # ----------------- Iputs Usuario --------------
    width = st.sidebar.slider("plot width", 100, 1000, 500)
    height = st.sidebar.slider("plot height", 100, 1000, 300)

    # ----------------- Datos ----------------------
    df_data = sns.load_dataset("iris")
    df_data2 = pd.DataFrame(data=datasets.load_wine().data, columns=datasets.load_wine().feature_names)
    # Del objeto de datos "datasets.load_wine()", utilizamos las propiedades "target_names" y "target", para crear la columna
    # "wineType", que es la clase de vino a la que pertenece cada muestra...
    df_data2["WineType"] = [datasets.load_wine().target_names[t] for t in datasets.load_wine().target]

    # Agrupamos por tipo de vino, y obtenemos la media aritmetica o promedio de cada variable/atributo/propiedad (columna), 
    # para cada clase de vino..en un objeto de tipo Dframe
    df_avg_winetype = df_data2.groupby("WineType").mean()
    # -----------------------------------------------
    
    # ------------- Estructurando el Layout ---------
    container1 = st.container()
    col1, col2 = st.columns(2)
    
    with container1:
        with col1:
            st.markdown("Data frame Iris (seaborne).")
            st.write(df_data)
        with col2:
            st.markdown("Data Wines (sklearn.datasets) - Transform in DFrame.")
            st.write(df_data2)

    # --------- Objeto Grafica 1 ----------
    # Preparando datos y parametrizaciones para el objeto de la grafica 1, dinamizando el tamaño..
    #fig = plt.subplots(figsize=(width, height))
    fig = px.scatter(data_frame=df_data, x = "sepal_length", y = "sepal_width", color = "species", width=width, height=height)
    #fig.update_layout()
    #ax.plot(datasets.load_iris())
    #sns.FacetGrid(data, hue ="species", height = 6).map(plt.scatter, 'sepal_length','petal_length').add_legend()
    #ax.legend()
    # -------------------------------------

    # --------- Objeto Grafica 2 ----------
    # Preparando datos y parametrizaciones para el objeto de la grafica 2, 
    # Pruebas
    #st.write(range(len(df_data2["WineType"].unique())-1))
    #st.write(range(3))
    st.write("Dataframe Medias aritmeticas - raw")
    st.write(df_avg_winetype)
    #st.write(type(avg_winetype))
    #st.write(avg_winetype.iloc[0].values)

    # Normalizamos el dataframe de medias..
    # df_avg_typewine_norm = (df_avg_winetype - df_avg_winetype.min()) / ( df_avg_winetype.max() - df_avg_winetype.min()) # Por MIN y MAX
    df_avg_typewine_norm = df_avg_winetype.apply(lambda x: (x-x.mean())/ x.std(), axis=0) # Por media y desviacion stndard
    st.write("Dataframe Normalizado(mean&std) - Para la visualizacion de la grafica de radar.")
    st.write(df_avg_typewine_norm)

    fig2 = pgo.Figure()
    
    for ind in range(len(df_data2["WineType"].unique())):
        st.write(ind)
        fig2.add_trace(pgo.Scatterpolar(r=df_avg_typewine_norm.iloc[ind].values,
                                        theta=df_avg_typewine_norm.columns,
                                        fill='toself',
                                        #name="TypeWine-%s"%datasets.load_wine().target_names[ind],
                                        name="TypeWine-%s"%df_avg_winetype.index[ind], # Recupera los rownames del dataframe..
                                        showlegend=True,)
                                        )
    
    fig2.update_layout(polar=dict(radialaxis=dict(visible=True,
                                                  range=[-1.5, 1.5])
                                 ),
                                 title="Propiedades de clases de vino."
                        )
    # -----------------------------

    # ------------- Estructurando el Layout ---------
    container2 = st.container()
    col3, col4 = st.columns(2)

    with container2:
        with col3:
            st.plotly_chart(fig)
        with col4:
            #fig2.show()
            st.plotly_chart(fig2)
    
    #data2 = sns.load_dataset("wine")
    #st.write(data2)
    # datasets.load_wine()
    
def graficas_animadas():

    df = px.data.gapminder()

    st.write(df)

    year_options = df['year'].unique().tolist()
    year = st.selectbox('Que año quiere ver:', year_options, 0)
    #df = df[df['year']==year]

    fig3 = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="continent",
                     log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90],
                     animation_frame="year", animation_group="country") # Estas 2 parametrizaciones dinamizan el grafico

    fig3.update_layout(height=500, width=1200)
    st.write(fig3)

    df_covid = pd.read_csv("https://raw.githubusercontent.com/shinokada/covid-19-stats/master/data/daily-new-confirmed-cases-of-covid-19-tests-per-case.csv")
    df_covid.columns = ["Country","Code","Date","Confirmed","Days since confirmed"]
    df_covid["Date"] = pd.to_datetime(df_covid['Date']).dt.strftime('%Y-%m-%d')
    country_options = df_covid['Country'].unique().tolist()

    st.write(df_covid)

    date_options = df_covid['Date'].unique().tolist()
    date = st.selectbox('Que fecha quiere ver:', date_options, 100)
    country = st.multiselect('Que cntry quiere ver:', country_options, ['Brazil'])

    df_covid = df_covid[df_covid['Country'].isin(country)]
    #df_covid = df_covid[df_covid['Date']==date]

    fig4 = px.bar(df_covid, x="Country", y="Confirmed", color="Country", range_y=[0,35000],
                  animation_frame="Date", animation_group="Country")

    #fig4.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
    #fig4.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

    fig4.update_layout(height=500, width=1200)

    st.write(fig4)


def html_inyections():

    st.markdown("""
                <div class="waveWrapper waveAnimation">
                <div class="waveWrapperInner bgTop">
                    <div class="wave waveTop" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-top.png')"></div>
                </div>
                <div class="waveWrapperInner bgMiddle">
                    <div class="wave waveMiddle" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-mid.png')"></div>
                </div>
                <div class="waveWrapperInner bgBottom">
                    <div class="wave waveBottom" style="background-image: url('http://front-end-noobs.com/jecko/img/wave-bot.png')"></div>
                </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("## Main KPIs")

    # Fisrst row / container..

    first_kpi, second_kpi, third_kpi = st.columns(3)

    with first_kpi:
        st.markdown("**First KPI**")
        number1 = 111 
        st.write(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)
    
    with second_kpi:
        st.markdown("**Second KPI**")
        number2 = 222 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

    with third_kpi:
        st.markdown("**Third KPI**")
        cont1 = st.container()
        with cont1:
            number3 = 331 
            st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)
        with cont1:
            number4 = 332 
            st.markdown(f"<h1 style='text-align: center; color: red;'>{number4}</h1>", unsafe_allow_html=True)

    ### second row / Container

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown("## Secondary KPIs")

    first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi = st.columns(6)

    with first_kpi:
        st.markdown("**First KPI**")
        number1 = 111 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

    with second_kpi:
        st.markdown("**Second KPI**")
        number2 = 222 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

    with third_kpi:
        st.markdown("**Third KPI**")
        number3 = 333 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

    with fourth_kpi:
        st.markdown("**First KPI**")
        number1 = 111 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

    with fifth_kpi:
        st.markdown("**Second KPI**")
        number2 = 222 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

    with sixth_kpi:
        st.markdown("**Third KPI**")
        number3 = 333 
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Charts Sections..

    st.markdown("## Chart Section: 1")

    first_chart, second_chart = st.columns(2)

    with first_chart:
        chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)

    with second_chart:
        chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)

    st.markdown("## Chart Section: 2")

    first_chart, second_chart = st.columns(2)

    with first_chart:
        chart_data = pd.DataFrame(np.random.randn(100, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)

    with second_chart:
        chart_data = pd.DataFrame(np.random.randn(2000, 3),columns=['a', 'b', 'c'])
        st.line_chart(chart_data)


def graficas_variadas():
    
    fig = px.scatter(pd.DataFrame(sns.load_dataset('iris')), x='sepal_width', y='sepal_length', color='species',
                     size='petal_length', hover_data=['petal_width'])
    
    st.plotly_chart(fig)

    # df = px.data.gapminder().query("continent == 'Europe")
    fig = px.line(px.data.gapminder().query("continent == 'Europe'"), x='year', y='lifeExp', color='country')
    # https://plotly.com/python/figure-labels/
    fig.update_layout(width=1200, height=500, font=dict(size=19)) # "Font" Cambia el tamaño de la legenda..
    st.plotly_chart(fig)

    fig = pgo.Figure(data=pgo.Scatter(x=[1,2,3,4], y=[10,11,12,13], mode='markers', marker=dict(size=[40,60,80,100],
                                                                                               color=[1,2,3,4])))
    st.plotly_chart(fig)

    # Interesante hacer un analisis de los datos recuperados, y ver como tienen que estar estructurados para
    # pasarselos a las funciones de PLOTLY...
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    
    df_fips_counties = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})
    
    # fig = plt.figure(figsize=(12,8))
    fig = px.choropleth_mapbox(df_fips_counties, geojson=counties, locations='fips',color='unemp',
                               color_continuous_scale='Viridis',
                               range_color=(0,12),
                               mapbox_style='carto-positron',
                               zoom=3.5, center={"lat":37.0902, "lon":-95.7129},
                               labels={"unemp":"unemployment rate"})
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, width=1200, height=500)
    st.plotly_chart(fig)


    fig = pgo.Figure()

    fig.add_trace(pgo.Scatter(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        name="Name of Trace 1"       # this sets its legend entry
    ))


    fig.add_trace(pgo.Scatter(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
        name="Name of Trace 2"
    ))

    fig.add_trace(pgo.Bar(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[1, 0, 3, 2, 5, 4, 7, 6, 8],
        name="Name of Trace 2"
    ))

    fig.update_layout(
        title="Plot Title",
        xaxis_title="X Axis Title",
        yaxis_title="Y Axis Title",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        height=600, 
        width=1000
    )

    #fig.show()
    st.plotly_chart(fig)



if __name__ == "__main__":
    # main()

    st.set_page_config(layout="wide") # Configuración de tipo de pagina a visualizar (Solo se puede parametrizar una vez)

    page = st.sidebar.selectbox(
        "Navegador de paginas:",
        [
            "Pagina principal",
            "Dashboard Wines",
            "Graficas dinamicas & Radar",
            "Graficas Animadas",
            "HTML Inyecton",
            "Graficas variadas"
            #"Horizontal Bar Graph",
            #"Scatter Plot",
            #"Histogram",
            #"Pie Chart",
            #"Sub Plot"
        ]
    )

    #First Page
    if page == "Pagina principal":
        # st.set_page_config(layout="centered") # NO se puede configurar este parametro varias veces..solo una.
        homepage()

    #Second Page
    if page == "Dashboard Wines":
        # st.set_page_config(layout="wide")
        dashboard_wines()
    
    if page == "Graficas dinamicas & Radar":
        change_size_plots()

    if page == "Graficas Animadas":
        graficas_animadas()
    
    if page == "HTML Inyecton":
        html_inyections()
    
    if page == "Graficas variadas":
        graficas_variadas()

