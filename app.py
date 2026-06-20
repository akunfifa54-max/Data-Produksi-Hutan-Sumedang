import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# SET PAGE
# =========================
st.set_page_config(
    page_title="Babakan Siliwangi Dashboard",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS (BIAR RAPI SEPERTI DASHBOARD)
# =========================
st.markdown("""
<style>
h1, h2, h3 {
    text-align: center;
}

.block-container {
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA (WAJIB SESUAI FILE GITHUB)
# =========================
df = pd.read_csv("babakan_siliwangi.csv")

# =========================
# HEADER / COVER
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "https://upload.wikimedia.org/wikipedia/id/thumb/8/89/Logo_UNISBA.svg/512px-Logo_UNISBA.svg.png",
        width=140
    )

st.markdown("""
# UNIVERSITAS ISLAM BANDUNG  
### Fakultas Ekonomi dan Bisnis  
### Ekonomi Sumber Daya Alam dan Lingkungan  

---

# 🌳 BABAKAN SILIWANGI CITY FOREST DASHBOARD
""")

st.markdown("### Kelompok 2: Dadang dkk")
st.divider()

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "MENU",
    ["Home", "Data", "Visualisasi", "Prediksi"]
)

# =========================
# HOME
# =========================
if menu == "Home":

    st.subheader("📌 Ringkasan")
    
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tahun", df["tahun"].nunique())
    col2.metric("Rata-rata Kunjungan", int(df["produksi"].mean()))
    col3.metric("Total Kunjungan", int(df["produksi"].sum()))

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/0/07/Forest.jpg"
    )

# =========================
# DATA
# =========================
elif menu == "Data":

    st.subheader("📄 Dataset")

    st.dataframe(df, use_container_width=True)

# =========================
# VISUALISASI
# =========================
elif menu == "Visualisasi":

    st.subheader("📊 Grafik Kunjungan")

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

    st.subheader("🔮 Prediksi Kunjungan")

    X = df[["tahun"]]
    y = df["produksi"]

    model = LinearRegression()
    model.fit(X, y)

    tahun = st.number_input(
        "Masukkan Tahun",
        min_value=int(df["tahun"].max()),
        value=int(df["tahun"].max() + 1)
    )

    pred = model.predict([[tahun]])[0]

    st.success(f"Prediksi Kunjungan: {int(pred):,}")

    hasil = pd.DataFrame({
        "tahun": list(df["tahun"]) + [tahun],
        "produksi": list(df["produksi"]) + [pred]
    })

    fig = px.line(
        hasil,
        x="tahun",
        y="produksi",
        markers=True,
        title="Prediksi Tren Kunjungan"
    )

    st.plotly_chart(fig, use_container_width=True)
