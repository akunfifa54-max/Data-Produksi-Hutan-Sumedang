import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Babakan Siliwangi A+ Dashboard",
    page_icon="🌳",
    layout="wide"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>

.block-container {
    padding: 2rem 3rem;
    background-color: #fbfcfb;
}

h1, h2, h3 {
    text-align: center;
    color: #1b5e20;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.metric {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    color: #1b5e20;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
# 🌳 BABAKAN SILIWANGI A+ DASHBOARD  
### Urban Forest & Ekonomi Lingkungan Bandung  

---

## UNIVERSITAS ISLAM BANDUNG  
Ekonomi Sumber Daya Alam dan Lingkungan  

## KELOMPOK 2  
- Dadang  
- Anggota 2  
- Anggota 3  
- Anggota 4  
""")

st.divider()

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 MENU",
    ["Dashboard", "Peta", "TEV Model", "Grafik Ekonomi"]
)

# =========================
# DATA SIMULASI
# =========================
df = pd.DataFrame({
    "tahun": [2019, 2020, 2021, 2022, 2023],
    "pengunjung": [12000, 13500, 11000, 16000, 18000],
    "karbon": [80, 85, 83, 90, 95]
})

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric">🌳 Profil<br><h2>19</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric">🪵 Aktivitas<br><h2>12</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric">📊 Data<br><h2>28</h2></div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric">📈 Modul<br><h2>6</h2></div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="card">
    <h3>📌 Babakan Siliwangi</h3>
    Urban forest sebagai sistem ekonomi-ekologi perkotaan yang memiliki nilai jasa lingkungan tinggi.
    </div>
    """, unsafe_allow_html=True)

# =========================
# 🗺️ MAP (BABAKAN SILIWANGI)
# =========================
elif menu == "Peta":

    st.subheader("🗺️ Lokasi Babakan Siliwangi")

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=-6.8895,
            longitude=107.6107,
            zoom=15,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=pd.DataFrame({
                    "lat": [-6.8895],
                    "lon": [107.6107]
                }),
                get_position='[lon, lat]',
                get_color='[0, 150, 0, 160]',
                get_radius=80
            )
        ],
    ))

    st.caption("📍 Babakan Siliwangi - Kota Bandung")

# =========================
# TEV MODEL
# =========================
elif menu == "TEV Model":

    st.subheader("💰 Model Total Economic Value (TEV)")

    p = st.slider("Provisioning (Rekreasi)", 0, 100, 40)
    r = st.slider("Regulating (Karbon)", 0, 100, 60)
    c = st.slider("Cultural (Wisata)", 0, 100, 70)
    s = st.slider("Supporting (Ekologi)", 0, 100, 50)

    total = p + r + c + s

    st.markdown(f"""
    <div class="metric">
    TOTAL TEV<br><br>
    Rp {total:,.0f}
    </div>
    """, unsafe_allow_html=True)

# =========================
# GRAFIK EKONOMI
# =========================
elif menu == "Grafik Ekonomi":

    st.subheader("📊 Analisis Ekonomi Babakan Siliwangi")

    fig1 = px.line(df, x="tahun", y="pengunjung", title="Tren Pengunjung")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(df, x="tahun", y="karbon", title="Serapan Karbon")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="card">
    Analisis menunjukkan bahwa peningkatan pengunjung berbanding dengan meningkatnya kesadaran lingkungan,
    sementara fungsi karbon tetap stabil sebagai jasa ekosistem utama.
    </div>
    """, unsafe_allow_html=True)
