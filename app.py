        for baris in teks.split("\n"):
            if baris.strip():
                daftar_fishbone.append({
                    "Kategori (5M + 1E)": kat.split(" ")[0],
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
            "Kategori (5M + 1E)": st.column_config.TextColumn("Kategori (5M + 1E)", disabled=True),
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

    if st.button("⚡ Hitung Nilai RPN & Urutkan Prioritas", use_container_width=True):
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
        "⬇️ Download Tabel Hasil FMEA (.xlsx)",
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
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-bars">
            <div class="bar-red"></div>
            <div class="bar-yellow"></div>
        </div>
        <div class="logo-title">PT XYZ</div>
        <div class="logo-sub">Building a Better Future</div>
    </div>
    """, unsafe_allow_html=True)

    pilihan_menu = st.radio("Navigasi", list(MENU_ITEMS.keys()), index=0)


MENU_ITEMS[pilihan_menu]()
