import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# =========================
# KONFIGURASI HALAMAN (WAJIB PALING ATAS)
# =========================
st.set_page_config(
    page_title="Dashboard Produksi Kayu Jawa Barat",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS TAMPILAN
# =========================
st.markdown("""
<style>
h1, h2, h3, h4 {
    text-align: center;
}

.main {
    padding-left: 50px;
    padding-right: 50px;
}

[data-testid="stSidebar"] {
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# =========================
# COVER MAKALAH
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "https://upload.wikimedia.org/wikipedia/id/thumb/8/89/Logo_UNISBA.svg/512px-Logo_UNISBA.svg.png",
        width=180
    )

st.markdown("""
<div style="text-align:center;">
    <h2>UNIVERSITAS ISLAM BANDUNG</h2>
    <h3>FAKULTAS EKONOMI DAN BISNIS</h3>
    <h3>PROGRAM STUDI EKONOMI PEMBANGUNAN</h3>
    <hr>
    <h1>DASHBOARD PRODUKSI KAYU JAWA BARAT</h1>
    <h4>Mata Kuliah Ekonomi Sumber Daya Alam dan Lingkungan</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### Kelompok 2
- Radea Rahman Dwiyana
- Bunga Wiati Manaki
- Shidqi Alhamdani
""")

st.divider()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("produksi_kayu_jabar.csv")

# =========================
# SIDEBAR MENU
# =========================
st.sidebar.title("📊 Menu")

menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Home", "Data", "Visualisasi", "Prediksi"]
)

# =========================
# HOME
# =========================
if menu == "Home":

    st.title("🌳 Dashboard Produksi Kayu Jawa Barat")

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Forest.jpg/640px-Forest.jpg",
        use_container_width=True
    )

    st.markdown("""
    ### Deskripsi
    Dashboard ini menampilkan data produksi kayu di Jawa Barat.

    ### Fitur
    - Data produksi
    - Visualisasi tren
    - Analisis sederhana
    - Prediksi produksi

    ### Sumber Data
    Open Data Jawa Barat
    """)

    st.metric("Total Data", len(df))
    st.metric("Jenis Kayu", df["jenis_kayu"].nunique())
    st.metric("Total Produksi", f"{df['produksi'].sum():,.0f}")

# =========================
# DATA
# =========================
elif menu == "Data":

    st.title("📄 Data Produksi")

    jenis = st.selectbox(
        "Pilih Jenis Kayu",
        sorted(df["jenis_kayu"].unique())
    )

    filtered = df[df["jenis_kayu"] == jenis]

    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        "Download CSV",
        filtered.to_csv(index=False),
        file_name="data_kayu.csv",
        mime="text/csv"
    )

# =========================
# VISUALISASI
# =========================
elif menu == "Visualisasi":

    st.title("📊 Visualisasi Produksi")

    jenis = st.selectbox(
        "Pilih Jenis Kayu",
        sorted(df["jenis_kayu"].unique())
    )

    filtered = df[df["jenis_kayu"] == jenis]

    fig1 = px.line(
        filtered,
        x="tahun",
        y="produksi",
        markers=True,
        title="Tren Produksi"
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        filtered,
        x="tahun",
        y="produksi",
        title="Produksi per Tahun"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.write(filtered["produksi"].describe())

# =========================
# PREDIKSI
# =========================
elif menu == "Prediksi":

    st.title("🔮 Prediksi Produksi")

    jenis = st.selectbox(
        "Pilih Jenis Kayu",
        sorted(df["jenis_kayu"].unique())
    )

    filtered = df[df["jenis_kayu"] == jenis]

    X = filtered[["tahun"]]
    y = filtered["produksi"]

    model = LinearRegression()
    model.fit(X, y)

    tahun = st.number_input(
        "Masukkan Tahun",
        min_value=int(df["tahun"].max()),
        value=int(df["tahun"].max() + 1)
    )

    pred = model.predict([[tahun]])[0]

    st.metric("Hasil Prediksi", f"{pred:,.0f}")

    hasil = pd.DataFrame({
        "tahun": list(filtered["tahun"]) + [tahun],
        "produksi": list(filtered["produksi"]) + [pred]
    })

    fig = px.line(
        hasil,
        x="tahun",
        y="produksi",
        markers=True,
        title="Prediksi Produksi"
    )

    st.plotly_chart(fig, use_container_width=True)
