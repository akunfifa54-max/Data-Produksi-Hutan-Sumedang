import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# ==========================================
# 1. ULTRA-PREMIUM FULL DARK MODE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Forest Valuation Dashboard",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Full Dark Mode - Menjamin Kontras Tinggi & Teks Sangat Jelas
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Base Dark Background */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0d1310 !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Container Utama */
    .block-container { 
        padding: 2.5rem 4.5rem; 
        background-color: #0d1310 !important; 
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 { 
        color: #4ade80 !important; 
        font-weight: 700; 
        letter-spacing: -0.5px; 
    }
    
    /* Jumbotron Hero Banner Premium Dark */
    .hero-banner {
        background: linear-gradient(135deg, #0f2e1b 0%, #1b4d22 50%, #2e7d32 100%);
        color: #ffffff !important; 
        padding: 45px; 
        border-radius: 20px; 
        margin-bottom: 35px;
        border: 1px solid #22c55e;
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.1);
    }
    .hero-banner h1, .hero-banner p { color: #ffffff !important; }
    
    /* Metrik Card - Latar Belakang Gelap Kontras */
    .metric-container {
        background: #141d19 !important; 
        border: 2px solid #22c55e !important; 
        border-radius: 16px;
        padding: 26px 22px; 
        text-align: center; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(34, 197, 94, 0.2);
    }
    .metric-hdr { 
        font-size: 12px; 
        color: #94a3b8 !important; 
        text-transform: uppercase; 
        font-weight: 700; 
        letter-spacing: 1px; 
    }
    .metric-val { 
        font-size: 28px; 
        font-weight: 700; 
        color: #4ade80 !important; 
        margin-top: 8px; 
    }
    
    /* Kotak Info Spesifik */
    .info-box-warn {
        background-color: #2a1b08 !important; 
        border-left: 6px solid #f59e0b !important;
        padding: 22px; 
        border-radius: 12px; 
        margin-top: 20px; 
        color: #fde68a !important;
        border: 1px solid #78350f;
    }
    .info-box-success {
        background-color: #092415 !important; 
        border-left: 6px solid #22c55e !important;
        padding: 22px; 
        border-radius: 12px; 
        margin-top: 20px; 
        color: #bbf7d0 !important;
        border: 1px solid #14532d;
    }
    
    /* Sidebar Dark Styling */
    section[data-testid="stSidebar"] { 
        background-color: #070b09 !important; 
        border-right: 1px solid #1b4d22 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] h2 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] label {
        color: #4ade80 !important; 
        font-weight: 600;
    }
    
    /* Menyelaraskan teks standar Streamlit agar cerah */
    .stMarkdown, p, span, li {
        color: #cbd5e1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FAIL-SAFE DATA ENGINE
# ==========================================
def safe_load_csv(file_name, backup_dict):
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name)
            df.columns = df.columns.str.strip()
            return df
        except:
            return pd.DataFrame(backup_dict)
    return pd.DataFrame(backup_dict)

df_rangkuman = safe_load_csv("Rangkuman.csv", {
    'variable': ['forest_area_ha', 'annual_resin_production_ton', 'annual_log_production_m3', 'carbon_stock'],
    'value': [31850, 5450, 24800, 1775000]
})
df_profil = safe_load_csv("Profil Hutan KPH Sumedang.csv", {
    'No': [1, 2, 3, 4, 5],
    'Kecamatan / BKPH': ['Ujungjaya', 'Tomo', 'Jatigede', 'Tanjungkerta', 'Conggeang'],
    'Luas Hutan Pinus (Ha)': [10500, 11200, 10150, 5900, 5800]
})
df_komposisi = safe_load_csv("Komposisi Hasil Hutan.csv", {
    'Kategori': ['Getah Pinus (HHBK)', 'Kayu Log Komersial', 'Valuasi Serapan Karbon'],
    'Persentase': [70, 20, 10]
})
df_produksi = safe_load_csv("Produksi Hasil Hutan.csv", {
    'Variabel': ['Getah Pinus', 'Kayu Log'],
    'Nilai': [5450, 24800]
})

luas_total_hutan = 31850
volume_getah_tahunan = 5450  
volume_kayu_tahunan = 24800   

# ==========================================
# 3. BRANDING LOGO & NAVIGATION
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    st.sidebar.image(Image.open(logo_path), use_container_width=True)

st.sidebar.markdown("<h2 style='text-align: center; margin-top:5px; font-size:20px; color:#4ade80; font-weight:700;'>PBL KELOMPOK 2</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94a3b8; font-size:13px; margin-top:-10px;'>Ekonomi Sumber Daya Alam & Lingkungan</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color: #1b4d22;'>", unsafe_allow_html=True)

st.sidebar.markdown("✨ **Menu Navigasi Utama:**")
menu = st.sidebar.radio(
    "Pilih Halaman Analisis:",
    [
        "🏠 Beranda Korporat Utama", 
        "📄 Karakteristik & Hayati Wilayah", 
        "📦 Neraca Aliran Production", 
        "💰 Valuasi TEV & Ekonomi Makro",
        "⚖️ Batas Kebijakan Trade-Off",
        "📊 Simulator Finansial Interaktif",
        "📂 Validasi Master Data CSV"
    ],
    label_visibility="collapsed"
)

# Template Fungsi untuk Grafik agar otomatis Sinkron dengan Dark Mode
def apply_dark_theme_layout(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#e2e8f0",
        title_font_color="#4ade80",
        legend_font_color="#e2e8f0"
    )
    fig.update_xaxes(gridcolor='#1e293b', title_font_color="#cbd5e1", tickfont_color="#cbd5e1")
    fig.update_yaxes(gridcolor='#1e293b', title_font_color="#cbd5e1", tickfont_color="#cbd5e1")
    return fig

# ==========================================
# MODUL 1: BERANDA KORPORAT UTAMA
# ==========================================
if menu == "🏠 Beranda Korporat Utama":
    st.markdown("""
    <div class="hero-banner">
        <h1>KPH SUMEDANG ECO-FOREST VALUATION</h1>
        <p>Sistem Pemodelan Nilai Ekonomi Lingkungan, Optimasi HHBK Pinus & Analisis Keberlanjutan Komoditas Kehutanan - PBL Kelompok 2</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.markdown("### 📑 Latar Belakang Riset Kasus (PBL)")
        st.write("""
        Platform dashboard digital ini dirancang secara khusus untuk menganalisis struktur tata kelola ekonomi makro dan mikro 
        pada **Kesatuan Pemangkuan Hutan (KPH) Sumedang**. Fokus kajian ilmiah diarahkan pada tegakan vegetasi komoditas **Pinus (*Pinus merkusii*)**.
        
        Melalui metodologi Ekonomi Sumber Daya Alam, kami membedah bagaimana pemanfaatan ekonomi komersial dari ekstraksi hasil hutan 
        dapat dioptimalkan tanpa mendegradasi fungsi perlindungan lingkungan hidup (*sustainable forest management*).
        """)
        
        st.markdown("### 👥 Identitas Peneliti Kelompok 2:")
        st.markdown("""
        * **Mata Kuliah:** Ekonomi Sumber Daya Alam dan Lingkungan  
        * **Institusi:** Fakultas Ekonomi dan Bisnis, Universitas Islam Bandung (UNISBA)  
        * **Dosen Pengampu:** Yuhka Sundaya, S.E., M.Si.  
        
        **Susunan Anggota Tim Peneliti:**
        1. 🧑‍💻 **Radea Rahman Dwiyana** (10090224001)
        2. 👩‍💻 **Bunga Wiati Manaki** (10090224026)
        3. 🧑‍💻 **Shidqi Alhamdani Mieftah** (10090224032)
        """)
    
    with col_side:
        st.markdown("""
        <div class='metric-container' style='border-top: 4px solid #4ade80; text-align:left;'>
            <h4 style='color:#4ade80; margin-top:0;'>🎯 Core Capabilities</h4>
            <p style='color:#cbd5e1; font-size:14px;'>• <b>Valuasi TEV:</b> Menilai aset nyata pasar dan non-pasar (karbon).</p>
            <p style='color:#cbd5e1; font-size:14px;'>• <b>Uji Sensitivitas Interaktif:</b> Simulasi ketahanan kas terhadap guncangan harga pasar.</p>
            <p style='color:#cbd5e1; font-size:14px;'>• <b>Policy Recommendation:</b> Penyusun strategi mitigasi konflik trade-off ekologi-ekonomi.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# MODUL 2: KARAKTERISTIK & HAYATI WILAYAH
# ==========================================
elif menu == "📄 Karakteristik & Hayati Wilayah":
    st.header("📄 Karakteristik Geografis, Fungsi Kawasan & Keanekaragaman Hayati")
    
    tab_geo, tab_status, tab_biodiv = st.tabs([
        "🗺️ Pembagian Spasial Wilayah", 
        "⚖️ Status Hukum & Tata Fungsi", 
        "🦅 Inventarisasi Biodiversitas"
    ])
    
    with tab_geo:
        col_t, col_b = st.columns([4, 3])
        with col_t:
            st.markdown("##### Sebaran Luas Pengelolaan Wilayah Kerja")
            st.dataframe(df_profil, use_container_width=True, hide_index=True)
        with col_b:
            st.markdown("<div class='info-box-success' style='margin-top:0;'>", unsafe_allow_html=True)
            st.markdown("##### 📍 Kondisi Topografi & Tanah")
            st.write("""
            Wilayah administrasi KPH Sumedang didominasi oleh perbukitan bergelombang tajam dengan karakteristik tanah latosol dan andosol subur. Iklim mikro jeung curah hujan anu stabil jadi prasyarat utama alusna pertumbuhan getah pinus.
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_status:
        st.markdown("### 🏛️ Kepastian Hukum Tata Kawasan Hutan")
        st.write("Mayoritas wilayah KPH Sumedang berstatus hukum sebagai **HUTAN PRODUKSI (HP)**, dikombinasikan jeung **Hutan Lindung (HL)** di hulu DAS.")
        
        st.markdown("<div class='info-box-success'>", unsafe_allow_html=True)
        st.markdown("##### 🔗 Relevansi Logis Terhadap Produksi Getah Pinus (HHBK)")
        st.write("""
        Kawasan HP kudu ngahasilkeun untung tapi tetep lestari. Ku kituna, **penyadapan Getah Pinus (HHBK)** jadi jalan tengah anu cerdas. **Pohon pinus tetep nangtung pikeun nyerep karbon jeung nahan erosi, sedengkeun getahna bisa dipanen terus-terusan jang pamasukan.**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_biodiv:
        st.markdown("### 🦅 Inventarisasi Keanekaragaman Hayati")
        c_flora, c_fauna = st.columns(2)
        with c_flora:
            st.markdown("""
            <div class='metric-container' style='text-align: left; border-top: 4px solid #4ade80;'>
                <h4 style='color:#4ade80;'>🌲 Varietas Flora (Vegetasi)</h4>
                <p>• <b>Pinus merkusii:</b> Tegakan utama penopang ekonomi.</p>
                <p>• <b>Kaliandra & Mahoni:</b> Penahan kebakaran jeung peningkat hara tanah.</p>
            </div>
            """, unsafe_allow_html=True)
        with c_fauna:
            st.markdown("""
            <div class='metric-container' style='text-align: left; border-top: 4px solid #f59e0b;'>
                <h4 style='color:#f59e0b;'>🦅 Taksonomi Fauna (Satwa Liar)</h4>
                <p>• <b>Predator:</b> Habitat manuk Elang Jawa (Spizaetus bartelsi) anu dilindungi.</p>
                <p>• <b>Mamalia:</b> Populasi Bagong, Peucang, jeung sato liar lianna.</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# MODUL 3: NERACA ALIRAN PRODUKSI
# ==========================================
elif menu == "📦 Neraca Aliran Production":
    st.header("📦 Neraca Aliran Output Hasil Produksi Tahunan")
    
    fig_prod = px.bar(
        df_produksi, x='Variabel', y='Nilai', color='Variabel', text_auto='.2s',
        color_discrete_sequence=['#4ade80', '#3b82f6'],
        title="Volume Panen Komoditas Tahunan KPH Sumedang"
    )
    fig_prod = apply_dark_theme_layout(fig_prod)
    st.plotly_chart(fig_prod, use_container_width=True)
    st.dataframe(df_produksi, use_container_width=True, hide_index=True)

# ==========================================
# MODUL 4: VALUASI TEV & EKONOMI MAKRO
# ==========================================
elif menu == "💰 Valuasi TEV & Ekonomi Makro":
    st.header("💰 Analisis Total Economic Value (TEV) & Proxy Kelayakan")
    
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown('<div class="metric-container"><div class="metric-hdr">Net Present Value (NPV) Baseline</div><div class="metric-val">Rp 198,500,000 / Ha</div></div>', unsafe_allow_html=True)
    with c_m2:
        st.markdown('<div class="metric-container"><div class="metric-hdr">Internal Rate of Return (IRR)</div><div class="metric-val">15.80 %</div></div>', unsafe_allow_html=True)
    with c_m3:
        st.markdown('<div class="metric-container"><div class="metric-hdr">Benefit-Cost Ratio (BCR)</div><div class="metric-val">2.85 x</div></div>', unsafe_allow_html=True)
        
    st.write("---")
    
    col_pie, col_desc = st.columns([1, 1])
    with col_pie:
        fig_pie = px.pie(
            df_komposisi, values='Persentase', names='Kategori', hole=0.4,
            color_discrete_sequence=['#1b4d22', '#2e7d32', '#4ade80'],
            title="Komposisi Kontribusi Manfaat Ekonomi Total (TEV)"
        )
        fig_pie = apply_dark_theme_layout(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_desc:
        st.markdown("#### 🌍 Total Nilai Ekonomi Agregat Makro")
        st.metric(label="Estimasi Nilai Total Ekonomi Kawasan KPH Per Tahun", value="Rp 66,100,000,000")
        st.write("""
        Melalui pemodelan TEV, Kelompok 2 bisa ngabuktikeun sacara ilmiah yen **Getah Pinus (HHBK) nyepeng 70% tina total valuasi ekonomi**. Ieu argumen kuat yen teu kudu negor tangkal jang meunangkeun duit gede.
        """)

# ==========================================
# MODUL 5: BATAS KEBIJAKAN TRADE-OFF
# ==========================================
elif menu == "⚖️ Batas Kebijakan Trade-Off":
    st.header("⚖️ Analisis Batas Trade-Off Keseimbangan Ekonomi & Ekologi")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="info-box-warn">
            <h4>📈 Sektor Dorongan Ekonomi Komersial</h4>
            <p>Nyadap getah kaleuleuwihi jeung negor tangkal gancang teuing demi ngudag profit instan.</p>
            <b>Risiko:</b> Tangkal ruksak/tumbang, sarta kamampuan leuweung nyerep karbon bakal turun drastis.
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="info-box-warn" style="border-left-color: #3b82f6 !important; background-color: #0b1e2d !important; color: #93c5fd !important; border: 1px solid #1e3a5f;">
            <h4>🌍 Sektor Proteksi Ekosistem & Lingkungan</h4>
            <p>Nyelang/ngalarang total penebangan jeung nyadap getah demi ngajaga alam utuh.</p>
            <b>Risiko:</b> Pendapatan daerah turun drastis jeung masarakat penyadap lokal bakal kaleungitan pagawean.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="info-box-success">
        <h4>💡 Resolusi Konseptual Kelompok 2: Optimalisasi HHBK Berkelanjutan</h4>
        <p>Ku nilai <b>BCR baseline 2.85</b>, skema pemanfaatan Getah Pinus (HHBK) mangrupakeun jalan tengah (equilibrium) pangalusna. Duit asup, tangkal tetep nangtung ngajaga lingkungan.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MODUL 6: SIMULATOR FINANSIAL INTERAKTIF
# ==========================================
elif menu == "📊 Simulator Finansial Interaktif":
    st.header("📊 Simulator Sensitivitas & Kelayakan Finansial Dinamis")
    st.write("Uji ketahanan finansial investasi KPH Sumedang dumasar kana parobahan harga getah pinus sacara real-time.")

    # Slider Kontrol Interaktif
    harga_simulasi = st.slider(
        "Atur Prakiraan Harga Jual Getah Pinus (Rupiah / Kilogram):",
        min_value=5000,
        max_value=25000,
        value=11500,
        step=500
    )
    
    # Hitungan Matematika Ekonomi
    omset_getah_live = volume_getah_tahunan * 1000 * harga_simulasi
    omset_kayu_statis = volume_kayu_tahunan * 650000
    total_omset_live = omset_getah_live + omset_kayu_statis
    
    rasio_indeks = harga_simulasi / 11500
    npv_live = 198500000 * rasio_indeks
    bcr_live = 2.85 * rasio_indeks

    st.write("---")
    st.markdown("### 📈 Proyeksi Indikator Finansial Hasil Simulasi")
    
    v1, v2, v3 = st.columns(3)
    with v1:
        st.metric(label="Proyeksi NPV Dinamis", value=f"Rp {int(npv_live):,}", delta=f"{((rasio_indeks-1)*100):+.1f}% Pergeseran")
    with v2:
        st.metric(label="Proyeksi BC Ratio Dinamis", value=f"{bcr_live:.2f} x", delta=f"{(bcr_live - 2.85):+.2f}")
    with v3:
        st.metric(label="Total Estimasi Penerimaan Bruto Kawasan", value=f"Rp {int(total_omset_live):,}")

    st.write("---")
    
    chart_df = pd.DataFrame({
        'Kategori Sumber Omset': ['Getah Pinus (Dinamis)', 'Kayu Log Komersial (Statis)'],
        'Nilai Pendapatan Bruto (Rp)': [omset_getah_live, omset_kayu_statis]
    })
    
    fig_live = px.bar(
        chart_df, x='Kategori Sumber Omset', y='Nilai Pendapatan Bruto (Rp)',
        color='Kategori Sumber Omset', text_auto='.3s',
        color_discrete_sequence=['#f59e0b', '#4ade80'],
        title=f"Perbandingan Omset dina Tingkat Harga Rp {harga_simulasi:,} / Kg"
    )
    fig_live = apply_dark_theme_layout(fig_live)
    st.plotly_chart(fig_live, use_container_width=True)

# ==========================================
# MODUL 7: VALIDASI MASTER DATA CSV
# ==========================================
elif menu == "📂 Validasi Master Data CSV":
    st.header("📂 Transparansi Master Data (CSV Audit Mode)")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Indikator Rangkuman", 
        "🗺️ Distribusi Spasial", 
        "🍰 Struktur Kontribusi TEV", 
        "📦 Volume Aliran Output"
    ])
    
    with tab1:
        st.dataframe(df_rangkuman, use_container_width=True)
    with tab2:
        st.dataframe(df_profil, use_container_width=True)
    with tab3:
        st.dataframe(df_komposisi, use_container_width=True)
    with tab4:
        st.dataframe(df_produksi, use_container_width=True)
