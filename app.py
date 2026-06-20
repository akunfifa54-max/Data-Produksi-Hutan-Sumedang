import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="BL 6 - Eco Forest",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS DASHBOARD STYLE
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

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (BL 6 STYLE + DISESUIKAN)
# =========================
st.markdown("""
# 🌳 BL 6 — Eco-Forest Valuation System  
## Aplikasi Analisis Ekonomi Sumber Daya Hutan  

---

### Mata Kuliah  
Ekonomi Sumber Daya Alam dan Lingkungan  

### Dosen Pengampu  
Yuhka Sundaya, S.E., M.Si.

---

## KELOMPOK 4  
- Salsa Zahratul Aulia (10090224004)  
- Aida Farida Kultsum (10090224014)  
- Nabil Athala Naufal (10090224022)  
""")

st.divider()

# =========================
# SIDEBAR MENU (KPH CEPU STYLE)
# =========================
menu = st.sidebar.radio(
    "📌 NAVIGASI SISTEM",
    [
        "🏠 Dashboard Utama",
        "🌳 Profil Hutan",
        "🪵 Produksi & Data",
        "📊 Master Data",
        "📈 Dashboard Summary",
        "⚙️ Simulasi Valuasi"
    ]
)

# =========================
# DASHBOARD UTAMA
# =========================
if menu == "🏠 Dashboard Utama":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-box">🌳 Profil Hutan</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">🪵 Produksi Kayu</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-box">📊 Master Data</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>📌 Deskripsi Aplikasi</h3>

    Aplikasi ini digunakan untuk analisis ekonomi sumber daya hutan pada kawasan 
    <b>Babakan Siliwangi / Hutan Kota Bandung</b> berbasis konsep valuasi ekonomi lingkungan.

    <br><br>
    Fitur utama:
    <ul>
        <li>Profil Hutan</li>
        <li>Produksi / Aktivitas Ekosistem</li>
        <li>Master Data Lingkungan</li>
        <li>Simulasi Valuasi Ekonomi (TEV)</li>
        <li>Dashboard Summary</li>
        <li>Analisis Ekonomi Lingkungan</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROFIL HUTAN
# =========================
elif menu == "🌳 Profil Hutan":

    st.markdown("""
    <div class="card">
    <h3>🌳 Babakan Siliwangi (Urban Forest Bandung)</h3>

    • Fungsi: Ruang Terbuka Hijau (RTH)  
    • Lokasi: Kota Bandung  
    • Status: Hutan Kota / Urban Forest  
    • Fungsi Ekonomi: Rekreasi, karbon, edukasi  
    • Fungsi Ekologi: Penyerapan CO₂, penyejuk kota  
    </div>
    """, unsafe_allow_html=True)

# =========================
# PRODUKSI / DATA
# =========================
elif menu == "🪵 Produksi & Data":

    st.markdown("""
    <div class="card">
    <h3>🪵 Aktivitas Ekosistem (Proxy Produksi)</h3>

    Dalam konteks hutan kota, “produksi” diartikan sebagai:
    <ul>
        <li>Jumlah kunjungan masyarakat</li>
        <li>Aktivitas wisata alam</li>
        <li>Pemanfaatan ruang publik</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="metric-box">📊 Data bersifat estimasi berbasis tren urban tourism</div>', unsafe_allow_html=True)

# =========================
# MASTER DATA
# =========================
elif menu == "📊 Master Data":

    st.markdown("""
    <div class="card">
    <h3>📊 Struktur Data Ekonomi Hutan</h3>

    • Provisioning → udara, air  
    • Regulating → karbon, suhu  
    • Cultural → wisata, estetika  
    • Supporting → biodiversitas  
    </div>
    """, unsafe_allow_html=True)

# =========================
# DASHBOARD SUMMARY
# =========================
elif menu == "📈 Dashboard Summary":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-box">🌳 Ekosistem Stabil</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">💰 Nilai Ekonomi Tinggi</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-box">🌿 Fungsi Lingkungan Aktif</div>', unsafe_allow_html=True)

# =========================
# SIMULASI
# =========================
elif menu == "⚙️ Simulasi Valuasi":

    st.subheader("💰 Simulasi Total Economic Value (TEV)")

    p = st.number_input("Provisioning", 0)
    r = st.number_input("Regulating", 0)
    c = st.number_input("Cultural", 0)
    s = st.number_input("Supporting", 0)

    total = p + r + c + s

    st.markdown(f"""
    <div class="metric-box">
    TOTAL ECONOMIC VALUE (TEV)<br><br>
    Rp {total:,.0f}
    </div>
    """, unsafe_allow_html=True)
