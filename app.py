import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# ==========================================
# CONFIG & THEME REFRESH
# ==========================================
st.set_page_config(
    page_title="Babakan Siliwangi A+ Dashboard",
    page_icon="🌳",
    layout="wide"
)

# Kustomisasi CSS untuk UI modern dan minimalis (Warna Alam Bandung)
st.markdown("""
<style>
    /* Mengubah background utama */
    .block-container {
        padding: 2.5rem 5rem;
        background-color: #fcfdfe;
    }
    
    /* Font & Tipografi */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #1b5e20;
    }
    
    /* Banner Kelompok */
    .banner {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(27,94,32,0.15);
    }
    
    /* Kartu Metrik Modern */
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #2e7d32;
        margin-top: 5px;
    }
    
    /* Info Card */
    .info-card {
        background-color: #f1f8e9;
        border-left: 5px solid #4caf50;
        padding: 20px;
        border-radius: 4px 12px 12px 4px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616561.png", width=70)
st.sidebar.markdown("### **Navigasi Sistem**")
menu = st.sidebar.radio(
    "Pilih Menu Analisis:",
    ["🏠 Beranda & Profil", "🗺️ Pemetaan Spasial", "💰 Pemodelan TEV", "📊 Tren & Ekonomi"],
    label_visibility="collapsed"
)

# Parameter Ekonomi Tambahan di Sidebar (Untuk TEV Dinamis)
st.sidebar.divider()
st.sidebar.markdown("### 🔧 Asumsi Harga Jasa")
harga_tiket = st.sidebar.slider("Tarif Willingness to Pay (WTP) / Orang", 5000, 25000, 10000, 1000)
harga_karbon = st.sidebar.slider("Nilai Karbon / Ton (Rp)", 50000, 200000, 150000, 10000)

# ==========================================
# SIMULASI DATA (Diperkaya untuk analisis)
# ==========================================
df_ekonomi = pd.DataFrame({
    "Tahun": [2021, 2022, 2023, 2024, 2025],
    "Pengunjung (Jiwa)": [11000, 14500, 16000, 18500, 22000],
    "Serapan Karbon (Ton)": [83, 88, 92, 95, 98],
    "Keanekaragaman Hayati (Spesies)": [24, 25, 28, 28, 31]
})

# ==========================================
# MODULE 1: BERANDA & PROFIL
# ==========================================
if menu == "🏠 Beranda & Profil":
    # Banner Identitas Kelompok & Kampus
    st.markdown("""
    <div class="banner">
        <h1 style="color: white; margin:0; font-size: 32px;">🌳 BABAKAN SILIWANGI A+ DASHBOARD</h1>
        <p style="margin: 5px 0 15px 0; font-size: 18px; opacity: 0.9;">Analisis Valuasi Ekonomi & Sistem Ekologi Hutan Kota Bandung</p>
        <hr style="border-color: rgba(255,255,255,0.2);">
        <p style="margin:0; font-size: 14px;"><strong>UNIVERSITAS ISLAM BANDUNG</strong> · Ekonomi Sumber Daya Alam dan Lingkungan</p>
        <p style="margin:0; font-size: 13px; opacity: 0.8;">Kelompok 2: Dadang, Anggota 2, Anggota 3, Anggota 4</p>
    </div>
    """, unsafe_allow_html=True)

    # Row Metrik Utama Ringkasan Wilayah
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-title">📐 Luas Area</div><div class="metric-value">3.8 Ha</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-title">🫁 Oksigen / Hari</div><div class="metric-value">14.2 Kg</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-title">👥 Tren WTP</div><div class="metric-value">↗️ Naik</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-title">🛡️ Status Hukum</div><div class="metric-value">Hutan Kota</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>📌 Pengantar Studi Kasus</h4>
        <p><b>Babakan Siliwangi (Baksil)</b> merupakan salah satu kawasan hutan kota penopang ekologi penting di Kota Bandung. 
        Sebagai sistem ekonomi-ekologi perkotaan, Baksil tidak hanya berfungsi sebagai paru-paru kota, namun juga menghasilkan 
        berbagai bentuk <i>intangible benefits</i> (manfaat tidak berwujud) seperti jasa pengatur iklim mikro, tata air, dan ruang edukasi-rekreasi budaya.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MODULE 2: PEMETAAN SPASIAL (PYDECK)
# ==========================================
elif menu == "🗺️ Pemetaan Spasial":
    st.subheader("📍 Geospasial & Batas Zona Ekologis")
    st.write("Visualisasi interaktif posisi geografis Ruang Terbuka Hijau Babakan Siliwangi.")

    # Data titik koordinat dan radius area
    map_data = pd.DataFrame({
        "lat": [-6.8895],
        "lon": [107.6107],
        "nama": ["Babakan Siliwangi"],
        "luas_m2": [38000]
    })

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/outdoors-v11",
        initial_view_state=pdk.ViewState(
            latitude=-6.8895,
            longitude=107.6107,
            zoom=15.5,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position='[lon, lat]',
                get_color='[46, 125, 50, 180]',
                get_radius=120,
                pickable=True
            ),
        ],
    ))
    st.caption("💡 Geser peta menggunakan klik kanan tetikus untuk melihat visualisasi sudut 3 Dimensi.")

# ==========================================
# MODULE 3: PEMODELAN TEV (TOTAL ECONOMIC VALUE)
# ==========================================
elif menu == "💰 Pemodelan TEV":
    st.subheader("📈 Simulasi Perhitungan Total Economic Value (TEV)")
    st.write("Gunakan penggeser (slider) di bawah ini untuk mengestimasi bobot/kuantitas komponen nilai guna ekonomi.")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### **1. Nilai Guna Langsung (Direct
