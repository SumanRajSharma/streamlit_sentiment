import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Plotting Demo")

st.title("Plotting Demo")
st.write("This is a simple plotting demo.")

# Create some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a plot
fig, ax = plt.subplots()
ax.plot(x, y)

st.pyplot(fig)

