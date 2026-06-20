import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# =========================

# KONFIGURASI HALAMAN

# =========================

st.set_page_config(
page_title="Dashboard Produksi Kayu Jawa Barat",
page_icon="🌳",
layout="wide"
)

# =========================

# CSS CUSTOM

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
st.image("logo_unisba.png", width=180)

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

* Radea Rahman Dwiyana
* Bunga Wiati Manaki
* Shidqi Alhamdani
  """)

st.divider()

# =========================

# LOAD DATA

# =========================

df = pd.read_csv("produksi_kayu_jabar.csv")

# =========================

# SIDEBAR

# =========================

st.sidebar.title("📋 Menu")

menu = st.sidebar.radio(
"Pilih Halaman",
["Home", "Data", "Visualisasi", "Prediksi"]
)

# =========================

# HOME

# =========================

if menu == "Home":

```
st.title("🌳 Dashboard Produksi Kayu Bulat Jawa Barat")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Forest.jpg/640px-Forest.jpg",
    use_container_width=True
)

st.markdown("""
Dashboard ini menampilkan data produksi kayu bulat di Jawa Barat berdasarkan jenis kayu.

### Fitur Dashboard
- Menampilkan data produksi kayu
- Visualisasi tren produksi
- Analisis statistik sederhana
- Prediksi produksi tahun berikutnya

### Sumber Data
Open Data Jawa Barat dan Dinas Kehutanan Jawa Barat
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Jumlah Data",
        len(df)
    )

with col2:
    st.metric(
        "Jenis Kayu",
        df["jenis_kayu"].nunique()
    )

with col3:
    st.metric(
        "Total Produksi",
        f"{df['produksi'].sum():,.0f} m³"
    )
```

# =========================

# DATA

# =========================

elif menu == "Data":

```
st.title("📄 Data Produksi")

jenis = st.selectbox(
    "Pilih Jenis Kayu",
    sorted(df["jenis_kayu"].unique())
)

data_filter = df[df["jenis_kayu"] == jenis]

st.dataframe(
    data_filter,
    use_container_width=True
)

st.download_button(
    label="⬇ Download CSV",
    data=data_filter.to_csv(index=False),
    file_name=f"{jenis}.csv",
    mime="text/csv"
)
```

# =========================

# VISUALISASI

# =========================

elif menu == "Visualisasi":

```
st.title("📊 Visualisasi Produksi")

jenis = st.selectbox(
    "Pilih Jenis Kayu",
    sorted(df["jenis_kayu"].unique())
)

data_filter = df[df["jenis_kayu"] == jenis]

col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        data_filter,
        x="tahun",
        y="produksi",
        markers=True,
        title=f"Tren Produksi {jenis}"
    )
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:
    fig2 = px.bar(
        data_filter,
        x="tahun",
        y="produksi",
        title=f"Produksi {jenis} per Tahun"
    )
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.subheader("📈 Ringkasan Statistik")

st.write(
    data_filter["produksi"].describe()
)
```

# =========================

# PREDIKSI

# =========================

elif menu == "Prediksi":

```
st.title("🔮 Prediksi Produksi")

jenis = st.selectbox(
    "Pilih Jenis Kayu",
    sorted(df["jenis_kayu"].unique())
)

data_filter = df[df["jenis_kayu"] == jenis]

X = data_filter[["tahun"]]
y = data_filter["produksi"]

model = LinearRegression()
model.fit(X, y)

tahun_prediksi = st.number_input(
    "Masukkan Tahun Prediksi",
    min_value=2023,
    value=2023
)

prediksi = model.predict(
    [[tahun_prediksi]]
)[0]

st.metric(
    "Prediksi Produksi",
    f"{prediksi:,.0f} m³"
)

tahun_baru = np.append(
    data_filter["tahun"].values,
    tahun_prediksi
)

produksi_baru = np.append(
    data_filter["produksi"].values,
    prediksi
)

hasil = pd.DataFrame({
    "tahun": tahun_baru,
    "produksi": produksi_baru
})

fig = px.line(
    hasil,
    x="tahun",
    y="produksi",
    markers=True,
    title=f"Prediksi Produksi {jenis}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```
