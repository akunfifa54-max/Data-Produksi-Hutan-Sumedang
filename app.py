import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# =========================
# CONFIG HALAMAN
# =========================
st.set_page_config(
    page_title="Babakan Siliwangi Dashboard",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS
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
# LOAD DATA (SUDAH FIX)
# =========================
df = pd.read_csv("babakan_siliwangi.csv")

# =========================
# COVER MAKALAH
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "https://upload.wikimedia.org/wikipedia/id/thumb/8/89/Logo_UNISBA.svg/512px-Logo_UNISBA.svg.png",
        width=160
    )

st.markdown("""
<div style="text-align:center;">
    <h2>UNIVERSITAS ISLAM BANDUNG</h2>
    <h3>FAKULTAS EKONOMI DAN BISNIS</h3>
    <h3>PROGRAM STUDI EKONOMI PEMBANGUNAN</h3>
    <hr>
    <h1>ANALISIS BABAKAN SILIWANGI CITY FOREST</h1>
    <h4>Mata Kuliah Ekonomi Sumber Daya Alam dan Lingkungan</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### Kelompok 2
- Dadang
- Anggota 2
- Anggota 3
- Anggota 4
""")

st.divider()

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Data", "Visualisasi", "Prediksi"]
)

# =========================
# HOME
# =========================
if menu == "Home":

    st.title("🌳 Babakan Siliwangi City Forest")

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Forest.jpg/640px-Forest.jpg",
        use_container_width=True
    )

    st.markdown("""
    ### Deskripsi
    Babakan Siliwangi adalah hutan kota di Bandung yang berfungsi sebagai ruang terbuka hijau dan wisata alam.

    ### Fungsi
    - RTH Kota Bandung
    - Wisata alam & edukasi
    - Paru-paru kota

    ### Catatan Data
    Data “produksi” diubah menjadi jumlah kunjungan sebagai indikator aktivitas ekonomi.
    """)

    st.metric("Total Tahun", df["tahun"].nunique())
    st.metric("Rata-rata Kunjungan", int(df["produksi"].mean()))
    st.metric("Total Kunjungan", int(df["produksi"].sum()))

# =========================
# DATA
# =========================
elif menu == "Data":

    st.title("📄 Dataset Babakan Siliwangi")

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="babakan_siliwangi.csv",
        mime="text/csv"
    )

# =========================
# VISUALISASI
# =========================
elif menu == "Visualisasi":

    st.title("📊 Tren Kunjungan")

    fig = px.line(
        df,
        x="tahun",
        y="produksi",
        markers=True,
        title="Tren Kunjungan Babakan Siliwangi"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        df,
        x="tahun",
        y="produksi",
        title="Kunjungan per Tahun"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# PREDIKSI
# =========================
elif menu == "Prediksi":

    st.title("🔮 Prediksi Kunjungan")

    X = df[["tahun"]]
    y = df["produksi"]

    model = LinearRegression()
    model.fit(X, y)

    tahun_pred = st.number_input(
        "Masukkan Tahun",
        min_value=int(df["tahun"].max()),
        value=int(df["tahun"].max() + 1)
    )

    pred = model.predict([[tahun_pred]])[0]

    st.metric("Prediksi Kunjungan", f"{pred:,.0f}")

    df_pred = pd.DataFrame({
        "tahun": list(df["tahun"]) + [tahun_pred],
        "produksi": list(df["produksi"]) + [pred]
    })

    fig = px.line(
        df_pred,
        x="tahun",
        y="produksi",
        markers=True,
        title="Prediksi Kunjungan"
    )

    st.plotly_chart(fig, use_container_width=True)
