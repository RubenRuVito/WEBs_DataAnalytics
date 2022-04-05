# https://programmerclick.com/article/56071642020/

import seaborn as sns
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


st.write("My First Streamlit Web App")

iris_data = sns.load_dataset('iris')
df = pd.DataFrame(iris_data)
st.write(df)

#st.subheader("Iris - Sepal Length")
#fig = Figure()
#ax = fig.subplots()
#sns.histplot(pd.to_numeric(df['Sepal.length'], errors='coerce').dropna().astype(np.int64), ax=ax, kde=True)
#ax.set_xlabel('Sepal Length')
#ax.set_ylabel('Density')
#st.pyplot(fig)

#sns.pairplot(iris)
#plt.show()

df.plot(kind='bar')
st.pyplot()

# Show Plots
#if st.checkbox("Simple Correlation Plot with Matplotlib "):
plt.matshow(df.corr())
st.pyplot()

# Show Plots
# if st.checkbox("Simple Correlation Plot with Seaborn "):
	st.write(sns.heatmap(df.corr(),annot=True))
	# Use Matplotlib to render seaborn
	st.pyplot()

# Show Plots
#if st.checkbox("Bar Plot of Groups or Counts"):
	v_counts = df.groupby('species')
	st.bar_chart(v_counts)

