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
    box-sizing: border-box;
}}
.kpi-box.accent-red::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 5px;
    background-color: {MERAH};
}}
.kpi-box.accent-yellow::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 5px;
    background-color: {KUNING};
}}
.kpi-box.accent-dark::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 5px;
    background-color: {HITAM};
}}
.kpi-box.accent-blue::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 5px;
    background-color: {BIRU};
}}
.kpi-icon {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 700;
    color: {PUTIH};
    flex-shrink: 0;
}}
.icon-dark {{ background-color: {HITAM}; }}
.icon-red {{ background-color: {MERAH}; }}
.icon-blue {{ background-color: {BIRU}; }}
.kpi-content {{
    min-width: 0;
    flex: 1;
}}
.kpi-title {{
    font-size: 12.5px;
    font-weight: 600;
    color: {ABU_TEKS};
    margin-bottom: 3px;
    line-height: 1.3;
    white-space: normal;
    word-wrap: break-word;
}}
.kpi-number {{
    font-size: clamp(18px, 1.4vw, 23px);
    font-weight: 800;
    color: {HITAM};
    line-height: 1.2;
    white-space: normal;
    overflow-wrap: anywhere;
}}

/* Kartu Putih Umum */
.action-card {{
    background: {PUTIH};
    border-radius: 14px;
    padding: 18px 22px 14px 22px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    border: 1px solid #E5E7EB;
    margin-bottom: 12px;
}}
.action-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}}
.action-badge {{
    width: 32px;
    height: 32px;
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
    font-size: 16.5px;
    font-weight: 700;
    color: {HITAM};
    margin: 0;
}}
.action-desc {{
    font-size: 13px;
    color: {ABU_TEKS};
    margin-bottom: 8px;
    line-height: 1.55;
}}

/* Kotak Interpretasi Palet 5 Warna */
.interp-box {{
    background: {PUTIH};
    border-radius: 12px;
    padding: 14px 18px;
    color: {HITAM};
    font-size: 13.5px;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    border: 1px solid #E5E7EB;
    margin-bottom: 12px;
}}
.interp-red {{ border-left: 6px solid {MERAH}; }}
.interp-blue {{ border-left: 6px solid {BIRU}; }}
.interp-yellow {{ border-left: 6px solid {KUNING}; }}

/* Perbaikan Kontras Input Label & Text Area */
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

