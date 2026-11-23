import io
import math
import textwrap
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

# Palet Warna Solid (Merah Marun Pekat, Kuning Emas, Putih, Hitam — Tanpa Warna Biru)
MERAH = "#5C0A0A"
MERAH_HOVER = "#420606"
KUNING = "#F5C518"
HITAM = "#1A1C20"
PUTIH = "#FFFFFF"
ABU_BG = "#F4F5F7"
ABU_TEKS = "#5A606A"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

:root {{
    --primary-color: {MERAH} !important;
    --background-color: {ABU_BG} !important;
    --secondary-background-color: {PUTIH} !important;
    --text-color: {HITAM} !important;
}}

html, body, .stApp, p, div, h1, h2, h3, h4, label, input, textarea, select, button, table, th, td {{
    font-family: 'Poppins', sans-serif !important;
}}
[data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] span {{
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}}

.stApp {{
    background-color: {ABU_BG};
    color: {HITAM};
}}

.block-container {{
    padding-top: 3.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1380px;
}}

*:focus, *:focus-visible {{
    outline-color: {MERAH} !important;
    box-shadow: none !important;
}}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within,
div[data-baseweb="select"] > div:focus-within {{
    border-color: {MERAH} !important;
    box-shadow: 0 0 0 1px {MERAH} !important;
}}
span[data-baseweb="tag"] {{
    background-color: {MERAH} !important;
    color: {PUTIH} !important;
}}

[data-testid="stSidebar"] {{
    background: {MERAH} !important;
    background-color: {MERAH} !important;
    border-right: none !important;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
}}
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{
    background-color: {MERAH} !important;
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
    padding-top: 0 !important;
    padding-bottom: 0.6rem !important;
}}

[data-testid="stSidebarHeader"] {{
    background-color: {MERAH} !important;
    min-height: 112px !important;
    padding: 22px 14px 30px 18px !important;
    display: flex !important;
    align-items: flex-start !important;
    justify-content: space-between !important;
    gap: 10px !important;
    margin-bottom: 24px !important;
    border-bottom: 1.5px solid rgba(255, 255, 255, 0.32) !important;
}}
[data-testid="stSidebarHeader"]::before {{
    content: "Dashboard Kualitas Produksi PT XYZ";
    font-family: 'Poppins', sans-serif !important;
    font-size: 16.5px;
    font-weight: 700;
    color: {PUTIH};
    line-height: 1.4;
    max-width: 190px;
}}

[data-testid="stSidebarCollapseButton"] button {{
    background-color: rgba(255, 255, 255, 0.16) !important;
    color: {PUTIH} !important;
    border: none !important;
    border-radius: 8px !important;
    width: 32px !important;
    height: 32px !important;
    flex-shrink: 0 !important;
}}
[data-testid="stSidebarCollapseButton"] button:hover {{
    background-color: {KUNING} !important;
    color: {HITAM} !important;
}}
[data-testid="stSidebarCollapseButton"] button:hover svg,
[data-testid="stSidebarCollapseButton"] button:hover span {{
    fill: {HITAM} !important;
    color: {HITAM} !important;
}}
[data-testid="collapsedControl"] button {{
    background-color: {MERAH} !important;
    color: {PUTIH} !important;
    border: none !important;
    border-radius: 8px !important;
    width: 34px !important;
    height: 34px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}}
[data-testid="collapsedControl"] button:hover {{
    background-color: {MERAH_HOVER} !important;
}}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] span {{
    fill: {PUTIH} !important;
    color: {PUTIH} !important;
}}

[data-testid="stSidebar"] .stRadio > label {{
    display: none !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 6px !important;
    padding: 4px 12px 0 12px !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background-color: transparent;
    border-radius: 9px;
    padding: 9px 14px !important;
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
    background-color: rgba(255, 255, 255, 0.14);
}}
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background-color: {KUNING} !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.24);
}}
[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
    color: {HITAM} !important;
    font-weight: 700 !important;
}}
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child,
[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {{
    display: none !important;
}}

.dashboard-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: {MERAH};
    padding: 23px 26px;
    min-height: 86px;
    border-radius: 14px;
    box-shadow: 0 10px 26px rgba(26, 28, 32, 0.20);
    border: 1px solid rgba(255, 255, 255, 0.14);
    margin-bottom: 20px;
    gap: 18px;
}}
.header-text-wrap {{
    display: flex;
    flex-direction: column;
    gap: 5px;
}}
.header-title {{
    font-size: 20px !important;
    font-weight: 700 !important;
    color: {PUTIH} !important;
    margin: 0 !important;
    line-height: 1.25 !important;
}}
.header-subtitle {{
    font-size: 12.8px !important;
    font-weight: 400 !important;
    color: rgba(255, 255, 255, 0.90) !important;
    margin: 0 !important;
    line-height: 1.45 !important;
}}
.period-badge {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: {PUTIH};
    border: 1px solid rgba(255, 255, 255, 0.4);
    border-radius: 9px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 600;
    color: {HITAM};
    white-space: nowrap;
    flex-shrink: 0;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}}

div[data-testid="stHorizontalBlock"] {{
    align-items: stretch !important;
}}
div[data-testid="column"],
div[data-testid="stColumn"] {{
    display: flex !important;
    flex-direction: column !important;
}}
div[data-testid="column"] > div,
div[data-testid="stColumn"] > div,
div[data-testid="column"] [data-testid="stVerticalBlock"],
div[data-testid="stColumn"] [data-testid="stVerticalBlock"] {{
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}}

.kpi-box {{
    background: {PUTIH};
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 8px 22px rgba(26, 28, 32, 0.11);
    border: 1px solid #E2E5EA;
    position: relative;
    overflow: hidden;
    height: 112px;
    min-height: 112px;
    max-height: 112px;
    width: 100%;
    box-sizing: border-box;
}}
.kpi-box::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 5px;
    background-color: {MERAH};
}}
.kpi-icon {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background-color: {MERAH};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    font-weight: 700;
    color: {PUTIH};
    flex-shrink: 0;
}}
.kpi-content {{
    min-width: 0;
    flex: 1;
}}
.kpi-title {{
    font-size: 12.5px;
    font-weight: 600;
    color: {ABU_TEKS};
    margin-bottom: 4px;
    line-height: 1.3;
    white-space: normal;
    word-wrap: break-word;
}}
.kpi-number {{
    font-size: clamp(18px, 1.35vw, 22px);
    font-weight: 800;
    color: {HITAM};
    line-height: 1.2;
    white-space: normal;
    overflow-wrap: anywhere;
}}

