import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(
    page_title="Six Sigma Dashboard - PT XYZ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palet Warna 5 Warna Solid
MERAH = "#D71920"
KUNING = "#F5C518"
HITAM = "#1A1C20"
PUTIH = "#FFFFFF"
BIRU = "#2563EB"
ABU_BG = "#F4F5F7"
ABU_TEKS = "#5A606A"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea, select, table, th, td, p, div, span, h1, h2, h3, h4, label {{
    font-family: 'Poppins', sans-serif !important;
}}

.stApp {{
    background-color: {ABU_BG};
    color: {HITAM};
}}
.block-container {{
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    max-width: 1380px;
}}

/* Sidebar Terkunci & Header Putih PT XYZ */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {PUTIH} 0px, {PUTIH} 68px, {HITAM} 68px, {HITAM} 100%) !important;
    border-right: 1px solid #E5E7EB;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}}
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    padding-top: 0.65rem !important;
    padding-bottom: 0.65rem !important;
}}

/* Tombol Segitiga / Panah Buka-Tutup Sidebar (< dan >) agar Kontras & Tidak Ketutupan */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button,
button[kind="headerNoPadding"] {{
    background-color: {HITAM} !important;
    color: {PUTIH} !important;
    border: 1.5px solid {HITAM} !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.18) !important;
}}
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="collapsedControl"] button:hover {{
    background-color: {MERAH} !important;
    border-color: {MERAH} !important;
    color: {PUTIH} !important;
}}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] svg {{
    fill: {PUTIH} !important;
    color: {PUTIH} !important;
}}

/* Header PT XYZ Pojok Kiri Atas */
.sidebar-logo {{
    text-align: left;
    padding: 6px 14px 14px 14px;
    margin-bottom: 8px;
}}
.logo-title {{
    font-size: 20px;
    font-weight: 800;
    color: {HITAM} !important;
    letter-spacing: 0.4px;
    line-height: 1.2;
}}

/* Menu Radio di Sidebar */
[data-testid="stSidebar"] .stRadio > label {{
    display: none !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 4px !important;
    padding: 0 8px;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background-color: transparent;
    border-radius: 9px;
    padding: 8px 14px !important;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    width: 100%;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label p {{
    color: {PUTIH} !important;
    font-size: 13.5px;
    font-weight: 500;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background-color: {MERAH} !important;
    box-shadow: 0 4px 12px rgba(215, 25, 32, 0.35);
}}
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
    color: {PUTIH} !important;
    font-weight: 700 !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child,
[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {{
    display: none !important;
}}

/* Header Banner Utama Ramping */
.dashboard-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: {PUTIH};
    padding: 13px 22px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    border: 1px solid #E5E7EB;
    margin-bottom: 16px;
    gap: 14px;
}}
.header-left {{
    display: flex;
    align-items: stretch;
    gap: 12px;
}}
.header-stripe {{
    width: 5px;
    border-radius: 4px;
    background: linear-gradient(180deg, {MERAH} 0%, {MERAH} 65%, {KUNING} 65%, {KUNING} 100%);
}}
.header-title {{
    font-size: 21px;
    font-weight: 700;
    color: {HITAM};
    margin: 0;
    line-height: 1.2;
}}
.header-subtitle {{
    font-size: 12.5px;
    font-style: italic;
    color: {ABU_TEKS};
    margin: 2px 0 0 0;
    line-height: 1.3;
}}
.period-badge {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: {PUTIH};
    border: 1px solid #D1D5DB;
    border-radius: 9px;
    padding: 6px 13px;
    font-size: 12.5px;
    font-weight: 600;
    color: {HITAM};
    white-space: nowrap;
    flex-shrink: 0;
}}

/* Kartu KPI Fleksibel & Responsif */
.kpi-box {{
    background: {PUTIH};
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    border: 1px solid #E5E7EB;
    position: relative;
    overflow: hidden;
    min-height: 104px;
    height: 100%;
    width: 100%;
    box-
