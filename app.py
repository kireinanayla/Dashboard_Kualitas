# ==============================================================================
# APLIKASI DASHBOARD SIX SIGMA - PT XYZ
# ==============================================================================
import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(
    page_title="Analisis Kualitas Produksi AAC - PT XYZ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

MERAH = "#D71920"
KUNING = "#F5C518"
HITAM = "#171717"
PUTIH = "#FFFFFF"
BIRU = "#2563EB"
ABU = "#F3F4F6"

st.markdown(f"""
<style>
.stApp {{ background: {ABU}; color: {HITAM}; }}
[data-testid="stSidebar"] {{ background: {HITAM}; }}
[data-testid="stSidebar"] * {{ color: {PUTIH}; }}
.block-container {{ padding-top: 1.4rem; }}
.main-title {{ border-left: 7px solid {MERAH}; padding-left: 16px; margin-bottom: 1.2rem; }}
.main-title h1 {{ color: {HITAM}; font-weight: 800; margin-bottom: 0.1rem; }}
.main-title p {{ color: #555; margin-top: 0; }}
.kpi-card {{
  background: {PUTIH}; border-radius: 12px; padding: 18px;
  border: 1px solid #E5E7EB; border-bottom: 5px solid {MERAH};
  box-shadow: 0 2px 8px rgba(0,0,0,.05); min-height: 112px;
}}
.kpi-card.yellow {{ border-bottom-color: {KUNING}; }}
.kpi-card.blue {{ border-bottom-color: {BIRU}; }}
.kpi-card.dark {{ border-bottom-color: {HITAM}; }}
.kpi-label {{ color: #60646C; font-size: 13px; font-weight: 650; }}
.kpi-value {{ color: {HITAM}; font-size: 27px; font-weight: 800; margin-top: 5px; }}
div.stButton > button, div.stDownloadButton > button {{
  background: {MERAH}; color: white; border: 0; border-radius: 8px; font-weight: 650;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover {{
  background: {HITAM}; color: white; border: 0;
}}
h1, h2, h3 {{ color: {HITAM}; }}
</style>
""", unsafe_allow_html=True)

if "df_produksi" not in st.session_state:
    st.session_state.df_produksi = None
if "excluded_subgroups" not in st.session_state:
    st.session_state.excluded_subgroups = []
if "fishbone_data" not in st.session_state:
    st.session_state.fishbone_data = pd.DataFrame(
        columns=["Kategori", "Penyebab"]
    )
if "fmea_data" not in st.session_state:
    st.session_state.fmea_data = pd.DataFrame(
        columns=["Potensi Kegagalan", "Dampak Kegagalan",
                 "Penyebab Kegagalan", "Severity", "Occurrence",
                 "RPN", "Usulan Perbaikan"]
    )

def header_halaman(judul, subjudul=None):
    sub = f"<p>{subjudul}</p>" if subjudul else ""
    st.markdown(
        f'<div class="main-title"><h1>{judul}</h1>{sub}</div>',
        unsafe_allow_html=True
    )

def kartu_kpi(kolom, label, nilai, aksen="red"):
    kelas = {"red": "", "yellow": "yellow", "blue": "blue", "dark": "dark"}.get(aksen, "")
    kolom.markdown(
        f'<div class="kpi-card {kelas}"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{nilai}</div></div>',
        unsafe_allow_html=True
    )

def format_angka(x):
    return f"{x:,.0f}".replace(",", ".")

def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor=PUTIH, plot_bgcolor=PUTIH,
        font=dict(color=HITAM),
        margin=dict(l=25, r=20, t=55, b=25),
        legend=dict(orientation="h", y=1.12)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB")
    fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB")
    return fig

# ==============================================================================
# FUNGSI UMUM DAN PERHITUNGAN STATISTIK
# ==============================================================================
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
    """Menghitung batas kendali P-Chart dan Laney P' sesuai kondisi data."""
    df = df_input.copy()
    if len(df) < 2:
        raise ValueError("Minimal diperlukan dua subgrup untuk menghitung moving range.")
    if "Subgrup" not in df:
        df["Subgrup"] = np.arange(1, len(df) + 1)

    df["p_i"] = df["Jumlah Produk Cacat"] / df["Jumlah Unit Diperiksa"]
    p_bar = float(df["p_i"].mean())
    df["sigma_pi"] = np.sqrt(
        p_bar * (1 - p_bar) / df["Jumlah Unit Diperiksa"]
    )
    if (df["sigma_pi"] == 0).any():
        raise ValueError("Simpangan baku proporsi bernilai nol; periksa proporsi cacat.")
    df["z_i"] = (df["p_i"] - p_bar) / df["sigma_pi"]

    df = df.sort_values("Subgrup").copy()
    selisih_subgrup = df["Subgrup"].diff()
    df["R_i"] = df["z_i"].diff().abs().where(selisih_subgrup == 1)
    valid_mr = df["R_i"].dropna()
    R_bar = float(valid_mr.mean()) if len(valid_mr) else 0.0
    faktor_penyesuai = R_bar / 1.128
    overdispersi = faktor_penyesuai > 1

    df["BKA_P"] = np.minimum(1, p_bar + 3 * df["sigma_pi"])
    df["BKB_P"] = np.maximum(0, p_bar - 3 * df["sigma_pi"])
    df["BKA_Laney"] = np.minimum(1, p_bar + 3 * faktor_penyesuai * df["sigma_pi"])
    df["BKB_Laney"] = np.maximum(0, p_bar - 3 * faktor_penyesuai * df["sigma_pi"])

    if overdispersi:
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

def hitung_level_sigma(jumlah_cacat, jumlah_unit, peluang_per_unit, shift=1.5):
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

# ==============================================================================
# HALAMAN 1: BERANDA
# ==============================================================================
def halaman_beranda():
    header_halaman("Analisis Kualitas Produksi Bata Ringan AAC", "PT XYZ")
    kiri, kanan = st.columns([1, 1.6])
    with kiri:
        st.markdown("### Template Data Excel")
        st.write("Unduh template, lalu isi data produksi sesuai nama kolom yang tersedia.")
        st.download_button(
            "⬇️ Download Template Excel",
            data=buat_template_excel(),
            file_name="Template_Data_Produksi_AAC.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with kanan:
        st.markdown("### Unggah Data")
        file = st.file_uploader(
            "Pilih file Excel (.xlsx)", type=["xlsx"], key="file_produksi"
        )
        if file is not None:
            try:
                data_baru = validasi_data_produksi(pd.read_excel(file))
                st.session_state.df_produksi = data_baru
                st.session_state.excluded_subgroups = []
                st.success(f"Data berhasil dibaca: {len(data_baru)} subgrup.")
            except Exception as e:
                st.error(f"File belum dapat digunakan: {e}")

    if st.session_state.df_produksi is None:
        st.info("Unggah data produksi untuk menampilkan ringkasan dan analisis.")
        return

    df = st.session_state.df_produksi.copy()
    total_unit = int(df["Jumlah Unit Diperiksa"].sum())
    total_cacat = int(df["Jumlah Produk Cacat"].sum())
    persen = total_cacat / total_unit * 100 if total_unit else 0

    st.markdown("### Ringkasan Produksi")
    a, b, c = st.columns(3)
    kartu_kpi(a, "Total Unit Diperiksa", format_angka(total_unit), "dark")
    kartu_kpi(b, "Total Produk Cacat", format_angka(total_cacat), "red")
    kartu_kpi(c, "Persentase Cacat", f"{persen:.2f}%", "yellow")

    st.markdown("### Tren Persentase Produk Cacat")
    tren = df.copy()
    tren["Persentase Cacat (%)"] = (
        tren["Jumlah Produk Cacat"] / tren["Jumlah Unit Diperiksa"] * 100
    )
    fig = px.line(
        tren, x="Tanggal", y="Persentase Cacat (%)", markers=True,
        color_discrete_sequence=[MERAH]
    )
    fig.update_traces(marker=dict(size=7, color=BIRU), line=dict(width=3))
    st.plotly_chart(style_plotly(fig), use_container_width=True)

    st.markdown("### Ringkasan Hasil Analisis")
    try:
        _, hasil = hitung_peta_kendali(df.assign(Subgrup=np.arange(1, len(df) + 1)))
        rt = hitung_runs_test(
            (df["Jumlah Produk Cacat"] / df["Jumlah Unit Diperiksa"])
        )
        _, ppk = hitung_ppk_persen(hasil["p_bar"])
        peluang = st.session_state.get("peluang_per_unit", 1)
        _, _, sigma = hitung_level_sigma(total_cacat, total_unit, peluang)
        r1, r2, r3, r4 = st.columns(4)
        kartu_kpi(r1, "Indikator Overdispersi", "Terjadi" if hasil["is_overdispersed"] else "Tidak", "yellow")
        kartu_kpi(r2, "Runs Test (p-value)", f"{rt['p_value']:.4f}", "blue")
        kartu_kpi(r3, "P%pk", f"{ppk:.4f}", "red")
        kartu_kpi(r4, "Level Sigma", f"{sigma:.2f}" if np.isfinite(sigma) else "Tidak terhingga", "dark")
    except Exception as e:
        st.warning(f"Ringkasan analisis belum dapat dihitung: {e}")

    st.markdown("### Pratinjau Data")
    tampil = df.copy()
    tampil.insert(0, "Subgrup", np.arange(1, len(tampil) + 1))
    st.dataframe(tampil, use_container_width=True, hide_index=True)

# ==============================================================================
# HALAMAN 2: IDENTIFIKASI OVERDISPERSI
# ==============================================================================
def halaman_overdispersi():
    header_halaman("Identifikasi Overdispersi")
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        hasil_df, res = hitung_peta_kendali(dasar)
    except Exception as e:
        st.error(str(e))
        return

    a, b, c = st.columns(3)
    kartu_kpi(a, "Rata-rata Proporsi (p̄)", f"{res['p_bar']:.5f}", "dark")
    kartu_kpi(b, "Rata-rata Moving Range (R̄)", f"{res['R_bar']:.5f}", "blue")
    kartu_kpi(c, "Keputusan", "Overdispersi" if res["is_overdispersed"] else "Tidak overdispersi", "yellow")

    if res["is_overdispersed"]:
        st.warning(
            f"Data menunjukkan kondisi overdispersi. "
            f"Jenis peta kendali yang dipilih: {res['chart_type']}."
        )
    else:
        st.success(
            f"Data tidak menunjukkan kondisi overdispersi. "
            f"Jenis peta kendali yang dipilih: {res['chart_type']}."
        )

    tabel = hasil_df[[
        "Subgrup", "Tanggal", "Jumlah Unit Diperiksa",
        "Jumlah Produk Cacat", "p_i", "sigma_pi", "z_i", "R_i"
    ]].copy()
    st.markdown("### Tabel Perhitungan")
    st.dataframe(tabel, use_container_width=True, hide_index=True)

# ==============================================================================
# HALAMAN 3: ANALISIS PETA KENDALI
# ==============================================================================
def halaman_peta_kendali():
    header_halaman("Analisis Peta Kendali")
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        df_ctrl, res = hitung_peta_kendali(aktif)
    except Exception as e:
        st.error(str(e))
        return

    a, b, c = st.columns(3)
    kartu_kpi(a, "Jenis Peta Kendali", res["chart_type"], "dark")
    kartu_kpi(b, "Garis Tengah (CL)", f"{res['p_bar']:.5f}", "blue")
    kartu_kpi(c, "Subgrup Out of Control", str(res["jumlah_ooc"]), "red")

    status = "BELUM TERKENDALI" if res["jumlah_ooc"] else "TERKENDALI STATISTIK"
    st.info(f"Status proses: **{status}** | Subgrup In Control: {res['jumlah_ic']}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["BKA_Aktif"], mode="lines", name="BKA", line=dict(color=MERAH, dash="dash", width=2)))
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["CL"], mode="lines", name="CL", line=dict(color=BIRU, width=2)))
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["BKB_Aktif"], mode="lines", name="BKB", line=dict(color=KUNING, dash="dash", width=2)))
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["p_i"], mode="lines+markers", name="Proporsi cacat (pi)", line=dict(color=HITAM), marker=dict(size=7)))
    ooc = df_ctrl[df_ctrl["Status_OOC"]]
    if not ooc.empty:
        fig.add_trace(go.Scatter(x=ooc["Subgrup"], y=ooc["p_i"], mode="markers", name="Out of Control", marker=dict(color=MERAH, size=12, symbol="diamond")))
    fig.update_layout(title=res["chart_type"], xaxis_title="Subgrup", yaxis_title="Proporsi cacat")
    st.plotly_chart(style_plotly(fig), use_container_width=True)

    st.markdown("### Evaluasi Subgrup Out of Control")
    if ooc.empty:
        st.success("Tidak ditemukan subgrup di luar batas kendali.")
    else:
        st.dataframe(ooc[["Subgrup", "Tanggal", "p_i", "BKA_Aktif", "BKB_Aktif"]], use_container_width=True, hide_index=True)
        pilihan = st.multiselect(
            "Pilih subgrup yang sudah diverifikasi memiliki penyebab khusus:",
            options=ooc["Subgrup"].astype(int).tolist(),
            default=[]
        )
        alasan = st.text_input("Catatan penyebab khusus / bukti evaluasi", value="")
        if st.button("Simpan subgrup yang dikeluarkan", disabled=(not pilihan or not alasan.strip())):
            sudah = {x["Subgrup"] for x in st.session_state.excluded_subgroups}
            for sg in pilihan:
                if int(sg) not in sudah:
                    tgl = ooc.loc[ooc["Subgrup"] == sg, "Tanggal"].iloc[0]
                    st.session_state.excluded_subgroups.append({
                        "Subgrup": int(sg),
                        "Tanggal": str(pd.Timestamp(tgl).date()),
                        "Alasan": alasan.strip()
                    })
            st.rerun()

    if st.session_state.excluded_subgroups:
        st.markdown("### Riwayat Subgrup yang Dikeluarkan")
        st.dataframe(pd.DataFrame(st.session_state.excluded_subgroups), use_container_width=True, hide_index=True)
        if st.button("Reset evaluasi subgrup"):
            st.session_state.excluded_subgroups = []
            st.rerun()

    st.markdown("### Tabel Peta Kendali")
    st.dataframe(df_ctrl, use_container_width=True, hide_index=True)