.action-card {{
    background: {PUTIH};
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0 8px 22px rgba(26, 28, 32, 0.11);
    border: 1px solid #E2E5EA;
    margin-bottom: 14px;
    width: 100%;
    box-sizing: border-box;
}}
.home-card {{
    height: 192px !important;
    min-height: 192px !important;
    max-height: 192px !important;
    padding: 24px 26px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: flex-start !important;
    margin-bottom: 14px !important;
}}
.action-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}}
.action-badge {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background-color: {MERAH};
    color: {PUTIH};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 700;
    flex-shrink: 0;
}}
.action-title {{
    font-size: 16px;
    font-weight: 700;
    color: {HITAM};
    margin: 0;
    line-height: 1.3;
}}
.action-desc {{
    font-size: 13px;
    color: {ABU_TEKS};
    margin: 0;
    line-height: 1.6;
}}
.fmea-guide-text {{
    font-size: 12.5px;
    color: {HITAM};
    line-height: 1.6;
    margin-bottom: 4px;
}}

div.stButton > button,
div.stDownloadButton > button {{
    background-color: {MERAH} !important;
    color: {PUTIH} !important;
    border: none !important;
    border-radius: 10px !important;
    height: 46px !important;
    min-height: 46px !important;
    max-height: 46px !important;
    padding: 0 1.2rem !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 16px rgba(26, 28, 32, 0.18) !important;
    width: 100% !important;
    margin: 0 !important;
}}
div.stButton > button:hover,
div.stDownloadButton > button:hover {{
    background-color: {MERAH_HOVER} !important;
    color: {PUTIH} !important;
}}

[data-testid="stFileUploader"] {{
    width: 100% !important;
    margin: 0 !important;
}}
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {{
    background-color: {MERAH} !important;
    border: none !important;
    border-radius: 10px !important;
    height: 46px !important;
    min-height: 46px !important;
    max-height: 46px !important;
    padding: 0 16px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 6px 16px rgba(26, 28, 32, 0.18) !important;
    cursor: pointer !important;
    width: 100% !important;
    box-sizing: border-box !important;
}}
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {{
    background-color: {MERAH_HOVER} !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] {{
    display: none !important;
}}
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button {{
    background-color: transparent !important;
    border: none !important;
    color: {PUTIH} !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
}}
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] button *,
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] svg {{
    color: {PUTIH} !important;
    fill: {PUTIH} !important;
    opacity: 1 !important;
}}

.interp-box {{
    background: {PUTIH};
    border-radius: 12px;
    padding: 16px 20px;
    color: {HITAM};
    font-size: 13.5px;
    line-height: 1.65;
    box-shadow: 0 8px 22px rgba(26, 28, 32, 0.11);
    border: 1px solid #E2E5EA;
    border-left: 6px solid {MERAH};
    margin-bottom: 14px;
}}
.interp-red, .interp-dark, .interp-yellow {{
    border-left: 6px solid {MERAH};
}}

label, .stTextArea label, .stTextInput label, .stSelectbox label, .stNumberInput label {{
    color: {HITAM} !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
}}
textarea, input {{
    background-color: {PUTIH} !important;
    color: {HITAM} !important;
    -webkit-text-fill-color: {HITAM} !important;
}}
textarea::placeholder, input::placeholder {{
    color: #4B5563 !important;
    -webkit-text-fill-color: #4B5563 !important;
    opacity: 1 !important;
}}

