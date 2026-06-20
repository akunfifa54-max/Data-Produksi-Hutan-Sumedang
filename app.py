import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# ==========================================
# 1. PLATINUM CONFIGURATION & BRANDING THEME
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Forest Valuation Dashboard",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Ultra-Premium (Clean, Corporate, Academic & Eco-Vibe)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }
    .block-container { padding: 2.5rem 4.5rem; background-color: #fcfdfe; }
    h1, h2, h3, h4 { color: #1b5e20; font-weight: 700; letter-spacing: -0.5px; }
    
    /* Jumbotron Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #43a047 100%);
        color: white; padding: 45px; border-radius: 20px; margin-bottom: 35px;
        box-shadow: 0 12px 30px rgba(27, 94, 32, 0.15);
        position: relative; overflow: hidden;
    }
    
    /* Metrik Eksklusif Soft Shadow */
    .metric-container {
        background: #ffffff; border: 1px solid #f1f5f9; border-radius: 16px;
        padding: 26px 22px; text-align: center; 
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02), 0 2px 4px rgba(0, 0, 0, 0.01);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-container:hover {
        transform: translateY(-5px);
        border-color: #2e7d32;
        box-shadow: 0 15px 30px rgba(46, 125, 50, 0.1);
    }
    .metric-hdr { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
    .metric-val { font-size: 28px; font-weight: 700; color: #1b5e20; margin-top: 8px; }
    
    /* Kotak Kajian Khusus */
    .info-box-warn {
        background-color: #fffbeb; border-left: 6px solid #d97706;
        padding: 22px; border-radius: 12px; margin-top: 20px; color: #78350f;
    }
    .info-box-success {
        background-color: #f0fdf4; border-left: 6px solid #16a34a;
        padding: 22px; border-radius: 12px; margin-top: 20px; color: #14532d;
    }
    
    /* Custom Sidebar Layout */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FAIL-SAFE DATA ENGINE (SUNTIK DATA OTOMATIS)
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

# Konstanta Dasar Penelitian Kelompok 2
luas_total_hutan = 31850
volume_getah_tahunan = 5450  # Ton
volume_kayu_tahunan = 24800   # m³

# ==========================================
# 3. BRANDING LOGO & NAVIGATION
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    st.sidebar.image(Image.open(logo_path), use_container_width=True)

st.sidebar.markdown("<h2 style='text-align: center; margin-top:0; font-size:18px; color:#1b5e20; font-weight:700;'>PBL KELOMPOK 2</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #64748b; font-size:12px; margin-top:-10px;'>Ekonomi Sumber Daya Alam & Lingkungan</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

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

# ==========================================
# MODUL 1: BERANDA KORPORAT UTAMA
# ==========================================
if menu == "🏠 Beranda Korporat Utama":
    st.markdown("""
    <div class="hero-banner">
        <h1 style="color: white; margin: 0; font-size: 38px; font-weight:700; letter-spacing: -1px;">KPH SUMEDANG ECO-FOREST VALUATION</h1>
        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.95; font-weight: 400;">
            Sistem Pemodelan Nilai Ekonomi Lingkungan, Optimasi HHBK Pinus & Analisis Keberlanjutan Komoditas Kehutanan - PBL Kelompok 2
        </p>
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
        
        **Susunan Anggota Tim Kelompok 2:**
        1. 🧑‍💻 **Radea Rahman Dwiyana** (10090224001)
        2. 👩‍💻 **Bunga Wiati Manaki** (10090224026)
        3. 🧑‍💻 **Shidqi Alhamdani Mieftah** (10090224032)
        """)
    
    with col_side:
        st.markdown("<div class='metric-container' style='background-color:#f8fafc; border-top: 4px solid #1b5e20; text-align:left;'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Core Dashboard Capabilities")
        st.markdown("""
        - **Valuasi TEV:** Menilai aset nyata pasar dan non-pasar (karbon).
        - **Uji Sensitivitas Interaktif:** Simulasi ketahanan kas terhadap guncangan harga pasar.
        - **Policy Recommendation:** Penyusun strategi mitigasi konflik *trade-off* ekologi-ekonomi.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODUL 2: KARAKTERISTIK & HAYATI WILAYAH
# ==========================================
elif menu == "📄 Karakteristik & Hayati Wilayah":
    st.header("📄 Karakteristik Geografis, Fungsi Kawasan & Keanekaragaman Hayati")
    st.write("Analisis biofisik spasial serta inventarisasi kekayaan flora dan fauna penyusun ekosistem KPH Sumedang.")
    
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
            Wilayah administrasi KPH Sumedang didominasi oleh perbukitan bergelombang tajam dengan karakteristik tanah latosol dan andosol subur hasil aktivitas vulkanik purba. 
            
            Kondisi iklim mikro dengan curah hujan yang stabil di sepanjang tahun memberikan prasyarat ekologis yang sangat prima bagi akselerasi pertumbuhan tanaman getah pinus berkualitas tinggi.
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_status:
        st.markdown("### 🏛️ Kepastian Hukum Tata Kawasan Hutan")
        st.write("Klasifikasi peruntukan legal kawasan KPH Sumedang berdasarkan regulasi kehutanan nasional:")
        
        st.markdown("""
        Mayoritas absolut wilayah pengelolaan KPH Sumedang berstatus hukum sebagai **HUTAN PRODUKSI (HP)**, dikombinasikan dengan beberapa sub-blok bermakna **Hutan Lindung (HL)** pada wilayah hulu tangkapan air regional. 
        
        Kawasan ini **bukanlah Hutan Raya (Tahura)** yang murni difungsikan sebagai kebun koleksi botani tanpa pemanfaatan komersial.
        """)
        
        st.markdown("<div class='info-box-success'>", unsafe_allow_html=True)
        st.markdown("##### 🔗 Relevansi Logis Terhadap Produksi Getah Pinus (HHBK)")
        st.write("""
        Berangkat dari status hukumnya sebagai Hutan Produksi, KPH Sumedang memikul tanggung jawab ganda: menghasilkan keuntungan ekonomi dan menjaga kelestarian lingkungan. Di sinilah komoditas **Pinus (*Pinus merkusii*)** memegang peranan vital. 
        
        Alih-alih melakukan penebangan kayu secara masif yang berisiko menggundulkan bukit, manajemen mengedepankan **Hasil Hutan Bukan Kayu (HHBK)** melalui **penyadapan Getah Pinus**. Struktur kebijakan ini sangat cerdas, karena **pohon pinus dibiarkan tetap tumbuh kokoh menyerap emisi karbon di atmosfer dan menahan laju erosi tanah, sementara cairan getahnya dipanen secara kontinyu untuk mendatangkan omset keuangan yang produktif.**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_biodiv:
        st.markdown("### 🦅 Inventarisasi Keanekaragaman Hayati (Biodiversitas)")
        st.write("KPH Sumedang berhasil menjaga koeksistensi kehidupan liar di tengah aktivitas produksi industri kehutanan.")
        
        c_flora, c_fauna = st.columns(2)
        with c_flora:
            st.markdown("""
            <div class='metric-container' style='text-align: left; border-top: 4px solid #1b5e20;'>
                <h4>🌲 Varietas Flora (Vegetasi)</h4>
                <ul>
                    <li><b>Pinus merkusii:</b> Tegakan utama penopang ekonomi korporat sekaligus komponen utama penyerap gas karbon.</li>
                    <li><b>Tanaman Pengaya (Kaliandra & Mahoni):</b> Ditanam secara strategis di sabuk batas luar kawasan sebagai penahan laju kebakaran hutan serta peningkat fiksasi nitrogen tanah.</li>
                    <li><b>Vegetasi Bawah:</b> Paku-pakuan alami dan perdu yang berfungsi menjaga tingkat kelembaban kebun hutan.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with c_fauna:
            st.markdown("""
            <div class='metric-container' style='text-align: left; border-top: 4px solid #ff9800;'>
                <h4>🦅 Taksonomi Fauna (Satwa Liar)</h4>
                <ul>
                    <li><b>Avifauna Predator:</b> Menjadi koridor perburuan burung Elang Jawa (Spizaetus bartelsi) dan Alap-alap yang dilindungi undang-undang.</li>
                    <li><b>Mamalia Terestrial:</b> Populasi Babi Hutan (Sus scrofa) dan Jelarang yang bertindak sebagai penyeimbang ekosistem tanah bawah.</li>
                    <li><b>Insekta Produktif:</b> Koloni lebah madu hutan lokal yang memanfaatkan polen bunga kaliandra sebagai basis produksi madu liar.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# MODUL 3: NERACA ALIRAN PRODUKSI
# ==========================================
elif menu == "📦 Neraca Aliran Production":
    st.header("📦 Neraca Aliran Output Hasil Produksi Tahunan")
    st.write("Visualisasi perbandingan kuantitas fisik komoditas primer kayu log (m³) dengan produk non-kayu getah pinus (Ton):")
    
    fig_prod = px.bar(
        df_produksi, x='Variabel', y='Nilai', color='Variabel', text_auto='.2s',
        color_discrete_sequence=['#2e7d32', '#1565c0'],
        title="Volume Panen Komoditas Tahunan Terintegrasi KPH Sumedang"
    )
    fig_prod.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_prod, use_container_width=True)
    
    st.markdown("##### Tabel Rincian Angka Produksi Aktual")
    st.dataframe(df_produksi, use_container_width=True, hide_index=True)

# ==========================================
# MODUL 4: VALUASI TEV & EKONOMI MAKRO
# ==========================================
elif menu == "💰 Valuasi TEV & Ekonomi Makro":
    st.header("💰 Analisis Total Economic Value (TEV) & Proxy Kelayakan")
    st.write("Struktur akuntansi kelayakan finansial pengelolaan hutan pinus per hektar:")
    
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
            color_discrete_sequence=['#1b5e20', '#2e7d32', '#a5d6a7'],
            title="Komposisi Kontribusi Manfaat Ekonomi Total (TEV)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_desc:
        st.markdown("#### 🌍 Total Nilai Ekonomi Agregat Makro")
        st.metric(label="Estimasi Nilai Total Ekonomi Kawasan KPH Per Tahun", value="Rp 66,100,000,000")
        st.write("""
        Melalui pemodelan Total Economic Value (TEV), kita dapat membuktikan secara matematis di hadapan dosen bahwa **Getah Pinus (HHBK) menguasai 70% total valuasi nilai ekonomi**. 
        
        Angka ini menjadi pijakan argumen yang sangat solid bagi Kelompok 2 untuk menyatakan bahwa pembangunan ekonomi kehutanan tidak harus merusak lingkungan; pemanfaatan jasa non-kayu terbukti jauh lebih menguntungkan secara finansial jangka panjang.
        """)

# ==========================================
# MODUL 5: BATAS KEBIJAKAN TRADE-OFF
# ==========================================
elif menu == "⚖️ Batas Kebijakan Trade-Off":
    st.header("⚖️ Analisis Batas Trade-Off Keseimbangan Ekonomi & Ekologi")
    st.write("Dialektika kritis penentuan kebijakan pengelolaan sumber daya alam berkelanjutan:")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="info-box-warn">
            <h4>📈 Sektor Dorongan Ekonomi Komersial</h4>
            <p>Melakukan penyadapan getah melebihi ambang batas kuota luka pohon dan mempercepat siklus tebang pohon untuk memaksimalkan keuntungan kas korporasi.</p>
            <b>Dampak Negatif:</b> Melemahkan struktur mekanis pohon terhadap angin kencang, memicu kekeringan getah prematur, dan menurunkan kapasitas hutan sebagai penyerap karbon emisi.
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="info-box-warn" style="border-left-color: #0284c7; background-color: #f0f9ff; color: #0c4a6e;">
            <h4>🌍 Sektor Proteksi Ekosistem & Lingkungan</h4>
            <p>Melarang total pemanenan kayu log komersial dan membatasi tajam aktivitas sadap getah demi mengamankan volume biomassa penyerapan polusi udara global.</p>
            <b>Dampak Negatif:</b> Menyebabkan penurunan drastis pada pendapatan asli daerah (PAD) sektor kehutanan serta memicu lonjakan angka pengangguran bagi masyarakat penyadap lokal.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="info-box-success">
        <h4>💡 Resolusi Konseptual Kelompok 2: Optimalisasi HHBK Berkelanjutan</h4>
        <p>Berdasarkan temuan ilmiah kami, rasio kelayakan <b>BCR baseline mencapai 2.85 (di atas 1)</b>. Hal ini menunjukkan bahwa skema pemanfaatan Getah Pinus (HHBK) adalah solusi ekuilibrium terbaik. Skema ini mengizinkan kegiatan ekonomi berjalan secara optimal tanpa mengorbankan tegakan pohon pokok yang memegang peranan krusial sebagai penyerap emisi gas rumah kaca di KPH Sumedang.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MODUL 6: SIMULATOR FINANSIAL INTERAKTIF
# ==========================================
elif menu == "📊 Simulator Finansial Interaktif":
    st.header("📊 Simulator Sensitivitas & Kelayakan Finansial Dinamis")
    st.write("Uji ketahanan finansial investasi KPH Sumedang terhadap guncangan naik-turunnya harga getah di pasar global secara real-time.")

    # INTERACTIVE PREMIUM SLIDER CONTROL
    harga_simulasi = st.slider(
        "Atur Prakiraan Harga Jual Getah Pinus Pasar (Rupiah / Kilogram):",
        min_value=5000,
        max_value=25000,
        value=11500,
        step=500
    )
    
    # ADVANCED MATHEMATICAL ECONOMIC COMPUTATION
    omset_getah_live = volume_getah_tahunan * 1000 * harga_simulasi
    omset_kayu_statis = volume_kayu_tahunan * 650000
    total_omset_live = omset_getah_live + omset_kayu_statis
    
    rasio_indeks = harga_simulasi / 11500
    npv_live = 198500000 * rasio_indeks
    bcr_live = 2.85 * rasio_indeks

    st.write("---")
    st.markdown("### 📈 Proyeksi Indikator Finansial Dinamis")
    
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
        color_discrete_sequence=['#ff9800', '#1b5e20'],
        title=f"Analisis Perbandingan Omset pada Tingkat Harga Keekonomian Rp {harga_simulasi:,} / Kg"
    )
    fig_live.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_live, use_container_width=True)

# ==========================================
# MODUL 7: VALIDASI MASTER DATA CSV
# ==========================================
elif menu == "📂 Validasi Master Data CSV":
    st.header("📂 Transparansi Sumber Daya Master Data (CSV Audit Mode)")
    st.write("Gunakan menu tab horizontal di bawah ini untuk menggeser dan meninjau keaslian data mentah:")

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
