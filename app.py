import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

# ==========================================
# 1. KONFIGURASI PREMIUM & UI THEME (HIJAU HUTAN)
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Forest Valuation",
    page_icon="🌲",
    layout="wide"
)

# Tema Eksklusif: Hijau Hutan Modern, Soft Shadow, & Interaksi Dinamis
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }
    .block-container { padding: 2.5rem 4.5rem; background-color: #fcfdfe; }
    h1, h2, h3, h4 { color: #1b5e20; font-weight: 700; letter-spacing: -0.5px; }
    
    /* Banner Jumbotron */
    .banner {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: white; padding: 40px; border-radius: 16px; margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(27, 94, 32, 0.12);
    }
    
    /* Kartu Metrik Eksklusif Soft Shadow */
    .metric-card {
        background: #ffffff; border: 1px solid #f1f5f9; border-radius: 14px;
        padding: 24px 20px; text-align: center; 
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.01);
        transition: all 0.3s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #2e7d32;
        box-shadow: 0 12px 24px rgba(46, 125, 50, 0.08);
    }
    .metric-title { font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #1b5e20; margin-top: 10px; }
    
    /* Box Kajian Akademik */
    .tradeoff-box {
        background-color: #fffbeb; border-left: 5px solid #d97706;
        padding: 20px; border-radius: 8px; margin-top: 20px; color: #78350f;
    }
    .solution-box {
        background-color: #f0fdf4; border-left: 5px solid #16a34a;
        padding: 20px; border-radius: 8px; margin-top: 20px; color: #14532d;
    }
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE (ANTI-CRASH)
# ==========================================
def smart_load(file_name, default_data):
    if os.path.exists(file_name):
        try:
            df = pd.read_csv(file_name)
            df.columns = df.columns.str.strip()
            return df
        except:
            return pd.DataFrame(default_data)
    return pd.DataFrame(default_data)

df_rangkuman = smart_load("Rangkuman.csv", {
    'variable': ['forest_area_ha', 'annual_resin_production_ton', 'annual_log_production_m3', 'carbon_stock'],
    'value': [31850, 5450, 24800, 1775000]
})
df_profil = smart_load("Profil Hutan KPH Sumedang.csv", {
    'No': [1, 2, 3],
    'Kecamatan': ['Ujungjaya', 'Tomo', 'Jatigede'],
    'Luas (Ha)': [10500, 11200, 10150]
})
df_komposisi = smart_load("Komposisi Hasil Hutan.csv", {
    'Kategori': ['Getah Pinus (HHBK)', 'Kayu Log Komersial', 'Valuasi Karbon'],
    'Persentase': [70, 20, 10]
})
df_harga = smart_load("Harga Getah Pinus.csv", {
    'Variabel': ['Batas Minimum', 'Harga Rata-Rata', 'Batas Maksimum'],
    'Nilai': [7500, 11500, 15000],
    'Satuan': ['Rp/Kg', 'Rp/Kg', 'Rp/Kg']
})
df_finansial = smart_load("Proxy Pengelolaan Finansial.csv", {
    'Variabel': ['NPV pinus', 'IRR pinus', 'BCR pinus', 'Total nilai ekonomi'],
    'Nilai': [198500000, 15.8, 2.85, 66100000000]
})
df_produksi = smart_load("Produksi Hasil Hutan.csv", {
    'Variabel': ['Getah Pinus', 'Kayu Log'],
    'Nilai': [5450, 24800]
})

prod_getah = 5450
prod_kayu = 24800

# ==========================================
# 3. BRANDING LOGO & NAVIGASI GESER UTAMA
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    st.sidebar.image(Image.open(logo_path), use_container_width=True)

st.sidebar.markdown("<h3 style='text-align: center; margin-top:0; font-size:18px; color:#1b5e20;'>PBL KELOMPOK 6</h3>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("📁 **Pilih Menu Analisis:**")
menu = st.sidebar.selectbox(
    "Navigasi Halaman:",
    [
        "🏠 Beranda Utama", 
        "📄 Profil, Vegetasi & Ekosistem", 
        "📦 Matriks Produksi Hutan", 
        "💰 Valuasi TEV & Kelayakan",
        "⚖️ Parameter Kebijakan Trade-Off",
        "📊 Simulator & Slider Dinamis",
        "📂 Transparansi Data CSV"
    ]
)

# ==========================================
# MODUL 1: BERANDA UTAMA
# ==========================================
if menu == "🏠 Beranda Utama":
    st.markdown("""
    <div class="banner">
        <h1 style="color: white; margin: 0; font-size: 36px; font-weight:700;">KPH SUMEDANG ECO-PRODUCTION</h1>
        <p style="margin: 8px 0 0 0; font-size: 16px; opacity: 0.9;">
            Platform Analisis Valuasi Ekonomi Lingkungan, Teknis Produksi Pinus & Kelayakan Finansial - PBL Kelompok 6
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.markdown("### 📑 Deskripsi Proyek Singkat")
        st.write("""
        Dashboard ini dirancang untuk memenuhi studi riset Kelompok 6 mengenai analisis tata kelola ekonomi lingkungan di 
        **KPH Sumedang**. Fokus riset difokuskan pada optimalisasi produk **Pinus (*Pinus merkusii*)**.
        """)
        
        st.markdown("### 👥 Tim Peneliti Akademik:")
        st.markdown("""
        * **Mata Kuliah:** Ekonomi Sumber Daya Alam dan Lingkungan  
        * **Institusi:** Universitas Islam Bandung (UNISBA)  
        * **Dosen Pembimbing:** Yuhka Sundaya, S.E., M.Si.  
        
        **Anggota Kelompok 6:**
        1. 🧑‍💻 **Radea Rahman Dwiyana** (10090224001)
        2. 👩‍💻 **Bunga Wiati Manaki** (10090224026)
        3. 🧑‍💻 **Shidqi Alhamdani Mieftah** (10090224032)
        """)
    with col_side:
        st.markdown("<div class='metric-card' style='background-color:#f8fafc; border-top: 4px solid #1b5e20;'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Sasaran Studi Kritis")
        st.markdown("""
        * **Valuasi Akurat:** Menghitung Total Nilai Ekonomi kawasan.
        * **Uji Sensitivitas:** Menilai ketahanan finansial terhadap pasar.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODUL 2: PROFIL, VEGETASI & EKOSISTEM (UPGRADED PERFECT)
# ==========================================
elif menu == "📄 Profil, Vegetasi & Ekosistem":
    st.header("📄 Karakteristik Biofisik, Status Hukum & Kekayaan Hayati")
    st.write("Analisis spasial wilayah, status fungsi kawasan hutan, serta keanekaragaman flora dan fauna di KPH Sumedang.")
    
    # Menampilkan Tab Internal yang Bisa Digeser untuk Memisahkan Data Teknis & Penjelasan Naratif
    tab_geo, tab_status, tab_biodiversitas = st.tabs([
        "🗺️ Distribusi Geografis", 
        "⚖️ Status Fungsi Kawasan Hutan", 
        "🦅 Kekayaan Flora & Fauna (Biodiversitas)"
    ])
    
    with tab_geo:
        col_tab, col_box = st.columns([4, 3])
        with col_tab:
            st.markdown("##### Luas Wilayah Administrasi Per Kecamatan di KPH Sumedang")
            st.dataframe(df_profil, use_container_width=True, hide_index=True)
        with col_box:
            st.markdown("<div class='solution-box' style='margin-top:0;'>", unsafe_allow_html=True)
            st.markdown("##### 📍 Kondisi Geografis Lokasi")
            st.write("""
            Secara geografis, wilayah **KPH Sumedang** membentang di Kabupaten Sumedang, Jawa Barat, dengan lanskap yang didominasi oleh topografi perbukitan bergelombang hingga pegunungan curam. 
            
            Kondisi tanah vulkanik yang subur didukung oleh curah hujan tropis yang tinggi menjadikan kawasan ini sebagai habitat yang sangat ideal bagi pertumbuhan tegakan vegetasi komoditas berkayu, khususnya pohon **Pinus (*Pinus merkusii*)**.
            """)
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_status:
        st.markdown("### ⚖️ Klasifikasi Status Hukum Kawasan Hutan")
        st.write("Apakah wilayah KPH Sumedang merupakan Hutan Lindung, Hutan Raya, atau Hutan Produksi?")
        
        st.markdown("""
        Berdasarkan tata guna hutan kesepakatan dan regulasi Perum Perhutani Divisi Regional Jawa Barat dan Banten, status hukum wilayah kerja KPH Sumedang secara mayoritas diklasifikasikan sebagai **HUTAN PRODUKSI (HP)**, dengan beberapa zonasi khusus sebagai **Hutan Lindung (HL)** untuk menjaga hulu daerah aliran sungai (DAS). 
        
        Kawasan ini **bukan merupakan Hutan Raya (Tahura)** yang peruntukannya murni untuk konservasi koleksi tumbuhan baku. 
        """)
        
        st.markdown("<div class='tradeoff-box' style='background-color: #f0fdf4; border-left-color: #16a34a; color: #14532d;'>", unsafe_allow_html=True)
        st.markdown("##### 🔗 Korelasi Status Hutan dengan Produksi Getah & Pohon Pinus")
        st.write("""
        Karena status hukumnya sebagai **Hutan Produksi**, KPH Sumedang memiliki legalitas resmi untuk memanen komoditas kayu log komersial. Namun, guna meminimalkan kerusakan lingkungan akibat penebangan pohon secara masif (*deforestasi*), pengelola menerapkan strategi **Hasil Hutan Bukan Kayu (HHBK)** melalui penderapan **Getah Pinus**.
        
        Strategi ini sangat brilian secara ekonomi sumber daya alam: **Pohon pinus tetap dibiarkan hidup tumbuh berdiri kokoh menjaga fungsi ekologis (menyerap karbon dan mencegah longsor), namun di saat bersamaan tetap mampu memproduksi getah secara periodik untuk mendatangkan profit finansial harian bagi perusahaan dan menyejahterakan masyarakat penyadap lokal.**
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_biodiversitas:
        st.markdown("### 🦅 Profil Ekosistem & Kekayaan Biodiversitas Hayati")
        st.write("Meskipun difungsikan sebagai kawasan produksi intensif Pinus merkusii, KPH Sumedang tetap menyimpan kekayaan flora dan fauna yang hidup berdampingan di dalam ekosistem hutan.")
        
        col_flora, col_fauna = st.columns(2)
        
        with col_flora:
            st.markdown("""
            <div class='metric-card' style='text-align: left; border-top: 4px solid #1b5e20;'>
                <h4>🌲 Kekayaan Flora (Vegetasi)</h4>
                <ul>
                    <li><b>Pinus merkusii (Tegakan Utama):</b> Tanaman pokok penghasil getah komersial sekaligus penopang biomassa karbon terbesar di kawasan ini.</li>
                    <li><b>Vegetasi Pengaya & Monokultur:</b> Di sela-sela tegakan pinus, terdapat sebaran tanaman Kaliandra, Mahoni, dan Akasia yang berfungsi sebagai tanaman sekat bakar serta menjaga kesuburan unsur hara tanah bawah.</li>
                    <li><b>Plantae Bawah:</b> Paku-pakuan, semak belukar, dan tanaman pakan alami yang menjaga kelembaban mikro tanah hutan.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_fauna:
            st.markdown("""
            <div class='metric-card' style='text-align: left; border-top: 4px solid #ff9800;'>
                <h4>🦅 Kekayaan Fauna (Satwa Liar)</h4>
                <ul>
                    <li><b>Avifauna (Burung):</b> Menjadi rumah bagi burung Elang Jawa (Spizaetus bartelsi) yang sesekali singgah di area hulu lindung, burung Kutilang, dan Cerocokan yang berperan sebagai penyerak biji alami.</li>
                    <li><b>Mamalia:</b> Terdapat populasi Babi Hutan (Sus scrofa), Tupai, dan beberapa jenis primata lokal seperti Monyet Ekor Panjang (Macaca fascicularis) yang mendiami area batas hutan konservasi.</li>
                    <li><b>Reptilia & Insekta:</b> Berbagai jenis ular sanca, kadal hutan, serta koloni lebah madu liar yang memanfaatkan bunga dari tanaman pengaya (kaliandra) di sekitar tegakan pohon pinus.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# MODUL 3: MATRIKS PRODUKSI HUTAN
# ==========================================
elif menu == "📦 Matriks Produksi Hutan":
    st.header("📦 Neraca Aliran Produksi Biomassa")
    
    fig_prod = px.bar(
        df_produksi, x='Variabel', y='Nilai', color='Variabel', text_auto='.2s',
        color_discrete_sequence=['#2e7d32', '#1565c0'],
        title="Kuantitas Volume Panen Komoditas Pinus Tahun Berjalan"
    )
    fig_prod.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_prod, use_container_width=True)

# ==========================================
# MODUL 4: ANALISIS VALUASI TEV
# ==========================================
elif menu == "💰 Valuasi TEV & Kelayakan":
    st.header("💰 Total Economic Value (TEV) & Indikator Kelayakan Finansial")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown('<div class="metric-card"><div class="metric-title">Net Present Value (NPV)</div><div class="metric-value">Rp 198,500,000</div></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div class="metric-card"><div class="metric-title">Internal Rate of Return (IRR)</div><div class="metric-value">15.80 %</div></div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown('<div class="metric-card"><div class="metric-title">Benefit-Cost Ratio (BCR)</div><div class="metric-value">2.85 x</div></div>', unsafe_allow_html=True)
        
    st.write("---")
    
    col_chart, col_tex = st.columns([1, 1])
    with col_chart:
        fig_pie = px.pie(
            df_komposisi, values='Persentase', names='Kategori', hole=0.4,
            color_discrete_sequence=['#1b5e20', '#2e7d32', '#81c784']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_tex:
        st.markdown("##### 📊 Valuasi Ekonomi Makro Agregat")
        st.metric(label="Total Nilai Ekonomi Wilayah KPH / Tahun", value="Rp 66,100,000,000")

# ==========================================
# MODUL 5: PARAMETER KEBIJAKAN TRADE-OFF
# ==========================================
elif menu == "⚖️ Parameter Kebijakan Trade-Off":
    st.header("⚖️ Analisis Batas Trade-Off")
    
    c_l, c_r = st.columns(2)
    with c_l:
        st.markdown("""
        <div class="tradeoff-box">
            <h4>📈 Sisi Ekonomi (Produksi)</h4>
            <p>Melakukan penyadapan getah secara masif untuk profit instan.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_r:
        st.markdown("""
        <div class="tradeoff-box" style="border-left-color: #0284c7; background-color: #f0f9ff; color: #0c4a6e;">
            <h4>🌍 Sisi Ekologi (Konservasi)</h4>
            <p>Menjaga pohon tetap utuh untuk asimilasi zat karbon.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# MODUL 6: SIMULATOR & SLIDER DINAMIS
# ==========================================
elif menu == "📊 Simulator & Slider Dinamis":
    st.header("📊 Simulator Interaktif Kelayakan Investasi")
    st.write("Silakan geser tombol di bawah ini untuk melihat dampak perubahan harga getah secara real-time.")

    harga_geser = st.slider(
        "Geser untuk Menyesuaikan Harga Pasar Getah Pinus (Rp / Kg):",
        min_value=5000,
        max_value=25000,
        value=11500,
        step=500
    )
    
    revenue_getah_live = prod_getah * 1000 * harga_geser
    revenue_kayu_fixed = prod_kayu * 620000 
    total_rev_live = revenue_getah_live + revenue_kayu_fixed
    indeks_perubahan = harga_geser / 11500
    npv_live = 198500000 * indeks_perubahan
    bcr_live = 2.85 * indeks_perubahan

    st.write("---")
    
    v1, v2, v3 = st.columns(3)
    with v1:
        st.metric(label="Proyeksi NPV Live", value=f"Rp {int(npv_live):,}")
    with v2:
        st.metric(label="Proyeksi BC Ratio Live", value=f"{bcr_live:.2f} x")
    with v3:
        st.metric(label="Total Estimasi Omset Bersama", value=f"Rp {int(total_rev_live):,}")

    st.write("---")
    chart_data = pd.DataFrame({
        'Komoditas Pendapatan': ['Getah Pinus (Live Bergeser)', 'Kayu Log (Statis)'],
        'Estimasi Nilai Bruto (Rp)': [revenue_getah_live, revenue_kayu_fixed]
    })
    fig_live_bar = px.bar(chart_data, x='Komoditas Pendapatan', y='Estimasi Nilai Bruto (Rp)', color='Komoditas Pendapatan', text_auto='.3s', color_discrete_sequence=['#ff9800', '#1b5e20'])
    fig_live_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_live_bar, use_container_width=True)

# ==========================================
# MODUL 7: TRANSPARANSI DATA CSV
# ==========================================
elif menu == "📂 Transparansi Data CSV":
    st.header("📂 Transparansi Dataset Sumber (Audit Mode)")
    st.write("Di bawah ini adalah menu sub-tabel yang bisa Anda klik dan geser untuk melihat data mentah asli:")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Rangkuman Indikator", "🗺️ Profil Spasial", "🍰 Struktur TEV", "💰 Skenario Harga"])
    
    with tab1:
        st.dataframe(df_rangkuman, use_container_width=True)
    with tab2:
        st.dataframe(df_profil, use_container_width=True)
    with tab3:
        st.dataframe(df_komposisi, use_container_width=True)
    with tab4:
        st.dataframe(df_harga, use_container_width=True)
