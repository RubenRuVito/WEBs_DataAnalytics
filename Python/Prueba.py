# https://programmerclick.com/article/56071642020/

from sklearn import datasets
import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import seaborn as sns

st.write("My First Streamlit Web App")

iris_data = datasets.load_iris()
df = pd.DataFrame(iris_data})
st.write(df).head()

st.subheader("Book Age")
fig = Figure()
ax = fig.subplots()
sns.histplot(pd.to_numeric(df['Sepal.length'], errors='coerce').dropna().astype(np.int64), ax=ax, kde=True)
ax.set_xlabel('Sepal Length')
ax.set_ylabel('Density')
st.pyplot(fig)