# ==============================================================================
# HALAMAN 4: UJI KEACAKAN (RUNS TEST)
# ==============================================================================
def halaman_runs_test():
    header_halaman("Uji Keacakan (Runs Test)")
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
    kartu_kpi(a, "Median Proporsi", f"{rt['median']:.5f}", "dark")
    kartu_kpi(b, "Jumlah Runs (V)", str(rt["V"]), "blue")
    kartu_kpi(c, "Statistik Uji Z", f"{rt['Z']:.4f}", "yellow")
    kartu_kpi(d, "P-value", f"{rt['p_value']:.4f}", "red")

    if rt["p_value"] < alpha:
        st.error("Keputusan: Tolak H₀. Data tidak menyebar secara acak.")
    else:
        st.success("Keputusan: Gagal menolak H₀. Tidak terdapat bukti bahwa data menyebar tidak acak.")

    st.write(f"n₁ = {rt['n1']} | n₂ = {rt['n2']} | E(V) = {rt['mu_V']:.4f} | σV = {rt['sigma_V']:.4f}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_ctrl["Subgrup"], y=df_ctrl["p_i"], mode="lines+markers", name="Proporsi cacat", line=dict(color=MERAH), marker=dict(color=BIRU)))
    fig.add_hline(y=rt["median"], line_dash="dash", line_color=KUNING, annotation_text=f"Median = {rt['median']:.5f}")
    fig.update_layout(title="Proporsi Cacat terhadap Median", xaxis_title="Subgrup", yaxis_title="Proporsi cacat")
    st.plotly_chart(style_plotly(fig), use_container_width=True)

# ==============================================================================
# HALAMAN 5: INDEKS KAPABILITAS PROSES (P%pk)
# ==============================================================================
def halaman_kapabilitas():
    header_halaman("Indeks Kapabilitas Proses", "Indeks kapabilitas atribut P%pk")
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    try:
        df_ctrl, res = hitung_peta_kendali(aktif)
        z_p, ppk = hitung_ppk_persen(res["p_bar"])
    except Exception as e:
        st.error(str(e))
        return

    if res["jumlah_ooc"] > 0:
        st.warning(f"Masih terdapat {res['jumlah_ooc']} subgrup OOC pada data aktif. Evaluasi dahulu penyebab khususnya sebelum menarik kesimpulan kapabilitas.")

    a, b, c = st.columns(3)
    kartu_kpi(a, "Proporsi Cacat (p̄)", f"{res['p_bar']:.5f}", "dark")
    kartu_kpi(b, "Nilai Normal Z(p̄)", f"{z_p:.5f}", "blue")
    kartu_kpi(c, "P%pk", f"{ppk:.5f}", "red")
    st.latex(r"P\%_{pk} = \frac{Z(\bar{p})}{3}")
    if ppk >= 1:
        st.success("Interpretasi berdasarkan batas P%pk ≥ 1: proses kapabel.")
    else:
        st.error("Interpretasi berdasarkan batas P%pk < 1: proses belum kapabel.")
    st.caption("Perhitungan menggunakan data aktif setelah evaluasi subgrup. Pastikan pilihan data ini sesuai dengan definisi operasional pada naskah skripsi.")

# ==============================================================================
# HALAMAN 6: LEVEL SIGMA
# ==============================================================================
def halaman_level_sigma():
    header_halaman("Level Sigma")
    dasar, aktif = get_data_aktif()
    if dasar is None:
        st.warning("Unggah data terlebih dahulu melalui halaman Beranda.")
        return
    total_cacat = int(aktif["Jumlah Produk Cacat"].sum())
    total_unit = int(aktif["Jumlah Unit Diperiksa"].sum())

    st.write("Masukkan jumlah peluang terjadinya cacat pada setiap unit sesuai definisi CTQ/karakteristik yang digunakan dalam penelitian.")
    peluang = st.number_input(
        "Jumlah peluang cacat per unit", min_value=1, value=1, step=1,
        help="Jangan mengubah nilai ini tanpa dasar definisi peluang cacat dalam penelitian."
    )
    shift = st.number_input("Sigma shift", min_value=0.0, max_value=2.0, value=1.5, step=0.1)
    try:
        dpo, dpmo, sigma = hitung_level_sigma(total_cacat, total_unit, int(peluang), float(shift))
    except Exception as e:
        st.error(str(e))
        return

    a, b, c, d = st.columns(4)
    kartu_kpi(a, "Total Produk Cacat", format_angka(total_cacat), "red")
    kartu_kpi(b, "DPO", f"{dpo:.5f}", "dark")
    kartu_kpi(c, "DPMO", f"{dpmo:,.2f}", "blue")
    kartu_kpi(d, "Level Sigma", f"{sigma:.4f}" if np.isfinite(sigma) else "Tidak terhingga", "yellow")
    st.latex(r"DPO = \frac{\text{Jumlah cacat}}{\text{Unit diperiksa} \times \text{Peluang per unit}}")
    st.latex(r"DPMO = DPO \times 10^6")
    st.latex(r"\text{Level Sigma} = \Phi^{-1}\left(1-\frac{DPMO}{10^6}\right)+\text{shift}")
    st.info("Nilai peluang per unit dan sigma shift harus mengikuti definisi yang digunakan dalam skripsi. Nilai default 1 dan 1,5 hanya nilai awal yang perlu dikonfirmasi.")

# ==============================================================================
# HALAMAN 7: DIAGRAM SEBAB-AKIBAT (FISHBONE)
# ==============================================================================
def halaman_fishbone():
    header_halaman("Diagram Sebab-Akibat (Fishbone)")
    st.info("Masukkan penyebab berdasarkan hasil wawancara/kuesioner dan pembahasan penelitian. Data contoh tidak diisi otomatis agar tidak dianggap sebagai temuan faktual.")
    kategori = [
        "Man (Manusia)", "Machine (Mesin)", "Method (Metode)",
        "Material (Bahan)", "Measurement (Pengukuran)",
        "Environment (Lingkungan)"
    ]
    with st.form("form_fishbone", clear_on_submit=True):
        k = st.selectbox("Kategori penyebab", kategori)
        sebab = st.text_area("Penyebab yang teridentifikasi")
        simpan = st.form_submit_button("Tambahkan penyebab")
    if simpan:
        if sebab.strip():
            baru = pd.DataFrame([{"Kategori": k, "Penyebab": sebab.strip()}])
            st.session_state.fishbone_data = pd.concat(
                [st.session_state.fishbone_data, baru], ignore_index=True
            )
            st.rerun()
        else:
            st.warning("Isi penyebab terlebih dahulu.")

    if not st.session_state.fishbone_data.empty:
        st.markdown("### Daftar Penyebab")
        edit = st.data_editor(
            st.session_state.fishbone_data,
            use_container_width=True, num_rows="dynamic",
            column_config={
                "Kategori": st.column_config.SelectboxColumn("Kategori", options=kategori),
                "Penyebab": st.column_config.TextColumn("Penyebab")
            }
        )
        if st.button("Simpan perubahan Fishbone"):
            st.session_state.fishbone_data = edit
            st.success("Perubahan disimpan.")
        st.markdown("### Ringkasan per Kategori")
        for kat in kategori:
            daftar = st.session_state.fishbone_data.loc[
                st.session_state.fishbone_data["Kategori"] == kat, "Penyebab"
            ].dropna().tolist()
            if daftar:
                with st.expander(kat, expanded=True):
                    for item in daftar:
                        st.write(f"• {item}")
    else:
        st.warning("Belum ada penyebab yang dimasukkan.")

# ==============================================================================
# HALAMAN 8: FMEA
# ==============================================================================
def halaman_fmea():
    header_halaman("Failure Mode and Effects Analysis (FMEA)")
    st.info("Isi tabel berdasarkan hasil analisis penelitian. RPN dihitung dari Severity × Occurrence; Detection tidak digunakan sesuai rancangan penelitian.")
    kolom = [
        "Potensi Kegagalan", "Dampak Kegagalan", "Penyebab Kegagalan",
        "Severity", "Occurrence", "RPN", "Usulan Perbaikan"
    ]
    if st.session_state.fmea_data.empty:
        st.session_state.fmea_data = pd.DataFrame(columns=kolom)

    edited = st.data_editor(
        st.session_state.fmea_data,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Potensi Kegagalan": st.column_config.TextColumn("Potensi Kegagalan", required=True),
            "Dampak Kegagalan": st.column_config.TextColumn("Dampak Kegagalan"),
            "Penyebab Kegagalan": st.column_config.TextColumn("Penyebab Kegagalan"),
            "Severity": st.column_config.NumberColumn("Severity", min_value=1, max_value=10, step=1),
            "Occurrence": st.column_config.NumberColumn("Occurrence", min_value=1, max_value=10, step=1),
            "RPN": st.column_config.NumberColumn("RPN", disabled=True),
            "Usulan Perbaikan": st.column_config.TextColumn("Usulan Perbaikan")
        },
        key="editor_fmea"
    )

    if st.button("Hitung RPN dan simpan FMEA"):
        hasil = edited.copy()
        for c in ["Severity", "Occurrence"]:
            hasil[c] = pd.to_numeric(hasil[c], errors="coerce")
        valid = hasil["Severity"].between(1, 10) & hasil["Occurrence"].between(1, 10)
        hasil["RPN"] = np.where(valid, hasil["Severity"] * hasil["Occurrence"], np.nan)
        st.session_state.fmea_data = hasil
        st.success("RPN dihitung dari Severity × Occurrence. Pastikan skala 1–10 sesuai instrumen skripsimu.")
        st.rerun()

    if not st.session_state.fmea_data.empty:
        st.markdown("### Tabel FMEA")
        st.dataframe(st.session_state.fmea_data, use_container_width=True, hide_index=True)
        if "RPN" in st.session_state.fmea_data:
            ringkas = st.session_state.fmea_data.dropna(subset=["RPN"]).sort_values("RPN", ascending=False)
            if not ringkas.empty:
                st.markdown("### Prioritas berdasarkan RPN")
                st.dataframe(ringkas, use_container_width=True, hide_index=True)