h1, h2, h3 {{ color: {HITAM}; }}
</style>
""", unsafe_allow_html=True)

# Session State
if "df_produksi" not in st.session_state:
    st.session_state.df_produksi = None
if "riwayat_iterasi" not in st.session_state:
    st.session_state.riwayat_iterasi = []
if "excluded_subgroups" not in st.session_state:
    st.session_state.excluded_subgroups = []
if "fishbone_inputs" not in st.session_state:
    st.session_state.fishbone_inputs = {
        "Man (Manusia)": "",
        "Machine (Mesin)": "",
        "Method (Metode)": "",
        "Material (Bahan)": "",
        "Measurement (Pengukuran)": "",
        "Environment (Lingkungan)": ""
    }
if "fishbone_problem" not in st.session_state:
    st.session_state.fishbone_problem = "Tingginya Produk Cacat Bata Ringan AAC"
if "fishbone_generated" not in st.session_state:
    st.session_state.fishbone_generated = False
if "fmea_scores" not in st.session_state:
    st.session_state.fmea_scores = pd.DataFrame()

CALENDAR_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#1A1C20" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'

def render_header(judul="Six Sigma Dashboard", subjudul=None):
    df = st.session_state.df_produksi
    if df is not None and not df.empty:
        tgl_awal = df["Tanggal"].min().strftime("%b %Y")
        tgl_akhir = df["Tanggal"].max().strftime("%b %Y")
        periode_teks = f"{tgl_awal} – {tgl_akhir}" if tgl_awal != tgl_akhir else tgl_awal
    else:
        periode_teks = "Menunggu Data"

    sub_html = f'<div class="header-subtitle">{subjudul}</div>' if subjudul else ""
    html = (
        f'<div class="dashboard-header">'
        f'<div class="header-text-wrap"><div class="header-title">{judul}</div>{sub_html}</div>'
        f'<div class="period-badge">{CALENDAR_SVG} <span>Periode Analisis: {periode_teks}</span></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_kpi(kolom, simbol, label, nilai):
    simbol_html = f'<div class="kpi-icon">{simbol}</div>' if simbol else ""
    html = (
        f'<div class="kpi-box">'
        f'{simbol_html}'
        f'<div class="kpi-content"><div class="kpi-title">{label}</div><div class="kpi-number">{nilai}</div></div>'
        f'</div>'
    )
    kolom.markdown(html, unsafe_allow_html=True)

def format_angka(x):
    return f"{x:,.0f}".replace(",", ".")

def format_koma(x, desimal=3):
    return f"{x:,.{desimal}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor=PUTIH,
        plot_bgcolor=PUTIH,
        font=dict(family="Poppins, sans-serif", color=HITAM, size=12),
        title=dict(font=dict(family="Poppins, sans-serif", color=HITAM, size=15), x=0, y=0.96, yanchor="top"),
        margin=dict(l=35, r=20, t=90, b=35),
        legend=dict(orientation="h", x=0, xanchor="left", y=1.08, yanchor="bottom", font=dict(color=HITAM))
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", tickfont=dict(color=HITAM), title_font=dict(color=HITAM))
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB", tickfont=dict(color=HITAM), title_font=dict(color=HITAM))
    return fig

KOLOM_WAJIB = ["Tanggal", "Jumlah Produk Cacat", "Jumlah Unit Diperiksa"]

def validasi_data_produksi(data):
    df = data.copy()
    hilang = [c for c in KOLOM_WAJIB if c not in df.columns]
    if hilang:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(hilang)}")
    df = df[KOLOM_WAJIB].copy()
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    for c in ["Jumlah Produk Cacat", "Jumlah Unit Diperiksa"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if df.empty:
        raise ValueError("File tidak memiliki baris data.")
    if df.isna().any().any():
        raise ValueError("Terdapat tanggal atau angka kosong/tidak valid.")
    if (df["Jumlah Unit Diperiksa"] <= 0).any():
        raise ValueError("Jumlah Unit Diperiksa harus lebih besar dari 0.")
    if (df["Jumlah Produk Cacat"] < 0).any():
        raise ValueError("Jumlah Produk Cacat tidak boleh negatif.")
    if (df["Jumlah Produk Cacat"] > df["Jumlah Unit Diperiksa"]).any():
        raise ValueError("Jumlah cacat tidak boleh melebihi unit diperiksa.")
    for c in ["Jumlah Produk Cacat", "Jumlah Unit Diperiksa"]:
        if not np.all(np.isclose(df[c], np.round(df[c]))):
            raise ValueError(f"Kolom {c} harus berisi bilangan bulat.")
        df[c] = df[c].astype(int)
    return df.reset_index(drop=True)

def buat_template_excel():
    contoh = pd.DataFrame({
        "Tanggal": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03"]),
        "Jumlah Produk Cacat": [12, 15, 9],
        "Jumlah Unit Diperiksa": [1000, 1050, 980]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        contoh.to_excel(writer, index=False, sheet_name="Data_Produksi")
    return output.getvalue()

def get_data_aktif():
    if st.session_state.df_produksi is None:
        return None, None
    dasar = st.session_state.df_produksi.copy()
    dasar["Subgrup"] = np.arange(1, len(dasar) + 1)
    dikeluarkan = {x["Subgrup"] for x in st.session_state.excluded_subgroups}
    aktif = dasar.loc[~dasar["Subgrup"].isin(dikeluarkan)].copy().reset_index(drop=True)
    return dasar, aktif

def hitung_peta_kendali(df_input, gunakan_laney=None):
    df = df_input.copy()

    if len(df) < 2:
        raise ValueError("Minimal diperlukan dua subgrup.")

    if "Subgrup" not in df.columns:
        df["Subgrup"] = np.arange(1, len(df) + 1)

    df = df.sort_values("Subgrup").reset_index(drop=True)

    if (df["Jumlah Unit Diperiksa"] <= 0).any():
        raise ValueError("Jumlah Unit Diperiksa harus lebih besar dari 0.")

    # Proporsi cacat
    df["p_i"] = (
        df["Jumlah Produk Cacat"] /
        df["Jumlah Unit Diperiksa"]
    )

    # Proporsi rata-rata tertimbang (sesuai rumus Excel: total cacat / total inspeksi)
    p_bar = float(df["Jumlah Produk Cacat"].sum() / df["Jumlah Unit Diperiksa"].sum())

    if not 0 < p_bar < 1:
        raise ValueError("Rata-rata proporsi tidak valid.")

    # Standar deviasi proporsi
    df["sigma_pi"] = np.sqrt(
        p_bar * (1 - p_bar) /
        df["Jumlah Unit Diperiksa"]
    )

    if (df["sigma_pi"] == 0).any():
        raise ValueError("Simpangan baku proporsi bernilai nol.")

    # Standardisasi
    df["z_i"] = (
        (df["p_i"] - p_bar) /
        df["sigma_pi"]
    )

    # Moving Range dan Sigma Z
    df["R_i"] = df["z_i"].diff().abs()

    R_bar = float(df["R_i"].dropna().mean())
    sigma_z = R_bar / 1.128

    overdispersi = sigma_z > 1

    # Metode ditentukan dari data awal dan dikunci selama iterasi
    if gunakan_laney is None:
        gunakan_laney = overdispersi

    # Batas kendali P
    df["BKA_P"] = np.minimum(
        1,
        p_bar + 3 * df["sigma_pi"]
    )
    df["BKB_P"] = np.maximum(
        0,
        p_bar - 3 * df["sigma_pi"]
    )

    # Batas kendali Laney P'
    df["BKA_Laney"] = np.minimum(
        1,
        p_bar + 3 * sigma_z * df["sigma_pi"]
    )
    df["BKB_Laney"] = np.maximum(
        0,
        p_bar - 3 * sigma_z * df["sigma_pi"]
    )

    if gunakan_laney:
        df["BKA_Aktif"] = df["BKA_Laney"]
        df["BKB_Aktif"] = df["BKB_Laney"]
        jenis = "Peta Kendali Laney P'"
    else:
        df["BKA_Aktif"] = df["BKA_P"]
        df["BKB_Aktif"] = df["BKB_P"]
        jenis = "Peta Kendali P"

    df["CL"] = p_bar

    df["Status_OOC"] = (
        (df["p_i"] > df["BKA_Aktif"]) |
        (df["p_i"] < df["BKB_Aktif"])
    )

    ringkasan = {
        "m": len(df),
        "p_bar": p_bar,
        "R_bar": R_bar,
        "sigma_z": sigma_z,
        "is_overdispersed": overdispersi,
        "chart_type": jenis,
        "jumlah_ooc": int(df["Status_OOC"].sum()),
        "jumlah_ic": int((~df["Status_OOC"]).sum())
    }

    return df, ringkasan


def hitung_tahapan_peta_kendali(df_input):
    dasar = df_input.copy()

    if "Subgrup" not in dasar.columns:
        dasar["Subgrup"] = np.arange(1, len(dasar) + 1)

    dasar = dasar.sort_values("Subgrup").reset_index(drop=True)

    # Identifikasi metode dari data awal
    _, hasil_awal = hitung_peta_kendali(dasar)
    pakai_laney = hasil_awal["is_overdispersed"]

    tahapan = []
    data_aktif = dasar.copy()
    seluruh_subgrup_dikeluarkan = []

    nomor_tahap = 1

    while len(data_aktif) >= 2:

        df_ctrl, hasil = hitung_peta_kendali(
            data_aktif,
            gunakan_laney=pakai_laney
        )

        ooc = df_ctrl[df_ctrl["Status_OOC"]].copy()

        tahapan.append({
            "tahap": nomor_tahap,
            "data": df_ctrl.copy(),
            "ringkasan": hasil.copy(),
            "ooc": ooc.copy(),
            "dikeluarkan_sebelumnya":
                seluruh_subgrup_dikeluarkan.copy()
        })

        # Berhenti jika sudah tidak ada OOC
        if ooc.empty:
            break

        subgrup_ooc = ooc["Subgrup"].astype(int).tolist()

        # Pengaman jika data tersisa kurang dari dua subgrup
        if len(data_aktif) - len(subgrup_ooc) < 2:
            break

        seluruh_subgrup_dikeluarkan.extend(subgrup_ooc)

        data_aktif = data_aktif[
            ~data_aktif["Subgrup"].isin(subgrup_ooc)
        ].copy().reset_index(drop=True)

        nomor_tahap += 1

    return tahapan, pakai_laney


def hitung_runs_test(data):
    """Runs Test dua sisi terhadap median, tanpa koreksi kontinuitas."""
    x = pd.Series(data, dtype="float64").dropna().to_numpy()
    if len(x) < 2:
        raise ValueError("Runs Test memerlukan minimal dua pengamatan.")

    median = float(np.median(x))
    # Nilai yang tepat sama dengan median tidak dimasukkan ke dua kelompok,
    # sesuai prosedur Runs Test berbasis median.
    tanda = np.where(x > median, 1, np.where(x < median, 0, np.nan))
    tanda = tanda[~pd.isna(tanda)].astype(int)
    n1 = int(np.sum(tanda == 1))
    n2 = int(np.sum(tanda == 0))
    if n1 == 0 or n2 == 0:
        raise ValueError("Runs Test tidak dapat dihitung karena seluruh data berada pada satu sisi median.")

    V = int(1 + np.sum(tanda[1:] != tanda[:-1]))
    n = n1 + n2
    mean_runs = (2 * n1 * n2) / n + 1
    variance = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))
    if variance <= 0:
        raise ValueError("Varians Runs Test tidak valid untuk data ini.")
    Z = float((V - mean_runs) / np.sqrt(variance))
    p_value = float(2 * norm.sf(abs(Z)))
    return {"median": median, "V": V, "Z": Z, "p_value": p_value,
            "n1": n1, "n2": n2, "expected_runs": mean_runs,
            "std_runs": float(np.sqrt(variance))}


def hitung_ppk_persen(p_bar):
    """Menghitung Z(p-bar) dan P%pk = Z/3 dari proporsi cacat."""
    p_bar = float(p_bar)
    if not 0 < p_bar < 1:
        raise ValueError("Proporsi cacat harus berada di antara 0 dan 1.")
    z_p = float(norm.ppf(1 - p_bar))
    return z_p, z_p / 3


def hitung_level_sigma(total_cacat, total_unit, peluang_per_unit=1, shift=1.5):
    """Menghitung DPO, DPMO, dan level sigma dengan shift yang ditentukan."""
    total_cacat = float(total_cacat)
    total_unit = float(total_unit)
    peluang_per_unit = float(peluang_per_unit)
    if total_unit <= 0 or peluang_per_unit <= 0:
        raise ValueError("Jumlah unit dan peluang per unit harus lebih besar dari nol.")
    if total_cacat < 0:
        raise ValueError("Jumlah produk cacat tidak boleh negatif.")
    dpo = total_cacat / (total_unit * peluang_per_unit)
    dpmo = dpo * 1_000_000
    if dpo <= 0:
        sigma = float("inf")
    elif dpo >= 1:
        sigma = float("-inf")
    else:
        sigma = float(norm.ppf(1 - dpo) + float(shift))
    return float(dpo), float(dpmo), sigma


def get_data_final_in_control():
    """Ambil subgrup tersisa setelah iterasi otomatis peta kendali."""
    if st.session_state.df_produksi is None:
        return None
    dasar = st.session_state.df_produksi.copy()
    dasar["Subgrup"] = np.arange(1, len(dasar) + 1)
    tahapan, _ = hitung_tahapan_peta_kendali(dasar)
    if not tahapan:
        return dasar
    return tahapan[-1]["data"].copy()


def halaman_beranda():
    render_header(
        judul="Six Sigma Dashboard",
        subjudul="Dashboard ini bertujuan untuk memantau dan menganalisis pengendalian kualitas produksi bata ringan AAC pada PT XYZ menggunakan pendekatan Six Sigma."
    )

    df = st.session_state.df_produksi
    if df is not None and not df.empty:
        total_unit = int(df["Jumlah Unit Diperiksa"].sum())
        total_cacat = int(df["Jumlah Produk Cacat"].sum())
        persen = (total_cacat / total_unit * 100) if total_unit > 0 else 0.0
    else:
        total_unit = 0
        total_cacat = 0
        persen = 0.0

    k1, k2, k3 = st.columns(3)
    render_kpi(k1, None, "Total Unit Diperiksa", format_angka(total_unit))
    render_kpi(k2, None, "Total Produk Cacat", format_angka(total_cacat))
    render_kpi(k3, None, "Persentase Cacat", f"{persen:.2f}%")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    col_kiri, col_kanan = st.columns(2)
    with col_kiri:
        st.markdown(
            '<div class="action-card home-card">'
            '<div class="action-header"><div class="action-badge">⬇</div><h3 class="action-title">Template Data Excel</h3></div>'
            '<p class="action-desc">Unduh template untuk memasukkan data produksi dan kecacatan sesuai format standar.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        st.download_button(
            "Download Template.xlsx",
            data=buat_template_excel(),
            file_name="Template_Data_Produksi_AAC.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_kanan:
        st.markdown(
            '<div class="action-card home-card">'
            '<div class="action-header"><div class="action-badge">☁</div><h3 class="action-title">Unggah Data</h3></div>'
            '<p class="action-desc">Upload file Excel (.xlsx) yang sudah diisi sesuai template untuk memulai analisis.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        file = st.file_uploader(
            "Upload File Excel (.xlsx)",
            type=["xlsx", "xls"],
            key="file_produksi",
            label_visibility="collapsed"
        )
        if file is not None:
            try:
                data_baru = validasi_data_produksi(pd.read_excel(file))
                st.session_state.df_produksi = data_baru
                st.session_state.riwayat_iterasi = []
                st.session_state.excluded_subgroups = []
                st.success(f"Data berhasil dibaca: {len(data_baru)} subgrup.")
                st.rerun()
            except Exception as e:
                st.error(f"File belum dapat digunakan: {e}")

def halaman_overdispersi():
    render_header(judul="Identifikasi Overdispersi")
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return

    data_uji = aktif if (aktif is not None and len(aktif) >= 2) else dasar
    if st.session_state.excluded_subgroups:
        st.caption(f"Menggunakan data aktif ({len(data_uji)} subgrup) setelah mengeluarkan {len(st.session_state.excluded_subgroups)} subgrup penyebab khusus.")

    try:
        _, res = hitung_peta_kendali(data_uji)
    except Exception as e:
        st.error(str(e))
        return

    a, b, c, d = st.columns(4)
    render_kpi(a, "p̄", "Rata-rata Proporsi (p̄)", f"{res['p_bar']:.4f}")
    render_kpi(b, "R̄", "Rata-rata Moving Range (R̄)", f"{res['R_bar']:.4f}")
    render_kpi(c, "σz", "Sigma Z", f"{res['sigma_z']:.4f}")
    render_kpi(d, None, "Keputusan", "Overdispersi" if res["is_overdispersed"] else "Tidak Overdispersi")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    if res["is_overdispersed"]:
        st.markdown(f'<div class="interp-box interp-yellow">Nilai Sigma Z = <b>{res["sigma_z"]:.4f} &gt; 1</b>, sehingga data mengalami overdispersi. Jenis peta kendali yang dipilih: <b>{res["chart_type"]}</b>.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="interp-box interp-dark">Nilai Sigma Z = <b>{res["sigma_z"]:.4f} &le; 1</b>, sehingga data tidak mengalami overdispersi. Jenis peta kendali yang dipilih: <b>{res["chart_type"]}</b>.</div>', unsafe_allow_html=True)

def halaman_peta_kendali():
    render_header(judul="Analisis Peta Kendali")

    if st.session_state.df_produksi is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return

    dasar = st.session_state.df_produksi.copy()
    dasar["Subgrup"] = np.arange(1, len(dasar) + 1)

    try:
        tahapan, pakai_laney = hitung_tahapan_peta_kendali(dasar)
    except Exception as e:
        st.error(f"Perhitungan peta kendali gagal: {e}")
        return

    if not tahapan:
        st.warning("Tidak terdapat tahapan yang dapat dihitung.")
        return

    for hasil_tahap in tahapan:

        tahap_ke = hasil_tahap["tahap"]
        df_ctrl = hasil_tahap["data"]
        res = hasil_tahap["ringkasan"]
        ooc = hasil_tahap["ooc"]
        dikeluarkan = hasil_tahap["dikeluarkan_sebelumnya"]

        st.markdown(f"## Peta Kendali — Tahap {tahap_ke}")

        if dikeluarkan:
            st.caption(
                "Subgrup yang telah dikeluarkan pada tahap sebelumnya: "
                + ", ".join(map(str, dikeluarkan))
            )

        a, b, c = st.columns(3)

        render_kpi(
            a, "📈", "Jenis Peta Kendali", res["chart_type"]
        )

        render_kpi(
            b, "—", "Garis Tengah (CL)", f"{res['p_bar']:.5f}"
        )

        render_kpi(
            c, "⚠", "Jumlah Subgrup Out of Control", str(res["jumlah_ooc"])
        )

        # Grafik peta kendali
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_ctrl["Subgrup"],
            y=df_ctrl["BKA_Aktif"],
            mode="lines",
            name="BKA",
            line=dict(color=MERAH, dash="dash", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=df_ctrl["Subgrup"],
            y=df_ctrl["CL"],
            mode="lines",
            name="CL",
            line=dict(color=HITAM, width=2)
        ))

        fig.add_trace(go.Scatter(
            x=df_ctrl["Subgrup"],
            y=df_ctrl["BKB_Aktif"],
            mode="lines",
            name="BKB",
            line=dict(color=KUNING, dash="dash", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=df_ctrl["Subgrup"],
            y=df_ctrl["p_i"],
            mode="lines+markers",
            name="Proporsi Cacat (pi)",
            line=dict(color=HITAM, width=2),
            marker=dict(size=7)
        ))

        # Menandai titik OOC
        if not ooc.empty:
            fig.add_trace(go.Scatter(
                x=ooc["Subgrup"],
                y=ooc["p_i"],
                mode="markers",
                name="Out of Control",
                marker=dict(
                    color=MERAH,
                    size=12,
                    symbol="diamond"
                )
            ))

        fig.update_layout(
            title=f"{res['chart_type']} — Tahap {tahap_ke}",
            xaxis_title="Subgrup",
            yaxis_title="Proporsi Cacat"
        )

        st.plotly_chart(
            style_plotly(fig),
            use_container_width=True
        )

        # Informasi subgrup OOC
        if not ooc.empty:
            daftar_ooc = ", ".join(
                ooc["Subgrup"].astype(str).tolist()
            )

            st.markdown(
                f"""<div style="background-color: rgba(255, 165, 0, 0.10);
                            border-left: 5px solid #f0a22e;
                            border-radius: 6px;
                            padding: 0.75rem 1rem;
                            font-size: 0.9rem;">
                    ⚠️ &nbsp;<b>Tahap {tahap_ke} belum terkendali secara statistik.</b>
                    Ditemukan {len(ooc)} subgrup <b>Out of Control</b>, yaitu: {daftar_ooc}.
                </div>""",
                unsafe_allow_html=True
            )

        else:
            st.success(
                f"**Proses sudah terkendali secara statistik pada Tahap {tahap_ke}.** "
                f"Seluruh {res['jumlah_ic']} subgrup berada di dalam batas kendali."
            )

    # Ringkasan hasil akhir
    tahap_akhir = tahapan[-1]
    ooc_akhir = tahap_akhir["ooc"]

    st.markdown("---")
    st.markdown("## Ringkasan Hasil Analisis")

    if ooc_akhir.empty:
        st.success(
            f"Proses mencapai kondisi In Control pada "
            f"**Tahap {tahap_akhir['tahap']}**."
        )
    else:
        st.error(
            f"Proses belum terkendali sampai tahap terakhir "
            f"yang dapat dihitung. Masih terdapat "
            f"{len(ooc_akhir)} subgrup Out of Control."
        )

def halaman_runs_test():
    render_header(judul="Uji Keacakan (Runs Test)")
    dasar, _ = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        df_ctrl = get_data_final_in_control()
        df_ctrl, _ = hitung_peta_kendali(df_ctrl)
        rt = hitung_runs_test(df_ctrl["p_i"])
    except Exception as e:
        st.error(str(e))
        return

    alpha = 0.05
    a, b, c, d = st.columns(4)
    render_kpi(a, "M", "Median Proporsi", f"{rt['median']:.5f}")
    render_kpi(b, "V", "Jumlah Runs (V)", str(rt["V"]))
    render_kpi(c, "Z", "Statistik Uji Z", f"{rt['Z']:.4f}")
    render_kpi(d, "P", "P-value", f"{rt['p_value']:.4f}")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    if rt["p_value"] < alpha:
        st.markdown('<div class="interp-box interp-red"><b>Keputusan: Tolak H₀.</b> Data tidak menyebar secara acak (taraf signifikansi α = 0,05).</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="interp-box interp-yellow"><b>Keputusan: Gagal menolak H₀.</b> Tidak terdapat bukti bahwa data menyebar tidak acak (taraf signifikansi α = 0,05).</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["p_i"], mode="lines+markers", name="Proporsi cacat", line=dict(color=MERAH), marker=dict(color=HITAM)))
    fig.add_hline(y=rt["median"], line_dash="dash", line_color=KUNING, annotation_text=f"Median = {rt['median']:.5f}")
    fig.update_layout(title="Proporsi Cacat terhadap Median", xaxis_title="Subgrup", yaxis_title="Proporsi cacat")
    st.plotly_chart(style_plotly(fig), use_container_width=True)

def halaman_kapabilitas():
    render_header(judul="Indeks Kapabilitas Proses")
    dasar, _ = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        _, res = hitung_peta_kendali(dasar)
        z_p, ppk = hitung_ppk_persen(res["p_bar"])
    except Exception as e:
        st.error(str(e))
        return

    a, b, c = st.columns(3)
    render_kpi(a, "p̄", "Proporsi Cacat (p̄)", f"{res['p_bar']:.5f}")
    render_kpi(b, "Z", "Nilai Normal Z(p̄)", f"{z_p:.5f}")
    render_kpi(c, "C", "P%pk", f"{ppk:.5f}")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    ppk_str = format_koma(ppk, 3)
    z_str = format_koma(z_p, 3)
    if ppk >= 1:
        st.markdown(
            f'<div class="interp-box interp-yellow">'
            f'<b>Interpretasi berdasarkan batas P%pk &ge; 1: proses kapabel.</b><br>'
            f'Nilai P%pk sebesar {ppk_str} dan Z sebesar {z_str} menunjukkan bahwa proses sudah kapabel, sehingga kinerja proses perlu terus dipertahankan.'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="interp-box interp-red">'
            f'<b>Interpretasi berdasarkan batas P%pk &lt; 1: proses belum kapabel.</b><br>'
            f'Nilai P%pk sebesar {ppk_str} dan Z sebesar {z_str} menunjukkan bahwa proses belum kapabel, sehingga diperlukan perbaikan untuk menurunkan proporsi cacat dan meningkatkan kapabilitas proses.'
            f'</div>',
            unsafe_allow_html=True
        )

def halaman_level_sigma():
    render_header(judul="Level Sigma")
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return

    # Level Sigma dihitung dari seluruh data yang diunggah (data mentah).
    data_uji = dasar
    total_cacat = int(data_uji["Jumlah Produk Cacat"].sum())
    total_unit = int(data_uji["Jumlah Unit Diperiksa"].sum())

    try:
        dpo, dpmo, sigma = hitung_level_sigma(total_cacat, total_unit, peluang_per_unit=1, shift=1.5)
    except Exception as e:
        st.error(str(e))
        return

    a, b, c, d = st.columns(4)
    render_kpi(a, None, "Total Produk Cacat", format_angka(total_cacat))
    render_kpi(b, None, "DPO", f"{dpo:.5f}")
    render_kpi(c, None, "DPMO", f"{dpmo:,.2f}")
    render_kpi(d, None, "Level Sigma", f"{sigma:.4f}" if np.isfinite(sigma) else "∞")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    dpmo_str = format_koma(dpmo, 3)
    peluang_bulat = format_angka(math.floor(dpmo))
    sigma_str = format_koma(sigma, 2) if np.isfinite(sigma) else "∞"

    if np.isfinite(sigma) and sigma >= 6:
        st.markdown(
            f'<div class="interp-box interp-yellow">'
            f'Hasil perhitungan menunjukkan nilai DPMO sebesar {dpmo_str} dengan level sigma {sigma_str}. '
            f'Artinya, dari satu juta peluang terdapat sekitar {peluang_bulat} peluang terjadinya cacat. '
            f'Nilai ini menunjukkan bahwa proses produksi telah memenuhi target Six Sigma (6σ), sehingga kinerja proses perlu terus dipertahankan.'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="interp-box interp-red">'
            f'Hasil perhitungan menunjukkan nilai DPMO sebesar {dpmo_str} dengan level sigma {sigma_str}. '
            f'Artinya, dari satu juta peluang terdapat sekitar {peluang_bulat} peluang terjadinya cacat. '
            f'Nilai ini menunjukkan bahwa proses produksi masih berada di bawah target Six Sigma (6σ), sehingga perlu dilakukan perbaikan untuk menurunkan jumlah cacat dan meningkatkan level sigma.'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.markdown("### Tabel Level Sigma")
    tabel_sigma = pd.DataFrame({
        "Level Sigma": ["2 sigma", "3 sigma", "4 sigma", "5 sigma", "6 sigma"],
        "DPMO": ["508,538", "66,807", "6,210", "233", "3,4"],
        "Keterangan": [
            "Rata-rata industri Indonesia",
            "Rata-rata industri Indonesia",
            "Rata-rata industri USA",
            "Rata-rata industri USA",
            "Industri kelas dunia"
        ]
    })
    st.dataframe(tabel_sigma, use_container_width=True, hide_index=True)

def buat_gambar_fishbone(data_kategori, masalah_utama="Tingginya Produk Cacat Bata Ringan AAC"):
    fig = go.Figure()

    fig.add_shape(type="line", x0=0.5, y0=5.0, x1=8.3, y1=5.0, line=dict(color=HITAM, width=4))
    fig.add_annotation(
        x=8.45, y=5.0, ax=8.1, ay=5.0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.8, arrowwidth=3, arrowcolor=MERAH
    )

    fig.add_shape(type="rect", x0=8.45, y0=3.5, x1=10.75, y1=6.5, fillcolor=MERAH, line=dict(color=HITAM, width=2))
    teks_kepala = "<br>".join(textwrap.wrap(masalah_utama or "Masalah Utama", width=20))
    fig.add_annotation(
        x=9.6, y=5.0, text=f"<b>{teks_kepala}</b>",
        showarrow=False, font=dict(family="Poppins, sans-serif", color=PUTIH, size=12), align="center"
    )

    posisi_cabang = [
        ("Man (Manusia)", 1.3, 8.8, 2.5, 5.0, True),
        ("Machine (Mesin)", 3.8, 8.8, 5.0, 5.0, True),
        ("Method (Metode)", 6.3, 8.8, 7.5, 5.0, True),
        ("Material (Bahan)", 1.3, 1.2, 2.5, 5.0, False),
        ("Measurement (Pengukuran)", 3.8, 1.2, 5.0, 5.0, False),
        ("Environment (Lingkungan)", 6.3, 1.2, 7.5, 5.0, False),
    ]

    for kat, x_top, y_top, x_spine, y_spine, is_atas in posisi_cabang:
        fig.add_shape(type="line", x0=x_top, y0=y_top, x1=x_spine, y1=y_spine, line=dict(color=HITAM, width=2.5))
        y_box = y_top + 0.45 if is_atas else y_top - 0.45
        fig.add_annotation(
            x=x_top, y=y_box, text=f"<b>{kat}</b>",
            showarrow=False, bgcolor=KUNING if is_atas else HITAM,
            bordercolor=HITAM, borderwidth=1.5, borderpad=6,
            font=dict(family="Poppins, sans-serif", color=HITAM if is_atas else PUTIH, size=11.5)
        )

        sebab_list = data_kategori.get(kat, [])
        for idx, sebab in enumerate(sebab_list[:5]):
            t = (idx + 1) / (min(len(sebab_list), 5) + 1)
            x_titik = x_top + t * (x_spine - x_top)
            y_titik = y_top + t * (y_spine - y_top)
            fig.add_shape(type="line", x0=x_titik - 0.85, y0=y_titik, x1=x_titik, y1=y_titik, line=dict(color=MERAH, width=1.5))
            label_pendek = (sebab[:28] + "...") if len(sebab) > 30 else sebab
            fig.add_annotation(
                x=x_titik - 0.88, y=y_titik, text=label_pendek,
                xanchor="right", showarrow=False,
                font=dict(family="Poppins, sans-serif", color=HITAM, size=10.5)
            )

    fig.update_layout(
        title=dict(text="<b>Diagram Sebab-Akibat (Fishbone) — PT XYZ</b>", font=dict(family="Poppins, sans-serif", color=HITAM)),
        xaxis=dict(range=[0, 11.0], visible=False),
        yaxis=dict(range=[0, 10.0], visible=False),
        paper_bgcolor=PUTIH, plot_bgcolor=PUTIH,
        height=620, margin=dict(l=15, r=15, t=55, b=15)
    )
    return fig

def halaman_fishbone():
    render_header(judul="Diagram Sebab-Akibat (Fishbone)")

    st.markdown('<div class="action-card"><div class="action-header"><div class="action-badge">✎</div><h3 class="action-title">Input Penyebab Kecacatan (5M dan 1E)</h3></div><p class="action-desc">Tuliskan akar penyebab pada masing-masing kategori di bawah ini (pisahkan dengan baris baru / Enter jika lebih dari satu penyebab). Hasil inputan akan otomatis membentuk gambar Diagram Fishbone dan diteruskan ke tabel FMEA.</p></div>', unsafe_allow_html=True)

    masalah_utama = st.text_input(
        "Akibat / Masalah Utama (Kepala Ikan):",
        value=st.session_state.fishbone_problem
    )

    kategori_list = [
        "Man (Manusia)", "Machine (Mesin)", "Method (Metode)",
        "Material (Bahan)", "Measurement (Pengukuran)", "Environment (Lingkungan)"
    ]

    col1, col2 = st.columns(2)
    input_baru = {}
    for i, kat in enumerate(kategori_list):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            input_baru[kat] = st.text_area(
                kat,
                value=st.session_state.fishbone_inputs.get(kat, ""),
                height=105,
                placeholder=f"Ketik penyebab dari faktor {kat.split(' ')[0]}...",
                key=f"fb_input_{kat}"
            )

    if st.button("Buat Gambar Diagram Fishbone & Simpan", use_container_width=True):
        st.session_state.fishbone_problem = masalah_utama
        st.session_state.fishbone_inputs = input_baru
        st.session_state.fishbone_generated = True
        st.markdown('<div class="interp-box interp-yellow">Data penyebab berhasil disimpan. Diagram Fishbone telah dibuat di bawah dan otomatis diteruskan ke menu FMEA.</div>', unsafe_allow_html=True)

    data_parsed = {}
    total_penyebab = 0
    for kat in kategori_list:
        baris = [b.strip() for b in st.session_state.fishbone_inputs.get(kat, "").split("\n") if b.strip()]
        data_parsed[kat] = baris
        total_penyebab += len(baris)

    if st.session_state.fishbone_generated or total_penyebab > 0:
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        fig_fb = buat_gambar_fishbone(data_parsed, masalah_utama=st.session_state.fishbone_problem)
        st.plotly_chart(fig_fb, use_container_width=True)

def kategori_prioritas_rpn(rpn):
    if pd.isna(rpn):
        return "-"
    if rpn >= 12:
        return "Prioritas Tinggi (Segera Diperbaiki)"
    elif rpn >= 6:
        return "Prioritas Sedang (Perlu Pengendalian)"
    else:
        return "Prioritas Rendah (Pemantauan Rutin)"

def halaman_fmea():
    render_header(judul="Failure Mode and Effects Analysis (FMEA)")

    panduan_html = (
        '<div class="action-card">'
        '<div class="action-header"><div class="action-badge">i</div><h3 class="action-title">Panduan Pengisian & Cara Membaca Nilai RPN</h3></div>'
        '<div class="fmea-guide-text">'
        '• <b>Failure Mode / Potensi Kegagalan</b> pada tabel di bawah ditarik secara otomatis dari hasil isian pada halaman <b>Diagram Sebab-Akibat (Fishbone)</b>.<br>'
        '• <b>Severity (S) — Nilai Keseriusan Risiko (5 Tingkatan):</b><br>'
        '&nbsp;&nbsp;&nbsp;1. <b>Low (1):</b> Kerusakan/kerugian kecil (hampir tidak ada kerugian) dan tidak berpengaruh terhadap kualitas produk.<br>'
        '&nbsp;&nbsp;&nbsp;2. <b>Medium (2):</b> Kerusakan/kerugian sedang dan berpengaruh terhadap kualitas produk.<br>'
        '&nbsp;&nbsp;&nbsp;3. <b>High (3):</b> Kerusakan/kerugian tinggi (misal: pesanan pelanggan batal, beberapa mesin rusak) dan berpengaruh terhadap kualitas produk.<br>'
        '&nbsp;&nbsp;&nbsp;4. <b>Extreme (4):</b> Kerusakan/kerugian sangat besar (misal: kebakaran, banjir, bencana, seluruh mesin rusak) dan menyebabkan perusahaan tidak beroperasi lama atau lebih dari satu bulan.<br>'
        '&nbsp;&nbsp;&nbsp;5. <b>Disaster (5):</b> Bencana alam yang menyebabkan <i>total breakdown system</i> (kebangkrutan).<br>'
        '• <b>Occurrence (O) — Tingkat Kemungkinan Terjadinya Frekuensi (4 Tingkatan):</b><br>'
        '&nbsp;&nbsp;&nbsp;1. <b>Low (1):</b> Terjadi &le; 1 kali dalam 6 bulan.<br>'
        '&nbsp;&nbsp;&nbsp;2. <b>Medium (2):</b> Terjadi 2–3 kali dalam 6 bulan.<br>'
        '&nbsp;&nbsp;&nbsp;3. <b>High (3):</b> Terjadi 4–6 kali dalam 6 bulan.<br>'
        '&nbsp;&nbsp;&nbsp;4. <b>Extreme (4):</b> Terjadi &gt; 6 kali dalam 6 bulan.<br>'
        '• <b>Cara Membaca Nilai RPN (Risk Priority Number = Severity × Occurrence, rentang 1–20):</b><br>'
        '&nbsp;&nbsp;&nbsp;Penentuan prioritas dilakukan berdasarkan <b>peringkat nilai RPN tertinggi</b>. Semakin tinggi nilai RPN suatu penyebab kegagalan, maka penyebab tersebut memiliki tingkat risiko paling kritis dan <b>harus paling cepat segera diperbaiki</b>.'
        '</div></div>'
    )
    st.markdown(panduan_html, unsafe_allow_html=True)

    daftar_fishbone = []
    for kat, teks in st.session_state.fishbone_inputs.items():
        for baris in teks.split("\n"):
            if baris.strip():
                daftar_fishbone.append({
                    "Kategori (5M & 1E)": kat.split(" ")[0],
                    "Failure Mode / Penyebab Kegagalan": baris.strip()
                })

    if not daftar_fishbone:
        st.warning("Belum ada data penyebab dari halaman **Diagram Sebab-Akibat (Fishbone)**. Silakan isi penyebab kecacatan pada menu Diagram Sebab-Akibat terlebih dahulu agar otomatis muncul di tabel ini.")
        return

    df_base = pd.DataFrame(daftar_fishbone)

    if not st.session_state.fmea_scores.empty and "Failure Mode / Penyebab Kegagalan" in st.session_state.fmea_scores.columns:
        skor_unik = st.session_state.fmea_scores[
            ["Kategori (5M & 1E)", "Failure Mode / Penyebab Kegagalan", "Dampak Kegagalan", "Severity", "Occurrence", "Usulan Perbaikan"]
        ].drop_duplicates(subset=["Kategori (5M & 1E)", "Failure Mode / Penyebab Kegagalan"])
        df_merged = pd.merge(
            df_base,
            skor_unik,
            on=["Kategori (5M & 1E)", "Failure Mode / Penyebab Kegagalan"],
            how="left"
        )
    else:
        df_merged = df_base.copy()
        df_merged["Dampak Kegagalan"] = ""
        df_merged["Severity"] = 1
        df_merged["Occurrence"] = 1
        df_merged["Usulan Perbaikan"] = ""

    df_merged["Dampak Kegagalan"] = df_merged["Dampak Kegagalan"].fillna("")
    df_merged["Severity"] = df_merged["Severity"].fillna(1).clip(1, 5).astype(int)
    df_merged["Occurrence"] = df_merged["Occurrence"].fillna(1).clip(1, 4).astype(int)
    df_merged["Usulan Perbaikan"] = df_merged["Usulan Perbaikan"].fillna("")
    df_merged["RPN (S × O)"] = df_merged["Severity"] * df_merged["Occurrence"]
    df_merged["Keterangan Prioritas"] = df_merged["RPN (S × O)"].apply(kategori_prioritas_rpn)

    st.markdown("### Input Skor Severity & Occurrence")
    edited_fmea = st.data_editor(
        df_merged,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Kategori (5M & 1E)": st.column_config.TextColumn("Kategori (5M & 1E)", disabled=True),
            "Failure Mode / Penyebab Kegagalan": st.column_config.TextColumn("Failure Mode / Penyebab Kegagalan", disabled=True),
            "Dampak Kegagalan": st.column_config.TextColumn("Dampak Kegagalan (Opsional)"),
            "Severity": st.column_config.NumberColumn("Severity (1–5)", min_value=1, max_value=5, step=1, required=True),
            "Occurrence": st.column_config.NumberColumn("Occurrence (1–4)", min_value=1, max_value=4, step=1, required=True),
            "RPN (S × O)": st.column_config.NumberColumn("RPN (S × O)", disabled=True),
            "Keterangan Prioritas": st.column_config.TextColumn("Keterangan Prioritas", disabled=True),
            "Usulan Perbaikan": st.column_config.TextColumn("Usulan Perbaikan")
        },
        key="editor_fmea_otomatis"
    )

    if st.button("Hitung Nilai RPN & Urutkan Prioritas", use_container_width=True):
        hasil = edited_fmea.copy()
        hasil["RPN (S × O)"] = hasil["Severity"].astype(int) * hasil["Occurrence"].astype(int)
        hasil["Keterangan Prioritas"] = hasil["RPN (S × O)"].apply(kategori_prioritas_rpn)
        st.session_state.fmea_scores = hasil
        st.rerun()

    hasil_akhir = edited_fmea.copy()
    hasil_akhir["RPN (S × O)"] = hasil_akhir["Severity"].astype(int) * hasil_akhir["Occurrence"].astype(int)
    hasil_akhir["Keterangan Prioritas"] = hasil_akhir["RPN (S × O)"].apply(kategori_prioritas_rpn)
    hasil_akhir = hasil_akhir.sort_values("RPN (S × O)", ascending=False).reset_index(drop=True)
    hasil_akhir.insert(0, "Peringkat", np.arange(1, len(hasil_akhir) + 1))

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("### Hasil Prioritas Perbaikan (Diurutkan dari RPN Tertinggi)")
    st.dataframe(hasil_akhir, use_container_width=True, hide_index=True)

    out_fmea = io.BytesIO()
    with pd.ExcelWriter(out_fmea, engine="openpyxl") as writer:
        hasil_akhir.to_excel(writer, index=False, sheet_name="Hasil_FMEA")
    st.download_button(
        "Download Tabel Hasil FMEA (.xlsx)",
        data=out_fmea.getvalue(),
        file_name="Hasil_Analisis_FMEA_PT_XYZ.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

MENU_ITEMS = {
    "Beranda (Input Data)": halaman_beranda,
    "Identifikasi Overdispersi": halaman_overdispersi,
    "Peta Kendali": halaman_peta_kendali,
    "Uji Keacakan (Runs Test)": halaman_runs_test,
    "Indeks Kapabilitas Proses": halaman_kapabilitas,
    "Level Sigma": halaman_level_sigma,
    "Diagram Sebab-Akibat": halaman_fishbone,
    "FMEA": halaman_fmea
}

with st.sidebar:
    pilihan_menu = st.radio("Navigasi", list(MENU_ITEMS.keys()), index=0)

MENU_ITEMS[pilihan_menu]()
