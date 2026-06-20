import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Eco-Forest Valuation",
    page_icon="🌳",
    layout="wide"
)

# =========================
# CSS STYLE (BIAR MIRIP DASHBOARD PRO)
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
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (STYLE KAMPUS + DASHBOARD)
# =========================
st.markdown("""
# 🌳 Eco-Forest Valuation  
### Aplikasi Pembelajaran Ekonomi Sumber Daya Hutan  

---

## UNIVERSITAS ISLAM BANDUNG  
Fakultas Ekonomi dan Bisnis | Ekonomi Pembangunan  

**Tugas Kelompok: Sistem Valuasi Ekonomi Hutan (TEV - Tietenberg & Lewis)**
""")

st.divider()

# =========================
# SIDEBAR (SEPERTI DASHBOARD KPH CEPU)
# =========================
menu = st.sidebar.selectbox(
    "📌 PILIH MODUL PEMBELAJARAN",
    [
        "🏠 Halaman Utama",
        "📘 Teori Ekosistem Hutan",
        "💰 Modul TEV Calculator",
        "⚖️ Trade-off Analysis",
        "🌿 PES Simulation",
        "🌳 Studi Kasus"
    ]
)

# =========================
# HOME / TEORI UTAMA
# =========================
if menu == "🏠 Halaman Utama":

    st.subheader("📌 Rencana Alur Pembelajaran")
    st.info("Fase 1 → Teori | Fase 2 → Valuasi | Fase 3 → Simulasi | Fase 4 → Evaluasi")

    st.markdown("""
### 📚 Deskripsi Aplikasi
Aplikasi ini digunakan untuk memahami nilai ekonomi hutan berdasarkan konsep **Total Economic Value (TEV)**.

---

### 🎯 Tujuan Pembelajaran
- Memahami jasa lingkungan hutan
- Menghitung nilai ekonomi ekosistem
- Menganalisis trade-off pemanfaatan hutan
- Simulasi kebijakan PES
""")

# =========================
# TEORI
# =========================
elif menu == "📘 Teori Ekosistem Hutan":

    st.subheader("🌿 Klasifikasi Jasa Lingkungan")

    st.table({
        "Kategori": ["Provisioning", "Regulating", "Cultural", "Supporting"],
        "Definisi": [
            "Barang langsung dari hutan",
            "Pengatur iklim & karbon",
            "Wisata & spiritual",
            "Siklus ekosistem dasar"
        ],
        "Contoh": [
            "Kayu, air",
            "Karbon, udara bersih",
            "Ekowisata",
            "Fotosintesis"
        ],
        "Metode": [
            "Market Price",
            "Replacement Cost",
            "WTP / Travel Cost",
            "Indirect Valuation"
        ]
    })

    st.markdown("""
---

### 📊 Komposisi TEV Hutan Tropis
- Regulating: **45%**
- Provisioning: **25%**
- Cultural: **20%**
- Supporting: **10%**

👉 Menunjukkan nilai terbesar hutan berasal dari fungsi ekologis, bukan kayu.
""")

# =========================
# TEV CALCULATOR
# =========================
elif menu == "💰 Modul TEV Calculator":

    st.subheader("💰 Total Economic Value")

    p = st.number_input("Provisioning Value", 0)
    r = st.number_input("Regulating Value", 0)
    c = st.number_input("Cultural Value", 0)
    s = st.number_input("Supporting Value", 0)

    tev = p + r + c + s

    st.success(f"TOTAL TEV = Rp {tev:,.0f}")

# =========================
# TRADE OFF
# =========================
elif menu == "⚖️ Trade-off Analysis":

    st.subheader("⚖️ Pemanfaatan Hutan")

    exploit = st.slider("Intensitas Eksploitasi", 0, 100, 40)
    conservation = 100 - exploit

    st.write(f"🔴 Eksploitasi: {exploit}%")
    st.write(f"🟢 Konservasi: {conservation}%")

    if exploit > 60:
        st.error("Risiko deforestasi tinggi!")
    else:
        st.success("Masih dalam batas berkelanjutan")

# =========================
# PES
# =========================
elif menu == "🌿 PES Simulation":

    st.subheader("🌿 Payment for Ecosystem Services")

    st.write("""
PES adalah sistem pembayaran untuk menjaga jasa lingkungan hutan.
""")

    budget = st.number_input("Dana PES (Rp)", 0)

    if budget > 1000000:
        st.success("Program PES efektif berjalan")
    else:
        st.warning("Dana masih kurang optimal")

# =========================
# CASE STUDY
# =========================
elif menu == "🌳 Studi Kasus":

    st.subheader("🌳 Studi Kasus Hutan Tropis")

    choice = st.selectbox(
        "Pilih Kebijakan",
        ["Eksploitasi Kayu", "Konservasi Total", "Eco-Tourism"]
    )

    if choice == "Eksploitasi Kayu":
        st.error("Pendapatan tinggi jangka pendek, kerusakan lingkungan tinggi")
    elif choice == "Konservasi Total":
        st.success("Lingkungan terjaga, ekonomi rendah")
    else:
        st.info("Keseimbangan ekonomi & lingkungan optimal")