# ==============================================================================
# NAVIGASI DAN PEMANGGILAN HALAMAN
# ==============================================================================
HALAMAN = [
    "Beranda",
    "Identifikasi Overdispersi",
    "Analisis Peta Kendali",
    "Uji Keacakan (Runs Test)",
    "Indeks Kapabilitas Proses",
    "Level Sigma",
    "Diagram Sebab-Akibat (Fishbone)",
    "FMEA"
]

with st.sidebar:
    st.markdown("# PT XYZ")
    st.caption("Sistem Analisis Kualitas Produksi AAC")
    st.markdown("---")
    halaman_dipilih = st.radio("MENU NAVIGASI", HALAMAN, index=0)
    st.markdown("---")
    if st.session_state.df_produksi is None:
        st.warning("Belum ada data diunggah.")
    else:
        st.success(f"Data aktif: {len(st.session_state.df_produksi)} subgrup")
        if st.session_state.excluded_subgroups:
            st.info(f"Subgrup dikeluarkan: {len(st.session_state.excluded_subgroups)}")

PEMANGGIL_HALAMAN = {
    "Beranda": halaman_beranda,
    "Identifikasi Overdispersi": halaman_overdispersi,
    "Analisis Peta Kendali": halaman_peta_kendali,
    "Uji Keacakan (Runs Test)": halaman_runs_test,
    "Indeks Kapabilitas Proses": halaman_kapabilitas,
    "Level Sigma": halaman_level_sigma,
    "Diagram Sebab-Akibat (Fishbone)": halaman_fishbone,
    "FMEA": halaman_fmea
}

PEMANGGIL_HALAMAN[halaman_dipilih]()
