
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm

st.set_page_config(
    page_title="Analisis Kualitas Produksi AAC",
    page_icon="📊",
    layout="wide"
)

st.title("Analisis Kualitas Produksi Bata Ringan AAC")

st.write("Dashboard analisis kualitas produksi bata ringan.")
