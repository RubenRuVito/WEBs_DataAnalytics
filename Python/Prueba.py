# https://programmerclick.com/article/56071642020/

import matplotlib.pyplot as plt
import seaborn  as sns
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
from matplotlib.figure import Figure


st.write("My First Streamlit Web App")

iris_data = datasets.load_iris()
df = pd.DataFrame(iris_data)
st.write(df).head()

st.subheader("Iris - Sepal Length")
fig = Figure()
ax = fig.subplots()
sns.histplot(pd.to_numeric(df['Sepal.length'], errors='coerce').dropna().astype(np.int64), ax=ax, kde=True)
ax.set_xlabel('Sepal Length')
ax.set_ylabel('Density')
st.pyplot(fig)
