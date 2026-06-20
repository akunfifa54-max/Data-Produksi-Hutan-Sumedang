import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="BL 6 - Eco Forest Valuation",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS STYLE
# =========================
st.markdown("""
<style>

.block-container {
    padding: 2rem 3rem;
}

h1, h2, h3 {
    text-align: center;
    color: #1b5e20;
}

.card {
    background-color: #ffffff;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.metric-box {
    background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-weight: bold;
    color: #1b5e20;
}

[data-testid="stSidebar"] {
    background-color: #f5f7f6;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
# 🌳 BL 6 — Eco-Forest Valuation System  
## Babakan Siliwangi (Urban Forest Bandung)

### Ekonomi Sumber Daya Alam dan Lingkungan  
### Yuhka Sundaya, S.E., M.Si.

---

## KELOMPOK 4  
- Salsa Zahratul Aulia (10090224004)  
- Aida Farida Kultsum (10090224014)  
- Nabil Athala Naufal (10090224022)  
""")

st.divider()

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 MENU",
    [
        "🏠 Dashboard",
        "🌳 Profil Hutan",
        "📊 Data Simulasi",
        "📈 Visualisasi",
        "⚙️ TEV Calculator"
    ]
)

# =========================
# DATA SIMULASI (BABAKAN SILIWANGI)
# =========================
data = pd.DataFrame({
    "tahun": [2019, 2020, 2021, 2022, 2023],
    "pengunjung": [12000, 13500, 11000, 16000, 18000],
    "carbon_absorption": [80, 85, 83, 90, 95]
})

# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-box">🌳 Profil Hutan<br><h2>19</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">🪵 Produksi<br><h2>12</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-box">📊 Master Data<br><h2>28</h2></div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-box">📈 Dashboard<br><h2>6</h2></div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="card">
    <h3>📌 Babakan Siliwangi Urban Forest</h3>
    Hutan kota sebagai ruang terbuka hijau dengan fungsi ekonomi, ekologi, dan sosial.
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROFIL
# =========================
elif menu == "🌳 Profil Hutan":

    st.markdown("""
    <div class="card">
    <h3>🌳 Babakan Siliwangi</h3>

    • Urban Forest Kota Bandung  
    • Fungsi rekreasi & edukasi  
    • Penyerap karbon  
    • Pengatur suhu kota  
    </div>
    """, unsafe_allow_html=True)

# =========================
# DATA
# =========================
elif menu == "📊 Data Simulasi":

    st.dataframe(data, use_container_width=True)

# =========================
# VISUALISASI
# =========================
elif menu == "📈 Visualisasi":

    fig1 = px.line(data, x="tahun", y="pengunjung", title="Tren Pengunjung Babakan Siliwangi")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(data, x="tahun", y="carbon_absorption", title="Serapan Karbon")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# TEV CALCULATOR
# =========================
elif menu == "⚙️ TEV Calculator":

    st.subheader("💰 Total Economic Value (TEV)")

    p = st.number_input("Rekreasi (Pengunjung)", 0)
    r = st.number_input("Karbon", 0)
    c = st.number_input("Edukasi", 0)
    s = st.number_input("Ekologi", 0)

    total = p + r + c + s

    st.markdown(f"""
    <div class="metric-box">
    TOTAL TEV<br><br>
    Rp {total:,.0f}
    </div>
    """, unsafe_allow_html=True)
