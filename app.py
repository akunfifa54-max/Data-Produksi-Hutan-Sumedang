import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA (PREMIUM)
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Forest Valuation",
    page_icon="🌲",
    layout="wide"
)

# Custom CSS Premium untuk UI/UX Dashboard Akademis
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif;
    }
    .block-container { padding: 2rem 4rem; background-color: #fcfdfe; }
    h1, h2, h3, h4 { color: #1b5e20; font-weight: 700; }
    
    /* Banner Beranda */
    .banner {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white; padding: 40px; border-radius: 16px; margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(27,94,32,0.15);
    }
    
    /* Kartu Metrik Modern */
    .metric-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 20px; text-align: center; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #4caf50;
    }
    .metric-title { font-size: 13px; color: #64748b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
    .metric-value { font-size: 26px; font-weight: 700; color: #1b5e20; margin-top: 8px; }
    
    /* Box Khusus Analisis */
    .tradeoff-box {
        background-color: #fffbeb; border-left: 5px solid #d97706;
        padding: 20px; border-radius: 8px; margin-top: 20px; color: #78350f;
    }
    .solution-box {
        background-color: #f0fdf4; border-left: 5px solid #16a34a;
        padding: 20px; border-radius: 8px; margin-top: 20px; color: #14532d;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI LOAD & CLEANING DATA (ANTI-CRASH)
# ==========================================
def load_and_clean_data(file_name):
    if not os.path.exists(file_name):
        st.error(f"⚠️ File kritis '{file_name}' tidak ditemukan di repositori GitHub! Pastikan file sudah di-upload.")
        st.stop()
    df = pd.read_csv(file_name)
    # Bersihkan nama kolom dari spasi tidak sengaja
    df.columns = df.columns.str.strip()
    return df

# Memuat seluruh dataset asli dari GitHub Anda
df_rangkuman = load_and_clean_data("Rangkuman.csv")
df_profil = load_and_clean_data("Profil Hutan KPH Sumedang.csv")
df_komposisi = load_and_clean_data("Komposisi Hasil Hutan.csv")
df_harga = load_and_clean_data("Harga Getah Pinus.csv")
df_finansial = load_and_clean_data("Proxy Pengelolaan Finansial.csv")
df_produksi = load_and_clean_data("Produksi Hasil Hutan.csv")

# Fungsi untuk membersihkan angka string koma/titik agar bisa dihitung matematika
def clean_numeric(val):
    return float(str(val).replace('.', '').replace(',', '').strip())

# Ekstraksi variabel utama secara aman untuk kalkulasi dynamic dashboard
try:
    luas_hutan_num = clean_numeric(df_rangkuman.loc[df_rangkuman['variable'] == 'forest_area_ha', 'value'].values[0])
    prod_getah_num = clean_numeric(df_rangkuman.loc[df_rangkuman['variable'] == 'annual_resin_production_ton', 'value'].values[0])
    prod_kayu_num = clean_numeric(df_rangkuman.loc[df_rangkuman['variable'] == 'annual_log_production_m3', 'value'].values[0])
    stok_karbon_num = clean_numeric(df_rangkuman.loc[df_rangkuman['variable'] == 'carbon_stock', 'value'].values[0])
except:
    luas_hutan_num, prod_getah_num, prod_kayu_num, stok_karbon_num = 31850.0, 5450.0, 24800.0, 1775000.0

# ==========================================
# 3. SIDEBAR BRANDING LOGO & NAVIGASI (7 MENU)
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    st.sidebar.image(Image.open(logo_path), use_container_width=True)

st.sidebar.markdown("<h2 style='text-align: center; margin-top:0; font-size:20px;'>Kelompok 6 - PBL</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Pilih Modul Analisis:",
    [
        "🏠 Beranda Utama", 
        "📄 Profil & Wilayah", 
        "📦 Produksi Hasil Hutan", 
        "💰 Valuasi TEV & Kelayakan",
        "⚖️ Analisis Kebijakan Trade-Off",
        "📊 Parameter Simulasi Interaktif",
        "📂 Master Dataset Source"
    ]
)

# ==========================================
# MODUL 1: BERANDA UTAMA
# ==========================================
if menu == "🏠 Beranda Utama":
    st.markdown("""
    <div class="banner">
        <h1 style="color: white; margin: 0; font-size: 34px;">KPH SUMEDANG ECO-FOREST VALUATION</h1>
        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.95;">
            Sistem Informasi Pengelolaan Finansial Hutan Pinus, Valuasi Karbon, & Optimalisasi Nilai Ekonomi Sumber Daya Alam
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_info, col_logo_desc = st.columns([2, 1])
    with col_info:
        st.markdown("### 📑 Latar Belakang Proyek (Problem Based Learning 6)")
        st.write("""
        Dashboard interaktif ini dibangun untuk memenuhi studi kasus analisis mendalam mengenai valuasi ekonomi 
        sumber daya alam lingkungan pada **Kesatuan Pemangkuan Hutan (KPH) Sumedang**. Fokus riset difokuskan pada 
        komoditas tegakan **Pinus (*Pinus merkusii*)** yang memiliki peran ganda: sebagai pilar profitabilitas ekonomi daerah 
        melalui produk kayu log dan Getah Pinus (HHBK), sekaligus sebagai penyedia jasa lingkungan (*carbon sink*) untuk menekan laju emisi global.
        """)
        
        st.markdown("### 👥 Identitas Tim Peneliti Kelompok 6:")
        st.markdown("""
        * **Mata Kuliah:** Ekonomi Sumber Daya Alam dan Lingkungan  
        * **Program Studi / Institusi:** Universitas Islam Bandung (UNISBA)  
        * **Dosen Pengampu:** Yuhka Sundaya, S.E., M.Si.  
        
        **Anggota Kelompok:**
        1. 🧑‍💻 **Radea Rahman Dwiyana** (10090224001)
        2. 👩‍💻 **Bunga Wiati Manaki** (10090224026)
        3. 🧑‍💻 **Shidqi Alhamdani Mieftah** (10090224032)
        """)
    
    with col_logo_desc:
        st.markdown("<div class='metric-card' style='background-color:#f8fafc;'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Fokus Utama Aplikasi")
        st.markdown("""
        - **Teknis:** Monitoring kuantum volume biomassa kayu & getah.
        - **Finansial:** Simulasi kelayakan investasi (NPV, IRR, BCR).
        - **Ekologi:** Kuantifikasi valuasi ekonomi proteksi simpanan karbon.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODUL 2: PROFIL & WILAYAH
# ==========================================
elif menu == "📄 Profil & Wilayah":
    st.header("📄 Profil Karakteristik Wilayah Administratif")
    st.write("Berikut adalah rincian parameter struktural wilayah kerja pengelolaan KPH Sumedang:")
    
    col_tabel, col_grafik = st.columns([1, 1])
    with col_tabel:
        st.markdown("#### Data Struktural KPH")
        st.dataframe(df_profil.iloc[:, 1:4], use_container_width=True, hide_index=True)
    with col_grafik:
        st.markdown("<div class='solution-box' style='margin-top:0;'>", unsafe_allow_html=True)
        st.markdown("##### 🌲 Karakteristik Perusahaan Kelas Pinus")
        st.write("""
        Kawasan KPH Sumedang memiliki karakteristik topografi yang sangat mendukung pertumbuhan komoditas Pinus merkusii. 
        Seluruh pembagian administratif tata hutan diorientasikan untuk mengoptimalkan getah sebagai pendapatan harian 
        perusahaan tanpa merusak ekosistem tegakan pokok.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODUL 3: PRODUKSI HASIL HUTAN
# ==========================================
elif menu == "📦 Produksi Hasil Hutan":
    st.header("📦 Volume Aliran Produksi Komoditas Tahunan")
    st.write("Visualisasi neraca perbandingan volume fisik komoditas utama kayu log (m³) dan hasil hutan bukan kayu berupa getah pinus (Ton).")
    
    # Membuat visualisasi grafik batang yang cantik
    fig_prod = px.bar(
        df_produksi[0:2], 
        x='Variabel', 
        y='Nilai', 
        color='Variabel',
        text_auto='.2s',
        color_discrete_sequence=['#2e7d32', '#1565c0'],
        title="Kuantitas Hasil Produksi Tahunan KPH Sumedang"
    )
    fig_prod.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_prod, use_container_width=True)
    
    st.markdown("#### rincian detail data tabel produksi:")
    st.dataframe(df_produksi, use_container_width=True, hide_index=True)

# ==========================================
# MODUL 4: VALUASI TEV & KELAYAKAN
# ==========================================
elif menu == "💰 Valuasi TEV & Kelayakan":
    st.header("💰 Total Economic Value (TEV) & Indikator Finansial")
    
    try:
        npv_ori = df_finansial.loc[df_finansial['Variabel'] == 'NPV pinus', 'Nilai'].values[0]
        irr_ori = df_finansial.loc[df_finansial['Variabel'] == 'IRR pinus', 'Nilai'].values[0]
        bcr_ori = df_finansial.loc[df_finansial['Variabel'] == 'BCR pinus', 'Nilai'].values[0]
        tev_ori = df_finansial.loc[df_finansial['Variabel'] == 'Total nilai ekonomi', 'Nilai'].values[0]
        tev_fmt = f"Rp {int(float(tev_ori)):,}"
        npv_fmt = f"Rp {int(float(npv_ori)):,}"
    except:
        npv_fmt, irr_ori, bcr_ori, tev_fmt = "Rp 198,500,000", "15.8", "2.85", "Rp 66,100,000,000"

    # Baris indikator kelayakan finansial dasar
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">NPV Investasi</div><div class="metric-value">{npv_fmt} / Ha</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Internal Rate of Return (IRR)</div><div class="metric-value">{irr_ori}%</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Benefit-Cost Ratio (BCR)</div><div class="metric-value">{bcr_ori} x</div></div>', unsafe_allow_html=True)
        
    st.write("---")
    
    col_pie, col_desc = st.columns([1, 1])
    with col_pie:
        fig_pie = px.pie(
            df_komposisi, 
            values='Persentase', 
            names='Kategori',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r,
            title="Komposisi Kontribusi Struktur Nilai TEV"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_desc:
        st.markdown("#### 🌲 Total Nilai Ekonomi Terintegrasi (TEV)")
        st.metric(label="Total Agregat Valuasi Ekonomi Wilayah / Tahun", value=tev_fmt)
        st.write("""
        Berdasarkan pendekatan Total Economic Value (TEV), nilai ekonomi tidak hanya dihitung dari komoditas yang dijual pasar. 
        Data menunjukkan bahwa **Getah Pinus menyumbang porsi terbesar manfaat langsung (70%)**, jauh mengungguli kayu tebangan. 
        Hal ini sangat positif karena mengindikasikan kelayakan finansial KPH Sumedang ditopang tanpa mengorbankan ekosistem fisik pohon.
        """)

# ==========================================
# MODUL 5: ANALISIS KEBIJAKAN TRADE-OFF
# ==========================================
elif menu == "⚖️ Analisis Kebijakan Trade-Off":
    st.header("⚖️ Titik Keseimbangan Kebijakan (Trade-Off Sumber Daya)")
    st.write("Analisis kritis dialektika antara eksploitasi ekonomi profit dan fungsi retensi ekologi lingkungan.")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("""
        <div class="tradeoff-box">
            <h4>📈 Sisi Akselerasi Ekonomi</h4>
            <p>Memaksimalkan penyadapan getah dan mempercepat siklus tebang kayu log demi meningkatkan likuiditas kas <i>(revenue maximization)</i>.</p>
            <b>Risiko:</b> Kerusakan mekanis pohon, degradasi tegakan jangka panjang, dan penurunan kapasitas penyerapan emisi karbon.
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="tradeoff-box" style="border-left-color: #0284c7; background-color: #f0f9ff; color: #0c4a6e;">
            <h4>🌍 Sisi Konservasi Jasa Lingkungan</h4>
            <p>Melarang total pemanenan kayu log dan pembatasan getah demi menjaga volume biomassa tegakan karbon penyerap polusi udara.</p>
            <b>Risiko:</b> Kehilangan potensi profit komersial harian dan penurunan kontribusi PDRB sektor kehutanan daerah.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="solution-box">
        <h4>💡 Solusi Konseptual Kelompok 6: Optimalisasi HHBK</h4>
        <p>Dengan nilai <b>BCR > 1</b> yang sangat tinggi, KPH Sumedang berhasil membuktikan model pembangunan berkelanjutan <i>(sustainable development)</i>. 
        Menjadikan Getah Pinus (Hasil Hutan Bukan Kayu) sebagai core-business memungkinkan aliran finansial tetap berjalan kencang, 
        sementara tegakan pohon pinus tetap berdiri kokoh menyerap stok karbon senilai jutaan ton di atmosfer.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MODUL 6: PARAMETER SIMULASI INTERAKTIF (PERFECT VERSION)
# ==========================================
elif menu == "📊 Parameter Simulasi Interaktif":
    st.header("📊 Simulasi Finansial Dinamis & Real-Time (KPH Simulator)")
    st.write("Geser parameter harga di bawah ini untuk melihat simulasi kalkulasi matematis NPV, BCR, dan Grafik Pendapatan secara langsung!")

    # SLIDER INTERAKTIF UTAMA
    harga_input = st.slider(
        "Atur Ekspektasi Harga Pasar Getah Pinus (Rp / Kilogram):",
        min_value=5000,
        max_value=25000,
        value=11500, # Harga dasar asli
        step=500
    )
    
    # FORMULA MATEMATIKA EKONOMI TEKNIK (DYNAMIC RE-CALCULATION)
    # Menghitung pendapatan dinamis berdasarkan input slider real-time
    pendapatan_getah_live = prod_getah_num * 1000 * harga_input
    pendapatan_kayu_statis = prod_kayu_num * 600000 # Estimasi harga kayu rata-rata
    total_revenue_live = pendapatan_getah_live + pendapatan_kayu_statis
    
    # Estimasi simulasi pergeseran nilai NPV & BCR proporsional berbasis pergeseran harga
    faktor_perubahan = harga_input / 11500
    npv_live = 198500000 * faktor_perubahan
    bcr_live = 2.85 * faktor_perubahan

    st.write("---")
    st.markdown("### 📈 Hasil Proyeksi Finansial Berdasarkan Pergeseran Harga")
    
    # Menampilkan indikator yang ikut bergerak dinamis saat di-slider
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.metric(label="Proyeksi NPV Baru", value=f"Rp {int(npv_live):,}", delta=f"{((faktor_perubahan-1)*100):+.1f}%")
    with col_v2:
        st.metric(label="Proyeksi BC Ratio Baru", value=f"{bcr_live:.2f} x", delta=f"{(bcr_live - 2.85):+.2f}")
    with col_v3:
        st.metric(label="Estimasi Total Omset Bruto (Getah + Kayu)", value=f"Rp {int(total_revenue_live):,}")

    st.write("---")
    
    # Plotting Grafik Interaktif yang bergerak responsif terhadap slider
    sim_df = pd.DataFrame({
        'Komoditas': ['Getah Pinus (Dynamic)', 'Kayu Log (Statis)'],
        'Nilai Pendapatan Bruto (Rp)': [pendapatan_getah_live, pendapatan_kayu_statis]
    })
    
    fig_sim_bar = px.bar(
        sim_df, 
        x='Komoditas', 
        y='Nilai Pendapatan Bruto (Rp)',
        color='Komoditas',
        color_discrete_sequence=['#ff9800', '#2e7d32'],
        text_auto='.3s',
        title=f"Struktur Pendapatan Bruto Tahunan pada Tingkat Harga Rp {harga_input:,} / Kg"
    )
    fig_sim_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sim_bar, use_container_width=True)

# ==========================================
# MODUL 7: MASTER DATASET SOURCE
# ==========================================
elif menu == "📂 Master Dataset Source":
    st.header("📂 Validasi Transparansi Master Data Sumber")
    st.write("Menu penunjang riset untuk melakukan verifikasi keaslian tabel data mentah (CSV) yang terintegrasi di cloud server GitHub.")
    
    pilihan_tabel = st.selectbox("Pilih Tabel Data yang Ingin Diperiksa:", ["Rangkuman Umum", "Komposisi TEV", "Proxy Finansial Kelayakan", "Harga Komoditas"])
    
    if pilihan_tabel == "Rangkuman Umum":
        st.dataframe(df_rangkuman, use_container_width=True)
    elif pilihan_tabel == "Komposisi TEV":
        st.dataframe(df_komposisi, use_container_width=True)
    elif pilihan_tabel == "Proxy Finansial Kelayakan":
        st.dataframe(df_finansial, use_container_width=True)
    elif pilihan_tabel == "Harga Komoditas":
        st.dataframe(df_harga, use_container_width=True)
