
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Kualitas AAC",
    page_icon="📊",
    layout="wide"
)

# CSS tampilan
st.markdown("""
<style>
.stApp {
    background-color: #F5F6FA;
}
h1, h2, h3 {
    color: #171717;
}
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #D71920;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏭 PT X Gadget")
st.sidebar.caption("Quality Control Dashboard")

menu = st.sidebar.radio(
    "MENU UTAMA",
    [
        "Beranda",
        "Analisis Kualitas",
        "Data Produksi"
    ]
)

if menu == "Beranda":
    st.title("Analisis Kualitas Produksi Bata Ringan AAC")
    st.write("Dashboard Monitoring dan Pengendalian Kualitas Produksi")

    st.divider()

    st.subheader("Ringkasan Produksi")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Produksi", "10.000")
    col2.metric("Produk Cacat", "350")
    col3.metric("Persentase Cacat", "3,50%")

    st.subheader("Tren Produk Cacat")

    data = pd.DataFrame({
        "Bulan": ["Januari", "Februari", "Maret", "April", "Mei"],
        "Produk Cacat": [300, 250, 400, 280, 350]
    })

    fig = px.line(
        data,
        x="Bulan",
        y="Produk Cacat",
        markers=True,
        title="Jumlah Produk Cacat per Bulan"
    )

    fig.update_traces(line_color="#D71920")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Analisis Kualitas":
    st.title("Analisis Kualitas")
    st.info("Halaman analisis kualitas produksi.")

elif menu == "Data Produksi":
    st.title("Data Produksi")
    st.info("Halaman data produksi.")