/* Tombol Merah Solid */
div.stButton > button, div.stDownloadButton > button {{
    background-color: {MERAH} !important;
    color: {PUTIH} !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 8px rgba(215, 25, 32, 0.25);
}}
div.stButton > button:hover, div.stDownloadButton > button:hover {{
    background-color: #B01218 !important;
    color: {PUTIH} !important;
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
if "fishbone_generated" not in st.session_state:
    st.session_state.fishbone_generated = False
if "fmea_scores" not in st.session_state:
    st.session_state.fmea_scores = pd.DataFrame()

CALENDAR_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1A1C20" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>'

def render_header(judul="Six Sigma Dashboard", subjudul="Analisis Kualitas Produksi Bata Ringan AAC – PT XYZ"):
    df = st.session_state.df_produksi
    if df is not None and not df.empty:
        tgl_awal = df["Tanggal"].min().strftime("%b %Y")
        tgl_akhir = df["Tanggal"].max().strftime("%b %Y")
        periode_teks = f"{tgl_awal} – {tgl_akhir}" if tgl_awal != tgl_akhir else tgl_awal
    else:
        periode_teks = "Menunggu Data"

    html = (
        f'<div class="dashboard-header">'
        f'<div class="header-left">'
        f'<div class="header-stripe"></div>'
        f'<div><h1 class="header-title">{judul}</h1><p class="header-subtitle">{subjudul}</p></div>'
        f'</div>'
        f'<div class="period-badge">{CALENDAR_SVG} <span>Periode Analisis: {periode_teks}</span></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_kpi(kolom, ikon, warna_ikon, aksen_bawah, label, nilai):
    html = (
        f'<div class="kpi-box {aksen_bawah}">'
        f'<div class="kpi-icon {warna_ikon}">{ikon}</div>'
        f'<div class="kpi-content"><div class="kpi-title">{label}</div><div class="kpi-number">{nilai}</div></div>'
        f'</div>'
    )
    kolom.markdown(html, unsafe_allow_html=True)

def format_angka(x):
    return f"{x:,.0f}".replace(",", ".")

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
    return df.sort_values("Tanggal").reset_index(drop=True)

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
    aktif = dasar.loc[~dasar["Subgrup"].isin(dikeluarkan)].copy()
    return dasar, aktif

def hitung_peta_kendali(df_input):
    """Menghitung batas kendali P-Chart dan Laney P' sesuai rumus Excel skripsi."""
    df = df_input.copy()
    if len(df) < 2:
        raise ValueError("Minimal diperlukan dua subgrup untuk menghitung moving range.")
    if "Subgrup" not in df:
        df["Subgrup"] = np.arange(1, len(df) + 1)

    df["p_i"] = df["Jumlah Produk Cacat"] / df["Jumlah Unit Diperiksa"]
    p_bar = float(df["Jumlah Produk Cacat"].sum() / df["Jumlah Unit Diperiksa"].sum())
    df["sigma_pi"] = np.sqrt(p_bar * (1 - p_bar) / df["Jumlah Unit Diperiksa"])
    if (df["sigma_pi"] == 0).any():
        raise ValueError("Simpangan baku proporsi bernilai nol; periksa proporsi cacat.")
    df["z_i"] = (df["p_i"] - p_bar) / df["sigma_pi"]

    df = df.sort_values("Subgrup").reset_index(drop=True)
    df["R_i"] = df["z_i"].diff().abs()
    valid_mr = df["R_i"].dropna()
    R_bar = float(valid_mr.mean()) if len(valid_mr) else 0.0
    sigma_z = R_bar / 1.128
    overdispersi = sigma_z > 1

    df["BKA_P"] = np.minimum(1, p_bar + 3 * df["sigma_pi"])
    df["BKB_P"] = np.maximum(0, p_bar - 3 * df["sigma_pi"])
    df["BKA_Laney"] = np.minimum(1, p_bar + 3 * sigma_z * df["sigma_pi"])
    df["BKB_Laney"] = np.maximum(0, p_bar - 3 * sigma_z * df["sigma_pi"])

    if overdispersi:
        df["BKA_Aktif"] = df["BKA_Laney"]
        df["BKB_Aktif"] = df["BKB_Laney"]
        jenis = "Peta Kendali Laney P'"
    else:
        df["BKA_Aktif"] = df["BKA_P"]
        df["BKB_Aktif"] = df["BKB_P"]
        jenis = "Peta Kendali P"

    df["CL"] = p_bar
    df["Status_OOC"] = (df["p_i"] > df["BKA_Aktif"]) | (df["p_i"] < df["BKB_Aktif"])
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

def hitung_runs_test(series):
    x = np.asarray(series, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        raise ValueError("Runs Test memerlukan minimal tiga pengamatan valid.")
    median = float(np.median(x))
    tanda = np.where(x > median, 1, np.where(x < median, -1, 0))
    tanda = tanda[tanda != 0]
    n1 = int(np.sum(tanda == 1))
    n2 = int(np.sum(tanda == -1))
    if n1 == 0 or n2 == 0:
        raise ValueError("Runs Test tidak dapat dihitung karena salah satu kelompok kosong.")
    V = int(1 + np.sum(tanda[1:] != tanda[:-1]))
    n = n1 + n2
    mu = (2 * n1 * n2) / n + 1
    var = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (n**2 * (n - 1))
    sd = float(np.sqrt(var))
    z = (V - mu) / sd
    p_value = float(2 * (1 - norm.cdf(abs(z))))
    return {
        "median": median, "n1": n1, "n2": n2, "V": V,
        "mu_V": mu, "sigma_V": sd, "Z": z, "p_value": p_value
    }

def hitung_ppk_persen(p_bar):
    if not 0 < p_bar < 1:
        raise ValueError("Proporsi cacat harus berada di antara 0 dan 1.")
    z_p = float(norm.ppf(1 - p_bar))
    return z_p, z_p / 3

def hitung_level_sigma(jumlah_cacat, jumlah_unit, peluang_per_unit=1, shift=1.5):
    if jumlah_unit <= 0 or peluang_per_unit <= 0:
        raise ValueError("Jumlah unit dan peluang cacat per unit harus lebih besar dari 0.")
    dpo = jumlah_cacat / (jumlah_unit * peluang_per_unit)
    dpmo = dpo * 1_000_000
    if dpmo <= 0:
        sigma = float("inf")
    elif dpmo >= 1_000_000:
        sigma = float("-inf")
    else:
        sigma = float(norm.ppf(1 - dpmo / 1_000_000) + shift)
    return dpo, dpmo, sigma

def halaman_beranda():
    render_header(
        judul="Six Sigma Dashboard",
        subjudul="Analisis Kualitas Produksi Bata Ringan AAC – PT XYZ"
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
    render_kpi(k1, "📦", "icon-dark", "accent-red", "Total Unit Diperiksa", format_angka(total_unit))
    render_kpi(k2, "❗", "icon-red", "accent-red", "Total Produk Cacat", format_angka(total_cacat))
    render_kpi(k3, "%", "icon-dark", "accent-yellow", "Persentase Cacat", f"{persen:.2f}%")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_kiri, col_kanan = st.columns(2)
    with col_kiri:
        st.markdown('<div class="action-card"><div class="action-header"><div class="action-badge">⬇</div><h3 class="action-title">Template Data Excel</h3></div><p class="action-desc">Unduh template untuk memasukkan data produksi dan kecacatan sesuai format standar.</p></div>', unsafe_allow_html=True)
        st.download_button(
            "Download Template.xlsx",
            data=buat_template_excel(),
            file_name="Template_Data_Produksi_AAC.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_kanan:
        st.markdown('<div class="action-card"><div class="action-header"><div class="action-badge">☁</div><h3 class="action-title">Unggah Data</h3></div><p class="action-desc">Upload file Excel (.xlsx) yang sudah diisi sesuai template untuk memulai analisis.</p></div>', unsafe_allow_html=True)
        file = st.file_uploader(
            "Pilih file Excel (.xlsx)",
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

    if st.session_state.df_produksi is not None:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("### Pratinjau Data Produksi")
        tampil = st.session_state.df_produksi.copy()
        tampil.insert(0, "Subgrup", np.arange(1, len(tampil) + 1))
        tampil["Tanggal"] = tampil["Tanggal"].dt.strftime("%Y-%m-%d")
        st.dataframe(tampil, use_container_width=True, hide_index=True)

def halaman_overdispersi():
    render_header(
        judul="Identifikasi Overdispersi",
        subjudul="Evaluasi Kondisi Overdispersi & Pemilihan Jenis Peta Kendali"
    )
    dasar, _ = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        _, res = hitung_peta_kendali(dasar)
    except Exception as e:
        st.error(str(e))
        return

    a, b, c, d = st.columns(4)
    render_kpi(a, "p̄", "icon-dark", "accent-dark", "Rata-rata Proporsi (p̄)", f"{res['p_bar']:.4f}")
    render_kpi(b, "R̄", "icon-dark", "accent-red", "Rata-rata Moving Range (R̄)", f"{res['R_bar']:.4f}")
    render_kpi(c, "σz", "icon-dark", "accent-yellow", "Sigma Z (R̄ / 1,128)", f"{res['sigma_z']:.4f}")
    render_kpi(d, "✓", "icon-red", "accent-yellow", "Keputusan", "Overdispersi" if res["is_overdispersed"] else "Tidak Overdispersi")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    if res["is_overdispersed"]:
        st.markdown(f'<div class="interp-box interp-yellow">Nilai Sigma Z = <b>{res["sigma_z"]:.4f} &gt; 1</b>, sehingga data mengalami overdispersi. Jenis peta kendali yang dipilih: <b>{res["chart_type"]}</b>.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="interp-box interp-blue">Nilai Sigma Z = <b>{res["sigma_z"]:.4f} &le; 1</b>, sehingga data tidak mengalami overdispersi. Jenis peta kendali yang dipilih: <b>{res["chart_type"]}</b>.</div>', unsafe_allow_html=True)

def halaman_peta_kendali():
    render_header(
        judul="Analisis Peta Kendali",
        subjudul="Pemantauan & Revisi Bertahap Hingga Seluruh Subgrup In Control"
    )
    if st.session_state.df_produksi is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return

    dasar = st.session_state.df_produksi.copy()
    dasar["Subgrup"] = np.arange(1, len(dasar) + 1)

    if st.session_state.riwayat_iterasi:
        col_info, col_reset = st.columns([4, 1])
        with col_info:
            st.markdown(f'<div class="interp-box interp-blue">Menampilkan <b>{len(st.session_state.riwayat_iterasi) + 1} tahap</b> analisis peta kendali.</div>', unsafe_allow_html=True)
        with col_reset:
            if st.button("Reset ke Tahap 1", use_container_width=True):
                st.session_state.riwayat_iterasi = []
                st.session_state.excluded_subgroups = []
                st.rerun()

    semua_tahap = [[]]
    kumulatif = []
    for dikeluarkan_tahap in st.session_state.riwayat_iterasi:
        kumulatif = kumulatif + dikeluarkan_tahap
        semua_tahap.append(list(kumulatif))

    for idx, dikeluarkan in enumerate(semua_tahap):
        tahap_ke = idx + 1
        is_tahap_terakhir = (idx == len(semua_tahap) - 1)
        df_tahap = dasar.loc[~dasar["Subgrup"].isin(dikeluarkan)].copy()

        st.markdown("---")
        st.markdown(f"## Peta Kendali — Tahap {tahap_ke}")
        if dikeluarkan:
            st.caption(f"Subgrup yang telah dikeluarkan hingga tahap ini: **{', '.join(map(str, dikeluarkan))}**")

        try:
            df_ctrl, res = hitung_peta_kendali(df_tahap)
        except Exception as e:
            st.error(f"Tahap {tahap_ke} tidak dapat dihitung: {e}")
            break

        a, b, c = st.columns(3)
        render_kpi(a, "📈", "icon-dark", "accent-dark", f"Jenis Peta (Tahap {tahap_ke})", res["chart_type"])
        render_kpi(b, "—", "icon-dark", "accent-yellow", "Garis Tengah (CL)", f"{res['p_bar']:.5f}")
        render_kpi(c, "⚠", "icon-red", "accent-red", "Subgrup Out of Control", str(res["jumlah_ooc"]))

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["BKA_Aktif"], mode="lines", name="BKA", line=dict(color=MERAH, dash="dash", width=2)))
        fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["CL"], mode="lines", name="CL", line=dict(color=BIRU, width=2)))
        fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["BKB_Aktif"], mode="lines", name="BKB", line=dict(color=KUNING, dash="dash", width=2)))
        fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["p_i"], mode="lines+markers", name="Proporsi cacat (pi)", line=dict(color=HITAM), marker=dict(size=7)))

        ooc = df_ctrl[df_ctrl["Status_OOC"]]
        if not ooc.empty:
            fig.add_trace(go.Scatter(x=ooc["Subgrup"], y=ooc["p_i"], mode="markers", name="Out of Control", marker=dict(color=MERAH, size=12, symbol="diamond")))

        fig.update_layout(title=f"{res['chart_type']} — Tahap {tahap_ke}", xaxis_title="Subgrup", yaxis_title="Proporsi cacat")
        st.plotly_chart(style_plotly(fig), use_container_width=True)

        if is_tahap_terakhir:
            if ooc.empty:
                st.markdown(f'<div class="interp-box interp-blue"><b>Proses Sudah Terkendali Statistik pada Tahap {tahap_ke}!</b> Seluruh subgrup ({res["jumlah_ic"]} subgrup) berada di dalam batas kendali.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="interp-box interp-red">Masih ditemukan <b>{res["jumlah_ooc"]} subgrup Out of Control</b> pada Tahap {tahap_ke}: Subgrup <b>{", ".join(ooc["Subgrup"].astype(str).tolist())}</b>.</div>', unsafe_allow_html=True)
                ooc_tampil = ooc[["Subgrup", "Tanggal", "Jumlah Produk Cacat", "Jumlah Unit Diperiksa", "p_i", "BKA_Aktif", "BKB_Aktif"]].copy()
                ooc_tampil["Tanggal"] = pd.to_datetime(ooc_tampil["Tanggal"]).dt.strftime("%Y-%m-%d")
                st.dataframe(ooc_tampil, use_container_width=True, hide_index=True)

                pilihan_ooc = st.multiselect(
                    f"Pilih subgrup OOC Tahap {tahap_ke} yang memiliki penyebab khusus untuk dikeluarkan:",
                    options=ooc["Subgrup"].astype(int).tolist(),
                    default=ooc["Subgrup"].astype(int).tolist(),
                    key=f"pilih_ooc_tahap_{tahap_ke}"
                )
                alasan = st.text_input(
                    f"Catatan penyebab khusus (Tahap {tahap_ke}):",
                    placeholder="Contoh: Kerusakan mesin potong / variasi bahan baku",
                    key=f"alasan_tahap_{tahap_ke}"
                )

                if st.button(f"Lanjut Analisis Peta Kendali Tahap {tahap_ke + 1}", key=f"btn_lanjut_{tahap_ke}", disabled=(not pilihan_ooc)):
                    st.session_state.riwayat_iterasi.append([int(x) for x in pilihan_ooc])
                    for sg in pilihan_ooc:
                        tgl = ooc.loc[ooc["Subgrup"] == sg, "Tanggal"].iloc[0]
                        st.session_state.excluded_subgroups.append({
                            "Subgrup": int(sg),
                            "Tanggal": str(pd.Timestamp(tgl).date()),
                            "Alasan": alasan.strip() if alasan.strip() else f"Penyebab khusus (Revisi Tahap {tahap_ke})"
                        })
                    st.rerun()

