import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Babakan Siliwangi Dashboard",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS (DASHBOARD STYLE RAPI)
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
# HEADER (KHUSUS BAKSIL)
# =========================
st.markdown("""
# 🌳 BABAKAN SILIWANGI DASHBOARD  
### Urban Forest & Ruang Terbuka Hijau Kota Bandung  

---

## UNIVERSITAS ISLAM BANDUNG  
Fakultas Ekonomi dan Bisnis | Ekonomi Pembangunan  

**Analisis Nilai Ekonomi Hutan Kota (Urban Forest Valuation)**
""")

st.divider()

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 MENU",
    [
        "🏠 Overview",
        "📘 Konsep Hutan Kota",
        "💰 Nilai Ekonomi (TEV)",
        "⚖️ Trade-off Pemanfaatan",
        "🌿 Jasa Lingkungan",
        "📊 Studi Kasus"
    ]
)

# =========================
# HOME
# =========================
if menu == "🏠 Overview":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-box">🌳 Hutan Kota Bandung</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-box">🏙️ Babakan Siliwangi</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-box">🌿 Urban Ecosystem</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>📌 Deskripsi</h3>
    Babakan Siliwangi adalah <b>hutan kota (urban forest)</b> di Bandung yang berfungsi sebagai:
    ruang terbuka hijau, wisata alam, dan penyeimbang ekosistem perkotaan.
    </div>
    """, unsafe_allow_html=True)

# =========================
# KONDISI HUTAN KOTA
# =========================
elif menu == "📘 Konsep Hutan Kota":

    st.markdown("""
    <div class="card">
    <h3>🌿 Fungsi Babakan Siliwangi</h3>

    • Paru-paru Kota Bandung  
    • Ruang rekreasi masyarakat  
    • Pengendali suhu mikro kota  
    • Penyerapan karbon  
    • Edukasi lingkungan  
    </div>
    """, unsafe_allow_html=True)

# =========================
# TEV (URBAN VERSION)
# =========================
elif menu == "💰 Nilai Ekonomi (TEV)":

    st.subheader("💰 Total Economic Value Hutan Kota")

    p = st.number_input("Nilai Rekreasi (Wisata)", 0)
    r = st.number_input("Nilai Penyerapan Karbon", 0)
    c = st.number_input("Nilai Edukasi & Estetika", 0)
    s = st.number_input("Nilai Ekologi Pendukung", 0)

    total = p + r + c + s

    st.markdown(f"""
    <div class="metric-box">
    TOTAL NILAI EKONOMI BABAKAN SILIWANGI<br><br>
    Rp {total:,.0f}
    </div>
    """, unsafe_allow_html=True)

# =========================
# TRADE OFF
# =========================
elif menu == "⚖️ Trade-off Pemanfaatan":

    st.subheader("⚖️ Pemanfaatan vs Konservasi")

    eksploitasi = st.slider("Intensitas Aktivitas Manusia (%)", 0, 100, 40)
    konservasi = 100 - eksploitasi

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
        🚶 Aktivitas Wisata<br>{eksploitasi}%
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
        🌿 Fungsi Ekologis<br>{konservasi}%
        </div>
        """, unsafe_allow_html=True)

    if eksploitasi > 70:
        st.error("⚠ Tekanan lingkungan tinggi pada hutan kota")
    else:
        st.success("✔ Masih dalam batas berkelanjutan")

# =========================
# JASA LINGKUNGAN
# =========================
elif menu == "🌿 Jasa Lingkungan":

    st.markdown("""
    <div class="card">
    <h3>🌳 Kategori Jasa Lingkungan Babakan Siliwangi</h3>

    <b>Provisioning:</b> udara bersih, air tanah<br>
    <b>Regulating:</b> karbon, suhu kota<br>
    <b>Cultural:</b> wisata, rekreasi, edukasi<br>
    <b>Supporting:</b> habitat biodiversitas
    </div>
    """, unsafe_allow_html=True)

# =========================
# STUDI KASUS
# =========================
elif menu == "📊 Studi Kasus":

    st.subheader("🌳 Babakan Siliwangi Case Study")

    opsi = st.selectbox(
        "Pilih Skenario Pengelolaan",
        ["Konservasi Ketat", "Wisata Intensif", "Balanced Management"]
    )

    if opsi == "Konservasi Ketat":
        st.success("Lingkungan sangat terjaga, akses publik terbatas")
    elif opsi == "Wisata Intensif":
        st.warning("Ekonomi naik, tekanan lingkungan meningkat")
    else:
        st.info("Keseimbangan antara ekologi dan ekonomi")
