import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px
import tensorflow as tf
from tensorflow import keras

# Read data
@st.cache
def load_data():
    # return pd.read_csv('https://gist/..../iris.csv')
    iris_data = sns.load_dataset('iris')
    return pd.DataFrame(iris_data)
df = load_data()

# scaler will be used to scale user input.
@st.cache
def get_scaler():
    # Clean data
    X = df.iloc[:, :4]
    y = np.zeros(shape=(X.shape[0], 3))

    for i, val in enumerate(df['species']):
        if val=='virginica':
            y[i,:] = np.array([1, 0, 0])
        elif val=='versicolor':
            y[i,:] = np.array([0, 1, 0])
        elif val=='setosa':
            y[i,:] = np.array([0, 0, 1])
            
    X_train, Y_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    
    # Create Model
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(512, activation=tf.nn.relu),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(10, activation='sigmoid')
    ])
    #model.compile(optimizer='adam',
    #              loss='categorical_crossentropy',
    #              metrics=['accuracy'])
    
    opt = keras.optimizers.Adam(learning_rate=0.01)
    model.compile(optimizer=opt, loss='categorical_crossentropy')

    model.fit(X_train, y_train, epochs=50)
    
    # Scale data
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler, model

scaler, model = get_scaler()

# Load model
#model = keras.models.load_model(iris_model)

# App title and description
st.title('Iris Flower Classifier')
st.markdown("""
Predict the species of an Iris flower using sepal and petal measurements.
""")

# Define components for the sidebar
st.sidebar.header('Input Features')
sepal_length = st.sidebar.slider(
    label='Sepal Length',
    min_value=float(df['sepal_length'].min()),
    max_value=float(df['sepal_length'].max()),
    value=float(round(df['sepal_length'].mean(), 1)),
    step=0.1)
sepal_width = st.sidebar.slider(
    label='Sepal Width',
    min_value=float(df['sepal_width'].min()),
    max_value=float(df['sepal_width'].max()),
    value=float(round(df['sepal_width'].mean(), 1)),
    step=0.1)
petal_length = st.sidebar.slider(
    label='Petal Length',
    min_value=float(df['petal_length'].min()),
    max_value=float(df['petal_length'].max()),
    value=float(round(df['petal_length'].mean(), 1)),
    step=0.1)
petal_width = st.sidebar.slider(
    label='Petal Width',
    min_value=float(df['petal_width'].min()),
    max_value=float(df['petal_width'].max()),
    value=float(round(df['petal_width'].mean(), 1)),
    step=0.1)

# Scale the user inputs
X_scaled = scaler.transform([[sepal_length, sepal_width, petal_length, petal_width]])

# Run input through the model
y_pred = model.predict(X_scaled)
df_pred = pd.DataFrame({
    'Species': ['Virginica', 'Versicolor', 'Setosa'],
    'Confidence': y_pred.flatten()
})

# Define the prediction bar chart
fig = px.bar(
    df_pred, 
    x='Species', 
    y='Confidence',
    width=350, 
    height=350, 
    color='Species',
    color_discrete_sequence =['#00CC96', '#EF553B', '#636EFA'])

# Create two columns for the web app
# Column 1 will be for the predictions
# Column 2 will be for the PCA
col1, col2 = st.beta_columns((1, 1.2))
with col1:
    st.markdown('### Predictions')
    fig

@st.cache
def run_pca():
    # Run PCA
    pca = PCA(2)
    X = df.iloc[:, :4]
    X_pca = pca.fit(X).transform(X)
    df_pca = pd.DataFrame(pca.transform(X))
    df_pca.columns = ['PC1', 'PC2']
    df_pca = pd.concat([df_pca, df['species']], axis=1)
    
    return pca, df_pca

pca, df_pca = run_pca()
# Create the PCA chart
pca_fig = px.scatter(
    df_pca, 
    x='PC1', 
    y='PC2', 
    color='species', 
    hover_name='species', 
    width=500, 
    height=350)

# Retrieve user input
datapoint = np.array([[
            sepal_length,
            sepal_width,
            petal_length,
            petal_width
        ]])
# Map the 4-D user input to 2-D using the PCA
datapoint_pca = pca.transform(datapoint)
# Add the user input to the PCA chart
pca_fig.add_trace(go.Scatter(
        x=[datapoint_pca[0, 0]], 
        y=[datapoint_pca[0,1]], 
        mode='markers', 
        marker={'color': 'black', 'size':10}, name='Your Datapoint'))

with col2:
    st.markdown('### Principle Component Analysis')
    pca_fig