def halaman_runs_test():
    render_header(
        judul="Uji Keacakan (Runs Test)",
        subjudul="Pengujian Pola Acak Proporsi Cacat Produksi"
    )
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        df_ctrl, _ = hitung_peta_kendali(aktif)
        rt = hitung_runs_test(df_ctrl["p_i"])
    except Exception as e:
        st.error(str(e))
        return

    alpha = st.number_input("Taraf signifikansi (α)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
    a, b, c, d = st.columns(4)
    render_kpi(a, "M", "icon-dark", "accent-dark", "Median Proporsi", f"{rt['median']:.5f}")
    render_kpi(b, "V", "icon-dark", "accent-yellow", "Jumlah Runs (V)", str(rt["V"]))
    render_kpi(c, "Z", "icon-dark", "accent-yellow", "Statistik Uji Z", f"{rt['Z']:.4f}")
    render_kpi(d, "P", "icon-red", "accent-red", "P-value", f"{rt['p_value']:.4f}")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    if rt["p_value"] < alpha:
        st.markdown('<div class="interp-box interp-red"><b>Keputusan: Tolak H₀.</b> Data tidak menyebar secara acak.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="interp-box interp-blue"><b>Keputusan: Gagal menolak H₀.</b> Tidak terdapat bukti bahwa data menyebar tidak acak.</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["p_i"], mode="lines+markers", name="Proporsi cacat", line=dict(color=MERAH), marker=dict(color=BIRU)))
    fig.add_hline(y=rt["median"], line_dash="dash", line_color=KUNING, annotation_text=f"Median = {rt['median']:.5f}")
    fig.update_layout(title="Proporsi Cacat terhadap Median", xaxis_title="Subgrup", yaxis_title="Proporsi cacat")
    st.plotly_chart(style_plotly(fig), use_container_width=True)

def halaman_kapabilitas():
    render_header(
        judul="Indeks Kapabilitas Proses",
        subjudul="Pengukuran Kapabilitas Data Atribut (P%pk)"
    )
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        _, res = hitung_peta_kendali(aktif)
        z_p, ppk = hitung_ppk_persen(res["p_bar"])
    except Exception as e:
        st.error(str(e))
        return

    a, b, c = st.columns(3)
    render_kpi(a, "p̄", "icon-dark", "accent-dark", "Proporsi Cacat (p̄)", f"{res['p_bar']:.5f}")
    render_kpi(b, "Z", "icon-dark", "accent-yellow", "Nilai Normal Z(p̄)", f"{z_p:.5f}")
    render_kpi(c, "C", "icon-red", "accent-red", "P%pk", f"{ppk:.5f}")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.latex(r"P\%_{pk} = \frac{Z(\bar{p})}{3}")
    if ppk >= 1:
        st.markdown('<div class="interp-box interp-blue"><b>Interpretasi berdasarkan batas P%pk &ge; 1: proses kapabel.</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="interp-box interp-red"><b>Interpretasi berdasarkan batas P%pk &lt; 1: proses belum kapabel.</b></div>', unsafe_allow_html=True)

def halaman_level_sigma():
    render_header(
        judul="Level Sigma",
        subjudul="Perhitungan DPO, DPMO, dan Nilai Sigma Proses Produksi"
    )
    dasar, _ = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return

    total_cacat = int(dasar["Jumlah Produk Cacat"].sum())
    total_unit = int(dasar["Jumlah Unit Diperiksa"].sum())

    try:
        dpo, dpmo, sigma = hitung_level_sigma(total_cacat, total_unit, peluang_per_unit=1, shift=1.5)
    except Exception as e:
        st.error(str(e))
        return

    a, b, c, d = st.columns(4)
    render_kpi(a, "❗", "icon-red", "accent-red", "Total Produk Cacat", format_angka(total_cacat))
    render_kpi(b, "D", "icon-dark", "accent-dark", "DPO", f"{dpo:.5f}")
    render_kpi(c, "M", "icon-dark", "accent-yellow", "DPMO", f"{dpmo:,.2f}")
    render_kpi(d, "Σ", "icon-red", "accent-yellow", "Level Sigma", f"{sigma:.4f}" if np.isfinite(sigma) else "∞")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.latex(r"DPO = \frac{\text{Jumlah cacat}}{\text{Unit diperiksa} \times \text{Peluang per unit}}")
    st.latex(r"DPMO = DPO \times 10^6")
    st.latex(r"\text{Level Sigma} = \Phi^{-1}\left(1-\frac{DPMO}{10^6}\right)+1{,}5")

def buat_gambar_fishbone(data_kategori, masalah_utama="Tingginya Produk Cacat Bata Ringan AAC"):
    fig = go.Figure()

    fig.add_shape(type="line", x0=0.5, y0=5.0, x1=8.3, y1=5.0, line=dict(color=HITAM, width=4))
    fig.add_annotation(
        x=8.45, y=5.0, ax=8.1, ay=5.0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.8, arrowwidth=3, arrowcolor=MERAH
    )

    fig.add_shape(type="rect", x0=8.45, y0=3.7, x1=10.6, y1=6.3, fillcolor=MERAH, line=dict(color=HITAM, width=2))
    teks_kepala = "<br>".join([masalah_utama[i:i+20] for i in range(0, len(masalah_utama), 20)])
    fig.add_annotation(
        x=9.52, y=5.0, text=f"<b>{teks_kepala}</b>",
        showarrow=False, font=dict(family="Poppins, sans-serif", color=PUTIH, size=12.5), align="center"
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
        xaxis=dict(range=[0, 10.9], visible=False),
        yaxis=dict(range=[0, 10.0], visible=False),
        paper_bgcolor=PUTIH, plot_bgcolor=PUTIH,
        height=620, margin=dict(l=15, r=15, t=55, b=15)
    )
    return fig

def halaman_fishbone():
    render_header(
        judul="Diagram Sebab-Akibat (Fishbone)",
        subjudul="Identifikasi Akar Penyebab Kecacatan Berdasarkan Kategori 5M dan 1E"
    )

    st.markdown('<div class="action-card"><div class="action-header"><div class="action-badge">✎</div><h3 class="action-title">Input Penyebab Kecacatan (5M dan 1E)</h3></div><p class="action-desc">Tuliskan akar penyebab pada masing-masing kategori di bawah ini (pisahkan dengan baris baru / Enter jika lebih dari satu penyebab). Hasil inputan akan otomatis membentuk gambar Diagram Fishbone dan diteruskan ke tabel FMEA.</p></div>', unsafe_allow_html=True)

    masalah_utama = st.text_input(
        "Akibat / Masalah Utama (Kepala Ikan):",
        value="Tingginya Produk Cacat Bata Ringan AAC"
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
                f"📌 {kat}",
                value=st.session_state.fishbone_inputs.get(kat, ""),
                height=105,
                placeholder=f"Ketik penyebab dari faktor {kat.split(' ')[0]}...",
                key=f"fb_input_{kat}"
            )

    if st.button("Buat Gambar Diagram Fishbone & Simpan", use_container_width=True):
        st.session_state.fishbone_inputs = input_baru
        st.session_state.fishbone_generated = True
        st.markdown('<div class="interp-box interp-blue">Data penyebab berhasil disimpan. Diagram Fishbone telah dibuat di bawah dan otomatis diteruskan ke menu FMEA.</div>', unsafe_allow_html=True)

    data_parsed = {}
    total_penyebab = 0
    for kat in kategori_list:
        baris = [b.strip() for b in st.session_state.fishbone_inputs.get(kat, "").split("\n") if b.strip()]
        data_parsed[kat] = baris
        total_penyebab += len(baris)

    if st.session_state.fishbone_generated or total_penyebab > 0:
        st.markdown("---")
        fig_fb = buat_gambar_fishbone(data_parsed, masalah_utama=masalah_utama)
        st.plotly_chart(fig_fb, use_container_width=True)

def kategori_prioritas_rpn(rpn):
    if pd.isna(rpn):
        return "-"
    if rpn >= 50:
        return "Prioritas Tinggi (Segera Diperbaiki)"
    elif rpn >= 25:
        return "Prioritas Sedang (Perlu Pengendalian)"
    else:
        return "Prioritas Rendah (Pemantauan Rutin)"

def halaman_fmea():
    render_header(
        judul="Failure Mode and Effects Analysis (FMEA)",
        subjudul="Penilaian Risiko & Penentuan Prioritas Perbaikan Berdasarkan Nilai RPN"
    )

    st.markdown(
        '<div class="action-card">'
        '<div class="action-header"><div class="action-badge">ℹ</div><h3 class="action-title">Panduan Pengisian & Cara Membaca Nilai RPN</h3></div>'
        '<p class="action-desc">'
        '• <b>Failure Mode / Potensi Kegagalan</b> di bawah ini ditarik secara otomatis dari hasil isian pada halaman <b>Diagram Sebab-Akibat (Fishbone)</b>.<br>'
        '• <b>Severity (S) [Skala 1–10]:</b> Tingkat keparahan dampak kecacatan terhadap kualitas produk maupun proses produksi berikutnya (<i>1 = dampak sangat ringan/tidak terasa, 10 = dampak sangat fatal/produk ditolak total</i>).<br>'
        '• <b>Occurrence (O) [Skala 1–10]:</b> Tingkat keseringan atau peluang munculnya penyebab kegagalan selama proses produksi (<i>1 = sangat jarang terjadi, 10 = hampir selalu terjadi</i>).<br>'
        '• <b>Cara Membaca Nilai RPN (Risk Priority Number = Severity × Occurrence, rentang 1–100):</b> Semakin tinggi nilai RPN, semakin kritis risiko kegagalan tersebut dan harus menjadi <b>prioritas utama perbaikan</b> (<i>&ge; 50: Prioritas Tinggi | 25–49: Prioritas Sedang | &lt; 25: Prioritas Rendah</i>).'
        '</p></div>',
        unsafe_allow_html=True
    )

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
        df_merged = pd.merge(
            df_base,
            st.session_state.fmea_scores[["Failure Mode / Penyebab Kegagalan", "Dampak Kegagalan", "Severity", "Occurrence", "Usulan Perbaikan"]],
            on="Failure Mode / Penyebab Kegagalan",
            how="left"
        )
    else:
        df_merged = df_base.copy()
        df_merged["Dampak Kegagalan"] = ""
        df_merged["Severity"] = 1
        df_merged["Occurrence"] = 1
        df_merged["Usulan Perbaikan"] = ""

    df_merged["Dampak Kegagalan"] = df_merged["Dampak Kegagalan"].fillna("")
    df_merged["Severity"] = df_merged["Severity"].fillna(1).astype(int)
    df_merged["Occurrence"] = df_merged["Occurrence"].fillna(1).astype(int)
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
            "Severity": st.column_config.NumberColumn("Severity (1–10)", min_value=1, max_value=10, step=1, required=True),
            "Occurrence": st.column_config.NumberColumn("Occurrence (1–10)", min_value=1, max_value=10, step=1, required=True),
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

    st.markdown("---")
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
    "🏠  Beranda (Input Data)": halaman_beranda,
    "📊  Identifikasi Overdispersi": halaman_overdispersi,
    "📈  Peta Kendali": halaman_peta_kendali,
    "🔀  Uji Keacakan (Runs Test)": halaman_runs_test,
    "⏱️  Indeks Kapabilitas Proses": halaman_kapabilitas,
    "Σ   Level Sigma": halaman_level_sigma,
    "🐟  Diagram Sebab-Akibat": halaman_fishbone,
    "📋  FMEA": halaman_fmea
}

with st.sidebar:
    st.markdown('<div class="sidebar-logo"><div class="logo-title">PT XYZ</div></div>', unsafe_allow_html=True)
    pilihan_menu = st.radio("Navigasi", list(MENU_ITEMS.keys()), index=0)

MENU_ITEMS[pilihan_menu]()
