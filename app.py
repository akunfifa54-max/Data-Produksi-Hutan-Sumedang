import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Forest Valuation",
    page_icon="🌲",
    layout="wide"
)

# Custom CSS untuk tema sidebar dan tampilan dashboard
st.markdown("""
<style>
    .block-container { padding: 2rem 4rem; background-color: #fcfdfe; }
    h1, h2, h3, h4 { color: #1b5e20; font-family: 'Inter', sans-serif; }
    .banner {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white; padding: 30px; border-radius: 15px; margin-bottom: 25px;
    }
    .metric-card {
        background: white; border: 1px solid #e0e0e0; border-radius: 10px;
        padding: 15px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-value { font-size: 23px; font-weight: bold; color: #2e7d32; }
    .tradeoff-box {
        background-color: #fff3e0; border-left: 5px solid #ff9800;
        padding: 15px; border-radius: 5px; margin-top: 15px;
    }
    section[data-testid="stSidebar"] { background-color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA DARI REPO GITHUB
# ==========================================
def load_data(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    return pd.DataFrame()

df_rangkuman = load_data("Rangkuman.csv")
df_profil = load_data("Profil Hutan KPH Sumedang.csv")
df_komposisi = load_data("Komposisi Hasil Hutan.csv")
df_harga = load_data("Harga Getah Pinus.csv")
df_finansial = load_data("Proxy Pengelolaan Finansial.csv")
df_produksi = load_data("Produksi Hasil Hutan.csv")

# Ekstraksi Data Utama untuk Metrik
try:
    luas_hutan_val = df_rangkuman.loc[df_rangkuman['variable'] == 'forest_area_ha', 'value'].values[0]
    prod_getah_val = df_rangkuman.loc[df_rangkuman['variable'] == 'annual_resin_production_ton', 'value'].values[0]
    prod_kayu_val = df_rangkuman.loc[df_rangkuman['variable'] == 'annual_log_production_m3', 'value'].values[0]
    
    # Ambil nilai angka murni untuk perhitungan simulasi slider
    clean_prod_getah = float(str(prod_getah_val).replace(',', ''))
except:
    luas_hutan_val, prod_getah_val, prod_kayu_val = "31,850", "5,450", "24,800"
    clean_prod_getah = 5450.0

# ==========================================
# 3. SIDEBAR NAVIGATION & LOGO
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    img_logo = Image.open(logo_path)
    st.sidebar.image(img_logo, use_container_width=True)

st.sidebar.title("Eco-Forest Valuation")
st.sidebar.markdown("**Navigasi**")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    [
        "🏠 Beranda", 
        "📄 Profil Hutan", 
        "📦 Produksi Hasil Hutan", 
        "💰 Analisis Ekonomi",
        "🗂️ Master Data",
        "📊 Parameter Simulasi",
        "📉 Dashboard Summary"
    ],
    label_visibility="collapsed"
)

# ==========================================
# LOGIKA TAMPILAN MENU
# ==========================================

# MENU 1: BERANDA
if menu == "🏠 Beranda":
    st.markdown('<div class="banner"><h1>Selamat Datang di Dashboard KPH Sumedang</h1><p>Analisis Ekonomi Sumber Daya Alam & Lingkungan - PBL Kelompok 6</p></div>', unsafe_allow_html=True)
    st.info("Dashboard ini menyajikan data hasil hutan kayu dan bukan kayu (Getah Pinus) beserta valuasi ekonomi dan kelayakan finansial pengelolaan hutan di wilayah Sumedang.")
    
    st.subheader("Identitas Kelompok")
    st.markdown("""
    **Mata Kuliah:** Ekonomi Sumber Daya Alam dan Lingkungan  
    **Dosen:** Yuhka Sundaya, S.E., M.Si.  
    
    **Anggota Kelompok:**
    1. Radea Rahman Dwiyana (10090224001)
    2. Bunga Wiati Manaki (10090224026)
    3. Shidqi Alhamdani Mieftah (10090224032)
    """)

# MENU 2: PROFIL HUTAN
elif menu == "📄 Profil Hutan":
    st.header("Profil Wilayah KPH Sumedang")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df_profil.iloc[:, 1:4], use_container_width=True, hide_index=True)
    with col2:
        st.success("**Keterangan Pengelolaan:** KPH Sumedang dikelola oleh Perum Perhutani Divre Jabar Banten dengan fokus utama pada tegakan Pinus merkusii.")

# MENU 3: PRODUKSI HASIL HUTAN
elif menu == "📦 Produksi Hasil Hutan":
    st.header("Data Produksi Tahunan")
    fig_prod = px.bar(df_produksi[0:2], x='Variabel', y='Nilai', color='Variabel', 
                     labels={'Nilai':'Volume (Ton/m3)'}, title="Volume Produksi Kayu vs Getah")
    st.plotly_chart(fig_prod, use_container_width=True)
    st.dataframe(df_produksi, use_container_width=True, hide_index=True)

# MENU 4: ANALISIS EKONOMI
elif menu == "💰 Analisis Ekonomi":
    st.header("💰 Valuasi Ekonomi & Analisis Kelayakan Kelompok 6")
    
    try:
        df_finansial['Variabel'] = df_finansial['Variabel'].str.strip()
        npv = df_finansial.loc[df_finansial['Variabel'] == 'NPV pinus', 'Nilai'].values[0]
        irr = df_finansial.loc[df_finansial['Variabel'] == 'IRR pinus', 'Nilai'].values[0]
        bcr = df_finansial.loc[df_finansial['Variabel'] == 'BCR pinus', 'Nilai'].values[0]
        tev_val = df_finansial.loc[df_finansial['Variabel'] == 'Total nilai ekonomi', 'Nilai'].values[0]
        tev_formatted = f"Rp {int(float(tev_val)):,}"
    except:
        npv, irr, bcr, tev_formatted = "198,500,000", "15.8", "2.85", "Rp 66,100,000,000"

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><b>NPV Pinus</b><br><span class="metric-value">Rp {npv} / Ha</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><b>IRR Pinus</b><br><span class="metric-value">{irr}%</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><b>Benefit-Cost Ratio (BCR)</b><br><span class="metric-value">{bcr} x</span></div>', unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🌲 Total Economic Value (TEV) KPH Sumedang")
    
    col_tev1, col_tev2 = st.columns([1, 1])
    with col_tev1:
        st.metric(label="Total Agregat Nilai Ekonomi Keseluruhan / Tahun", value=tev_formatted)
        st.markdown("""
        * **Direct Use Value (Nilai Manfaat Langsung):** Disumbangkan oleh penjualan Getah Pinus (*Non-Timber Forest Products*) dan pemanfaatan kayu log tebangan terencana.
        * **Indirect Use Value (Nilai Manfaat Tidak Langsung):** Diwakili oleh nilai asimilasi karbon hutan pinus yang berfungsi sebagai pengendali emisi gas rumah kaca.
        """)
    with col_tev2:
        fig_pie = px.pie(df_komposisi, values='Persentase', names='Kategori', 
                         title="Komposisi Kontribusi Manfaat TEV",
                         color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.write("---")
    st.subheader("⚖️ Analisis Trade-Off: Produksi vs Konservasi Lingkungan")
    
    col_to1, col_to2 = st.columns(2)
    with col_to1:
        st.markdown("""
        #### 📈 Eksploitasi Sisi Ekonomi (Produksi)
        * **Tindakan:** Memaksimalkan penderapan getah pinus dan mempercepat daur tebang kayu log untuk mengejar target profit finansial perusahaan.
        * **Dampak:** Menurunkan kekuatan mekanis batang jika penderapan terlalu ekstrem.
        """)
    with col_to2:
        st.markdown("""
        #### 🌍 Retensi Sisi Ekologi (Konservasi)
        * **Tindakan:** Membiarkan pohon utuh untuk asimilasi karbon maksimal.
        * **Dampak:** Mengurangi arus kas instan (*cash flow*) dari penjualan kayu komersial.
        """)
        
    st.markdown('<div class="tradeoff-box">💡 <b>Solusi Kebijakan Sumber Daya:</b> Nilai BCR sebesar <b>' + str(bcr) + '</b> membuktikan bahwa strategi saat ini sudah tepat. KPH Sumedang berhasil menempatkan penderapan getah pinus sebagai roda utama ekonomi (70%), sehingga fungsi penyerapan karbon lingkungan tetap berjalan beriringan dengan keuntungan finansial.</div>', unsafe_allow_html=True)

# MENU 5: MASTER DATA
elif menu == "🗂️ Master Data":
    st.header("Dataset Master (Raw CSV)")
    tab1, tab2, tab3 = st.tabs(["Rangkuman Umum", "Analisis Finansial", "Data Produksi"])
    with tab1: st.dataframe(df_rangkuman, use_container_width=True)
    with tab2: st.dataframe(df_finansial, use_container_width=True)
    with tab3: st.dataframe(df_produksi, use_container_width=True)

# MENU 6: PARAMETER SIMULASI (DENGAN SLIDER FITUR GESER KELOMPOK 6)
elif menu == "📊 Parameter Simulasi":
    st.header("📊 Simulasi Interaktif Harga Komoditas Getah Pinus")
    st.write("Gunakan tombol geser di bawah ini untuk melihat simulasi dampak perubahan harga getah di pasar terhadap pendapatan bruto daerah.")

    # 1. Menambahkan Fitur Slider (Bisa digeser-geser)
    harga_slider = st.slider(
        label="Geser untuk Menyesuaikan Harga Getah Pinus (Rp per Kg):",
        min_value=5000,
        max_value=25000,
        value=11500,  # Harga awal (default)
        step=500
    )
    
    # 2. Rumus Matematika Simulasi Otomatis
    # Produksi dalam Ton diubah ke Kg dikali harga dari slider
    pendapatan_simulasi = clean_prod_getah * 1000 * harga_slider
    
    st.write("---")
    
    # Menampilkan Hasil Pergeseran secara Real-Time via Info Box & Metric
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        st.info("💡 **Hasil Simulasi Live:**")
        st.metric(label="Harga Getah Terpilih", value=f"Rp {harga_slider:,} / Kg")
        st.metric(label="Estimasi Pendapatan Bruto Getah / Tahun", value=f"Rp {int(pendapatan_simulasi):,}")
    
    with col_s2:
        # Membuat Dataframe Bayangan untuk memplot Grafik Batang secara Dinamis
        simulasi_data = pd.DataFrame({
            'Skenario': ['Batas Minimum Data', 'Hasil Geser Anda (Live)', 'Batas Maksimum Data'],
            'Nilai Pendapatan Bruto (Rp)': [40875000000, pendapatan_simulasi, 81750000000]
        })
        
        fig_sim = px.bar(
            simulasi_data, 
            x='Skenario', 
            y='Nilai Pendapatan Bruto (Rp)', 
            color='Skenario',
            color_discrete_map={'Hasil Geser Anda (Live)': '#ff9800', 'Batas Minimum Data': '#a5d6a7', 'Batas Maksimum Data': '#2e7d32'},
            title="Perbandingan Posisi Pendapatan Real-Time"
        )
        st.plotly_chart(fig_sim, use_container_width=True)

    st.write("---")
    st.markdown("#### Tabel Acuan Statis (Data Asli CSV):")
    st.table(df_harga[['Variabel', 'Nilai', 'Satuan']])

# MENU 7: DASHBOARD SUMMARY
elif menu == "📉 Dashboard Summary":
    st.header("Ringkasan Eksekutif")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Luas Hutan (Ha)", luas_hutan_val)
    col2.metric("Produksi Getah (Ton)", prod_getah_val)
    col3.metric("Produksi Kayu (m³)", prod_kayu_val)
    col4.metric("Kelayakan Proyek", "LAYAK (BCR > 1)")
    
    st.write("---")
    st.info("💡 **Kesimpulan:** Pengelolaan hutan pinus di KPH Sumedang memiliki nilai ekonomi yang tinggi dengan indikator kelayakan finansial yang positif. Komoditas Getah Pinus (HHBK) menjadi penopang utama ekonomi wilayah.")
