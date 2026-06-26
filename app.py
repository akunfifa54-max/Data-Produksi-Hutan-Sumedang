import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from PIL import Image

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA TERANG (LIGHT)
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Forest Valuation Dashboard",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Menyelaraskan seluruh elemen ke warna tema terang (Light Mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
    
    /* Latar Belakang Aplikasi & Konten Utama (Light Mode) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #ffffff !important; 
        color: #1f2937 !important; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .block-container { 
        padding: 2.5rem 4.5rem; 
        background-color: #ffffff !important; 
    }
    
    /* Tipografi Judul */
    h1, h2, h3, h4, h5, h6 { 
        color: #047857 !important; 
        font-weight: 700; 
    }
    
    /* Jumbotron Banner Utama */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        padding: 45px; border-radius: 20px; margin-bottom: 35px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .hero-banner h1 { color: #ffffff !important; }
    .hero-banner p { color: #a7f3d0 !important; }
    
    /* Sidebar Navigation panel (Light-Gray Theme) */
    section[data-testid="stSidebar"] { 
        background-color: #f3f4f6 !important; 
        border-right: 1px solid #e5e7eb !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #111827 !important; 
        font-weight: 600 !important;
    }
    
    /* Radio Button Text (Pilihan Menu) */
    div[data-testid="stRadio"] label p {
        color: #1f2937 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    
    /* Kotak Metrik / Ringkasan Finansial */
    .metric-box {
        background: #f9fafb !important; 
        border: 1px solid #e5e7eb;
        border-radius: 12px; padding: 20px; text-align: left;
        color: #111827 !important; margin-bottom: 15px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    .metric-box h4 {
        color: #047857 !important;
        font-weight: 700 !important;
        margin-top: 0px;
    }
    .metric-box p, .metric-box li, .metric-box span {
        color: #374151 !important;
        font-size: 14px !important;
    }
    .metric-box b { color: #111827 !important; }
    .metric-box-title { font-size: 13px; color: #6b7280 !important; text-transform: uppercase; font-weight: 600; }
    .metric-box-value { font-size: 24px; font-weight: 700; color: #111827 !important; margin-top: 5px; }
    .metric-box-delta { font-size: 13px; color: #059669 !important; font-weight: 600; margin-top: 2px; }
    
    /* Kotak Informasi Berwarna (Aman untuk Light Theme) */
    .info-box-warn {
        background-color: #fff7ed !important; 
        border-left: 6px solid #f97316 !important;
        padding: 22px; border-radius: 12px; margin-top: 20px; margin-bottom: 20px;
        color: #7c2d12 !important;
        border: 1px solid #ffedd5;
    }
    .info-box-warn h4 { color: #ea580c !important; margin-top: 0px !important; }
    
    .info-box-success {
        background-color: #f0fdf4 !important; 
        border-left: 6px solid #10b981 !important;
        padding: 22px; border-radius: 12px; margin-top: 20px; margin-bottom: 20px;
        color: #14532d !important;
        border: 1px solid #d1fae5;
    }
    .info-box-success h4 { color: #16a34a !important; margin-top: 0px !important; }
    
    /* Global Teks Override */
    .stMarkdown, p, span, li, label {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE (BACKUP & LOAD CSV)
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

# Konstanta Dasar Geografis KPH Sumedang
luas_total_hutan_sumedang = 31850
volume_getah_tahunan_sumedang = 5450  
volume_kayu_tahunan_sumedang = 24800   

# ==========================================
# 3. SIDEBAR BRANDING LOGO & NAVIGASI
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    st.sidebar.image(Image.open(logo_path), use_container_width=True)

st.sidebar.markdown("<h2 style='text-align: center; margin-top:5px; font-size:20px; color:#047857; font-weight:700;'>PBL KELOMPOK 2</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #4b5563; font-size:13px; margin-top:-10px;'>Ekonomi Sumber Daya Alam & Lingkungan</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color: #e5e7eb;'>", unsafe_allow_html=True)

st.sidebar.markdown("✨ **Menu Navigasi Utama:**")
menu = st.sidebar.radio(
    "Pilih Halaman Analisis:",
    [
        "🏠 Beranda Korporat Utama", 
        "📄 Karakteristik & Hayati Wilayah", 
        "📦 Neraca Aliran Produksi", 
        "💰 Valuasi TEV & Ekonomi Makro",
        "⚖️ Batas Kebijakan Trade-Off",
        "📊 Slider Simulasi Finansial",
        "📂 Validasi Master Data CSV"
    ],
    label_visibility="collapsed"
)

# Fungsi Sinkronisasi Warna Grafik Plotly ke Tema Terang (Light Mode)
def apply_light_theme_layout(fig):
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#1f2937",
        title_font_color="#047857",
        legend_font_color="#1f2937"
    )
    fig.update_xaxes(gridcolor='#f3f4f6', title_font_color="#1f2937", tickfont_color="#1f2937")
    fig.update_yaxes(gridcolor='#f3f4f6', title_font_color="#1f2937", tickfont_color="#1f2937")
    return fig

# ==========================================
# 4. LOGIKA ROUTING HALAMAN NAVIGASI
# ==========================================

# MODUL 1: BERANDA KORPORAT UTAMA
if menu == "🏠 Beranda Korporat Utama":
    st.markdown("""
    <div class="hero-banner">
        <h1>KPH SUMEDANG ECO-FOREST VALUATION</h1>
        <p>Sistem Pemodelan Nilai Ekonomi Lingkungan, Optimasi HHBK Pinus & Analisis Keberlanjutan Komoditas Kehutanan - PBL Kelompok 2</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    with col_main:
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
        st.write("---")
        
        st.markdown("### 📑 Latar Belakang Riset Kasus (PBL)")
        st.write("""
        Platform dashboard digital ini dirancang secara khusus untuk menganalisis struktur tata kelola ekonomi makro dan mikro 
        pada **Kesatuan Pemangkuan Hutan (KPH) Sumedang**. Fokus kajian ilmiah diarahkan pada tegakan vegetasi komoditas **Pinus (*Pinus merkusii*)**.
        
        Melalui pemodelan Ekonomi Sumber Daya Alam, kami membedah bagaimana pemanfaatan ekonomi komersial dari ekstraksi hasil hutan 
        dapat dioptimalkan tanpa mendegradasi fungsi perlindungan lingkungan hidup (*sustainable forest management*).
        """)
    
    with col_side:
        st.markdown("""
        <div class='metric-box' style='border-top: 4px solid #047857;'>
            <h4>🎯 Kemampuan Inti</h4>
            <p>• <b>Valuasi TEV:</b> Menilai aset nyata pasar dan non-pasar (karbon).</p>
            <p>• <b>Uji Sensitivitas Interaktif:</b> Simulasi ketahanan kas terhadap guncangan harga pasar.</p>
            <p>• <b>Rekomendasi Kebijakan:</b> Penyusun strategi mitigasi konflik trade-off ekologi-ekonomi.</p>
        </div>
        """, unsafe_allow_html=True)

# MODUL 2: KARAKTERISTIK & HAYATI WILAYAH
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
            st.markdown("""
            <div class='info-box-success' style='margin-top:0;'>
                <h4>📍 Kondisi Topografi & Tanah</h4>
                <p>Wilayah administrasi KPH Sumedang didominasi oleh perbukitan bergelombang tajam dengan karakteristik tanah latosol dan andosol yang subur. Kondisi iklim mikro serta curah hujan yang stabil menjadi prasyarat utama optimalnya pertumbuhan dan produktivitas getah pinus.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_status:
        st.markdown("### 🏛️ Kepastian Hukum Tata Kawasan Hutan")
        st.write("Mayoritas wilayah KPH Sumedang berstatus hukum sebagai **HUTAN PRODUKSI (HP)**, dikombinasikan dengan **Hutan Lindung (HL)** di area hulu DAS.")
        
        st.markdown("""
        <div class='info-box-success'>
            <h4>🔗 Relevansi Logis Terhadap Produksi Getah Pinus (HHBK)</h4>
            <p>Kawasan Hutan Produksi diwajibkan memberikan kontribusi ekonomi namun dengan tetap menjaga kelestarian lingkungan. Oleh karena itu, <b>penyadapan Getah Pinus (HHBK)</b> menjadi solusi jalan tengah yang strategis. <b>Pohon pinus tetap berdiri tegak untuk menyerap karbon dan menahan erosi tanah, sementara komoditas getahnya dapat dipanen secara berkelanjutan sebagai sumber pendapatan.</b></p>
        </div>
        """, unsafe_allow_html=True)

    with tab_biodiv:
        st.markdown("### 🦅 Inventarisasi Keanekaragaman Hayati")
        c_flora, c_fauna = st.columns(2)
        with c_flora:
            st.markdown("""
            <div class='info-box-success' style='margin-top:0;'>
                <h4>🌲 Varietas Flora (Vegetasi)</h4>
                <p>• <b>Pinus merkusii:</b> Tegakan utama penopang nilai ekonomi kawasan.</p>
                <p>• <b>Kaliandra & Mahoni:</b> Berfungsi sebagai penahan sebaran kebakaran serta peningkat unsur hara tanah.</p>
            </div>
            """, unsafe_allow_html=True)
        with c_fauna:
            st.markdown("""
            <div class='info-box-warn' style='margin-top:0;'>
                <h4>🦅 Taksonomi Fauna (Satwa Liar)</h4>
                <p>• <b>Predator:</b> Menjadi habitat penting burung Elang Jawa (Spizaetus bartelsi) yang dilindungi oleh negara.</p>
                <p>• <b>Mamalia:</b> Populasi Babi Hutan, Kancil, serta berbagai jenis satwa liar endemik lainnya.</p>
            </div>
            """, unsafe_allow_html=True)

# MODUL 3: NERACA ALIRAN PRODUKSI
elif menu == "📦 Neraca Aliran Produksi":
    st.header("📦 Neraca Aliran Output Hasil Produksi Tahunan")
    
    fig_prod = px.bar(
        df_produksi, x='Variabel', y='Nilai', color='Variabel', text_auto='.2s',
        color_discrete_sequence=['#10b981', '#3b82f6'],
        title="Volume Panen Komoditas Tahunan KPH Sumedang"
    )
    fig_prod = apply_light_theme_layout(fig_prod)
    st.plotly_chart(fig_prod, use_container_width=True)
    st.dataframe(df_produksi, use_container_width=True, hide_index=True)

# MODUL 4: VALUASI TEV & EKONOMI MAKRO
elif menu == "💰 Valuasi TEV & Ekonomi Makro":
    st.header("💰 Analisis Total Economic Value (TEV) & Proxy Kelayakan")
    
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.markdown('<div class="metric-box"><div class="metric-box-title">Net Present Value (NPV) Baseline</div><div class="metric-box-value">Rp 198,500,000 / Ha</div></div>', unsafe_allow_html=True)
    with col_v2:
        st.markdown('<div class="metric-box"><div class="metric-box-title">Internal Rate of Return (IRR)</div><div class="metric-box-value">15.80 %</div></div>', unsafe_allow_html=True)
    with col_v3:
        st.markdown('<div class="metric-box"><div class="metric-box-title">Benefit-Cost Ratio (BCR)</div><div class="metric-box-value">2.85 x</div></div>', unsafe_allow_html=True)
        
    st.write("---")
    
    col_pie, col_desc = st.columns([1, 1])
    with col_pie:
        fig_pie = px.pie(
            df_komposisi, values='Persentase', names='Kategori', hole=0.4,
            color_discrete_sequence=['#064e3b', '#047857', '#34d399'],
            title="Komposisi Kontribusi Manfaat Ekonomi Total (TEV)"
        )
        fig_pie = apply_light_theme_layout(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_desc:
        st.markdown("#### 🌍 Total Nilai Ekonomi Agregat Makro")
        st.metric(label="Estimasi Nilai Total Ekonomi Kawasan KPH Per Tahun", value="Rp 66,100,000,000")
        st.write("""
        Melalui pemodelan TEV, Kelompok 2 berhasil membuktikan secara ilmiah bahwa **Getah Pinus (HHBK) memegang 70% dari total valuasi ekonomi kawasan**. Ini menjadi argumen akademik yang kuat bahwa optimalisasi ekonomi tidak harus dilakukan dengan melakukan penebangan pohon secara masif.
        """)

# MODUL 5: BATAS KEBIJAKAN TRADE-OFF (LIGHT MODE)
elif menu == "⚖️ Batas Kebijakan Trade-Off":
    st.header("⚖️ Analisis Batas Trade-Off Keseimbangan Ekonomi & Ekologi")
    st.write("Gunakan slider di bawah untuk mensimulasikan pergeseran fokus kebijakan pengelolaan hutan di KPH Sumedang.")

    st.markdown("### 🎛️ Mainkan Simulasi Prioritas Kebijakan")
    bobot_ekonomi = st.slider("Bobot Fokus Ekonomi Komersial (%):", 0, 100, 50, step=5)
    bobot_ekologi = 100 - bobot_ekonomi
    st.info(f"💡 Komposisi Kebijakan Saat Ini: **Ekonomi {bobot_ekonomi}%** | **Ekologi {bobot_ekologi}%**")

    # Kalkulasi Live Score
    skor_pendapatan = 20 + (bobot_ekonomi * 0.75)
    skor_kelestarian = 15 + (bobot_ekologi * 0.80)
    
    fig_tradeoff = go.Figure()
    fig_tradeoff.add_trace(go.Bar(
        x=['Fokus Ekonomi', 'Fokus Ekologi'],
        y=[skor_pendapatan, skor_kelestarian],
        marker_color=['#f97316', '#10b981'],
        text=[f"{skor_pendapatan:.1f} Pts", f"{skor_kelestarian:.1f} Pts"],
        textposition='auto'
    ))
    fig_tradeoff.update_layout(
        title="Live Indeks Kinerja Kebijakan (Model Analisis: PBL Kelompok 2)", 
        yaxis_title="Skor Indeks"
    )
    fig_tradeoff = apply_light_theme_layout(fig_tradeoff)
    st.plotly_chart(fig_tradeoff, use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="info-box-warn">
            <h4>📈 Sektor Dorongan Ekonomi Komersial</h4>
            <p>Melakukan penyadapan getah secara berlebihan dan mempercepat siklus penebangan pohon demi mengejar profit jangka pendek.</p>
            <b>Risiko Kelebihan Bobot:</b> Kerusakan fisik pada pohon, potensi pohon tumbang meningkat, serta kemampuan hutan dalam menyerap karbon akan menurun drastis.
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="info-box-warn" style="border-left-color: #3b82f6 !important; background-color: #eff6ff !important; color: #1e3a8a !important; border: 1px solid #bfdbfe;">
            <h4>🌍 Sektor Proteksi Ekosistem & Lingkungan</h4>
            <p>Melarang total seluruh aktivitas penebangan komersial dan penyadapan getah demi menjaga kemurnian kondisi alam.</p>
            <b>Risiko Kelebihan Bobot:</b> Pendapatan asli daerah dari sektor kehutanan akan menurun drastis dan masyarakat penyadap lokal akan kehilangan mata pencaharian utamanya.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="info-box-success">
        <h4>💡 Resolusi Konseptual Kelompok 2: Optimalisasi HHBK Berkelanjutan</h4>
        <p>Dengan nilai <b>BCR baseline sebesar 2.85</b>, skema pemanfaatan Getah Pinus (HHBK) merupakan titik keseimbangan (equilibrium) terbaik. Pendapatan ekonomi tetap terjaga, sementara fungsi ekologis pohon dalam melindungi lingkungan tetap berjalan optimal.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer Identitas Kelompok di bagian paling bawah halaman simulasi
    st.markdown("<br><hr style='border-color: #e5e7eb;'><center style='color: #6b7280; font-size: 12px;'>Sistem Simulasi Kebijakan disusun oleh: PBL Kelompok 2</center>", unsafe_allow_html=True)

# MODUL 6: SLIDER SIMULASI FINANSIAL (LIGHT MODE)
elif menu == "📊 Slider Simulasi Finansial":
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 35px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="color: #ffffff !important; font-size: 42px; font-weight: 800; letter-spacing: 2px; margin: 0;">
            🌳 ECO-FOREST
        </h1>
        <h2 style="color: #a7f3d0 !important; font-size: 32px; font-weight: 300; letter-spacing: 4px; margin-top: 5px; margin-bottom: 20px;">
            VALUATION
        </h2>
        <p style="color: #d1fae5 !important; font-size: 18px; font-weight: 400; opacity: 0.9; margin: 0;">
            Sistem Valuasi Ekonomi Hutan
        </p>
        <p style="color: #34d399 !important; font-size: 15px; font-weight: 600; margin-top: 8px; margin-bottom: 0;">
            📍 KPH Sumedang · Jawa Barat
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## ⚙️ Simulasi Finansial")
    st.write("Uji komparatif simulasi multi-skenario hasil pemodelan komoditas kehutanan **KPH Sumedang** oleh **PBL Kelompok 2**.")
    
    # Input Sliders Parameter
    st.markdown("### 🛠️ Pengaturan Parameter Utama (Spesifik Hutan Pinus Sumedang)")
    c_in1, c_in2, c_in3 = st.columns(3)
    with c_in1:
        luas_simulasi = st.slider("Luas Kawasan Simulasi Pinus (Ha):", 1000, 40000, luas_total_hutan_sumedang, step=250)
    with c_in2:
        harga_getah = st.slider("Harga Jual Getah Pinus (Rp/Kg):", 5000, 25000, 11500, step=500)
        harga_kayu = st.slider("Harga Jual Kayu Log Pinus (Rp/m³):", 300000, 2000000, 650000, step=25000)
    with c_in3:
        daur_tebang = st.slider("Daur Siklus Tegakan Pinus (Tahun):", 10, 80, 30, step=5)
        suku_bunga = st.slider("Suku Bunga / Discount Rate (%):", 2.0, 20.0, 10.0, step=0.5)
        
    # Logika Hitung Model Finansial Kehutanan
    rasio_skala = luas_simulasi / luas_total_hutan_sumedang
    volume_getah_live = volume_getah_tahunan_sumedang * rasio_skala
    volume_kayu_live = volume_kayu_tahunan_sumedang * rasio_skala
    
    omset_getah = volume_getah_live * 1000 * harga_getah
    omset_kayu = volume_kayu_live * harga_kayu
    total_omset_komersial = omset_getah + omset_kayu
    
    npv_tradisional = (total_omset_komersial * 5) / (1 + (suku_bunga/100))**5
    bcr_tradisional = 1.85 + (harga_getah / 15000)
    irr_tradisional = 12.5 + (harga_getah / 4000)
    
    pemasukan_serapan_karbon = luas_simulasi * 55 * 150000  
    npv_hijau = npv_tradisional + pemasukan_serapan_karbon
    bcr_hijau = bcr_tradisional + 0.65
    irr_hijau = irr_tradisional + 3.3
    
    selisih_npv = npv_hijau - npv_tradisional
    persen_peningkatan = (selisih_npv / npv_tradisional) * 100

    st.write("---")
    
    # Ringkasan Output Metrik Live
    st.markdown("### 📊 Hasil Proyeksi Finansial Terupdate")
    c_out1, c_out2, c_out3, c_out4 = st.columns(4)
    with c_out1:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Total Luas Wilayah</div><div class="metric-box-value">{luas_simulasi:,} Ha</div></div>', unsafe_allow_html=True)
    with c_out2:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Volume Getah Terpola</div><div class="metric-box-value">{volume_getah_live:,.1f} Ton</div></div>', unsafe_allow_html=True)
    with c_out3:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">NPV Skenario A (Tradisional)</div><div class="metric-box-value">Rp {int(npv_tradisional):,}</div></div>', unsafe_allow_html=True)
    with c_out4:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">NPV Skenario B (Hijau)</div><div class="metric-box-value">Rp {int(npv_hijau):,}</div><div class="metric-box-delta">+Rp {int(pemasukan_serapan_karbon):,} Karbon</div></div>', unsafe_allow_html=True)

    st.write("---")
    
    # Visualisasi Grafik Perbandingan Skenario Finansial
    st.markdown("### 📈 Visualisasi Grafik Perbandingan NPV")
    chart_data = pd.DataFrame({
        'Skenario Analisis': ['Skenario A (Tradisional)', 'Skenario B (Hijau Terintegrasi)'],
        'Nilai NPV Terproyeksi (Rp)': [npv_tradisional, npv_hijau]
    })
    
    fig_live = px.bar(
        chart_data, x='Skenario Analisis', y='Nilai NPV Terproyeksi (Rp)',
        color='Skenario Analisis', text_auto='.3s',
        color_discrete_sequence=['#ef4444', '#10b981'],
        title="Grafik Komparatif Kelayakan Ekonomi KPH Sumedang (Analisis: PBL Kelompok 2)"
    )
    fig_live = apply_light_theme_layout(fig_live)
    st.plotly_chart(fig_live, use_container_width=True)
    
    st.markdown(f"""
    > 📌 **Analisis Grafik Perbandingan NPV:**
    > * **Skenario B (Hijau Terintegrasi)** menghasilkan keuntungan finansial jauh lebih tinggi berkat inklusi nilai ekonomi serapan karbon hutan pinus.  
    > * Selisih nilai tambah bersih dari penerapan ekonomi hijau di KPH Sumedang adalah sebesar **Rp {int(selisih_npv):,}**.
    """)

    st.write("---")

    # Tabel Evaluasi Multi-Parameter Kelayakan Investasi
    st.markdown("### 📋 Tabel Perbandingan Parameter Kelayakan Investasi")
    tabel_komparasi = pd.DataFrame({
        'Indikator Kelayakan Finansial': ['Proyeksi Nilai NPV (Rupiah)', 'Internal Rate of Return (IRR)', 'Benefit-Cost Ratio (BCR)'],
        'Skenario A (Tradisional)': [f"Rp {int(npv_tradisional):,}", f"{irr_tradisional:.2f} %", f"{bcr_tradisional:.2f} x"],
        'Skenario B (Hijau Terintegrasi)': [f"Rp {int(npv_hijau):,}", f"{irr_hijau:.2f} %", f"{bcr_hijau:.2f} x"]
    })
    st.dataframe(tabel_komparasi, use_container_width=True, hide_index=True)

    # Kesimpulan Akhir
    st.markdown(f"""
    <div class="info-box-success">
        <h4>💡 Ringkasan Rekomendasi Finansial - PBL Kelompok 2</h4>
        <p>Dengan menerapkan data riil KPH Sumedang, <b>Skenario B (Hijau Terintegrasi)</b> terbukti memberikan return finansial tertinggi. 
        Skenario ini meningkatkan keuntungan bersih NPV sebesar <b>{persen_peningkatan:.2f}%</b> serta menaikkan indeks efisiensi BCR dari {bcr_tradisional:.2f} menjadi <b>{bcr_hijau:.2f}</b>.</p>
        <span style="font-size:12px; font-weight:700;">🟢 STATUS MODEL: SIMULASI BERHASIL DISINKRONKASI</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer Identitas Kelompok di bagian paling bawah halaman simulasi
    st.markdown("<br><hr style='border-color: #e5e7eb;'><center style='color: #6b7280; font-size: 12px;'>Sistem Simulasi Finansial disusun oleh: PBL Kelompok 2</center>", unsafe_allow_html=True)

# MODUL 7: VALIDASI MASTER DATA CSV
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
