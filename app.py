import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(
    page_title="Six Sigma Dashboard - PT XYZ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palet Warna Sesuai Desain Referensi PT XYZ
MERAH = "#D71920"
KUNING = "#F5C518"
HITAM = "#1A1C20"
PUTIH = "#FFFFFF"
BIRU = "#2563EB"
ABU_BG = "#FFFFFF"
ABU_TEKS = "#1A1C20"

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
    font-family: 'Poppins', sans-serif !important;
}}
.stApp {{
    background-color: {ABU_BG};
    color: {HITAM};
}}
.block-container {{
    padding-top: 0.65rem;
    padding-bottom: 1.25rem;
    max-width: 1380px;
}}

/* Sidebar dengan Header Putih & Body Gelap */
[data-testid="stSidebar"] {{
    background: {HITAM};
    border-right: 1px solid #E5E7EB;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top: 0.7rem;
}}

/* Logo Box di Sidebar */
.sidebar-logo {{
    text-align: center;
    padding: 8px 10px 14px 10px;
    margin-bottom: 8px;
}}
.logo-bars {{
    display: inline-flex;
    gap: 5px;
    margin-bottom: 4px;
}}
.bar-red {{ width: 14px; height: 26px; background: {MERAH}; transform: skewX(-22deg); border-radius: 2px; }}
 .bar-orange {{ width: 14px; height: 26px; background: {MERAH}; transform: skewX(-22deg); border-radius: 2px; }}
.bar-yellow {{ width: 14px; height: 26px; background: {KUNING}; transform: skewX(-22deg); border-radius: 2px; }}
.logo-title {{
    font-size: 22px;
    font-weight: 900;
    color: {HITAM} !important;
    letter-spacing: 0.5px;
    line-height: 1.1;
}}
.logo-sub {{
    font-size: 10.5px;
    font-weight: 600;
    color: {ABU_TEKS} !important;
}}

/* Menu Radio di Sidebar */
[data-testid="stSidebar"] .stRadio > label {{
    display: none;
}}
[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 6px;
    padding: 0 8px;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background-color: transparent;
    border-radius: 10px;
    padding: 10px 14px;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}}
