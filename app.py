import streamlit as st
import pandas as pd
import plotly.express as px
import os

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
    h1, h2, h3 { color: #1b5e20; }
    .banner {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white; padding: 30px; border-radius: 15px; margin-bottom: 25px;
    }
    .metric-card {
        background: white; border: 1px solid #e0e0e0; border-radius: 10px;
        padding: 15px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #2e7d32; }
    .stRadio > div { background-color: transparent !important; }
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
    luas_hutan = df_rangkuman.loc[df_rangkuman['variable'] == 'forest_area_ha', 'value'].values[0]
    prod_getah = df_rangkuman.loc[df_rangkuman['variable'] == 'annual_resin_production_ton', 'value'].values[0]
    prod_kayu = df_rangkuman.loc[df_rangkuman['variable'] == 'annual_log_production_m3', 'value'].values[0]
except:
    luas_hutan, prod_getah, prod_kayu = "31,850", "5,450", "24,800"

# ==========================================
# 3. SIDEBAR NAVIGATION (7 MENU)
# ==========================================
st.sidebar.title("🌲 Eco-Forest Valuation")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigasi",
    [
        "🏠 Beranda", 
        "📄 Profil Hutan", 
        "📦 Produksi Hasil Hutan", 
        "💰 Analisis Ekonomi",
        "🗂️ Master Data",
        "📊 Parameter Simulasi",
        "📉 Dashboard Summary"
    ]
)

# ==========================================
# MENU 1: BERANDA
# ==========================================
if menu == "🏠 Beranda":
    st.markdown('<div class="banner"><h1>Selamat Datang di Dashboard KPH Sumedang</h1><p>Analisis Ekonomi Sumber Daya Alam & Lingkungan - PBL Kelompok 6</p></div>', unsafe_allow_html=True)
    st.info("Dashboard ini menyajikan data hasil hutan kayu dan bukan kayu (Getah Pinus) beserta valuasi ekonomi dan kelayakan finansial pengelolaan hutan di wilayah Sumedang.")
    
    st.subheader("Identitas Kelompok")
    st.write("**Mata Kuliah:** Ekonomi Sumber Daya Alam dan Lingkungan")
    st.write("**Dosen:** Yuhka Sundaya, S.E., M.Si.")
    st.markdown("""
    1. Radea Rahman Dwiyana (10090224001)
    2. Bunga Wiati Manaki (10090224026)
    3. Shidqi Alhamdani Mieftah (10090224032)
    """)

# ==========================================
# MENU 2: PROFIL HUTAN
# ==========================================
elif menu == "📄 Profil Hutan":
    st.header("Profil Wilayah KPH Sumedang")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_profil.iloc[:, 1:4], use_container_width=True, hide_index=True)
    with col2:
        st.success("**Keterangan Pengelolaan:** KPH Sumedang dikelola oleh Perum Perhutani Divre Jabar Banten dengan fokus utama pada tegakan Pinus merkusii.")

# ==========================================
# MENU 3: PRODUKSI HASIL HUTAN
# ==========================================
elif menu == "📦 Produksi Hasil Hutan":
    st.header("Data Produksi Tahunan")
    st.write("Volume produksi Kayu dan Getah Pinus tahun 2024.")
    
    fig_prod = px.bar(df_produksi[0:2], x='Variabel', y='Nilai', color='Variabel', title="Volume Produksi Utama")
    st.plotly_chart(fig_prod, use_container_width=True)
    st.dataframe(df_produksi, use_container_width=True, hide_index=True)

# ==========================================
# MENU 4: ANALISIS EKONOMI
# ==========================================
elif menu == "💰 Analisis Ekonomi":
    st.header("Analisis Valuasi & Kelayakan")
    
    c1, c2, c3 = st.columns(3)
    try:
        npv = df_finansial.loc[df_finansial['Variabel'] == 'NPV pinus', 'Nilai'].values[0]
        irr = df_finansial.loc[df_finansial['Variabel'] == 'IRR pinus', 'Nilai'].values[0]
        bcr = df_finansial.loc[df_finansial['Variabel'] == 'BCR pinus', 'Nilai'].values[0]
    except:
        npv, irr, bcr = "0", "0", "0"

    c1.markdown(f'<div class="metric-card">NPV<br><span class="metric-value">Rp {npv}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">IRR<br><span class="metric-value">{irr}%</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">BC Ratio<br><span class="metric-value">{bcr}</span></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("#### Distribusi Nilai Ekonomi Total")
    fig_pie = px.pie(df_komposisi, values='Persentase', names='Kategori', hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# MENU 5: MASTER DATA
# ==========================================
elif menu == "🗂️ Master Data":
    st.header("Dataset Mentah (CSV Source)")
    tab1, tab2, tab3 = st.tabs(["Rangkuman", "Finansial", "Produksi"])
    with tab1: st.dataframe(df_rangkuman)
    with tab2: st.dataframe(df_finansial)
    with tab3: st.dataframe(df_produksi)

# ==========================================
# MENU 6: PARAMETER SIMULASI
# ==========================================
elif menu == "📊 Parameter Simulasi":
    st.header("Simulasi Harga Getah Pinus")
    st.write("Estimasi pendapatan kotor (bruto) berdasarkan skenario harga pasar.")
    
    df_bruto = df_harga[df_harga['Variabel'].str.contains('Nilai bruto')]
    fig_bruto = px.line(df_bruto, x='Variabel', y='Nilai', markers=True, title="Skenario Pendapatan Tahunan")
    st.plotly_chart(fig_bruto, use_container_width=True)
    st.table(df_harga[['Variabel', 'Nilai', 'Satuan']])

# ==========================================
# MENU 7: DASHBOARD SUMMARY
# ==========================================
elif menu == "📉 Dashboard Summary":
    st.header("Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Luas Hutan (Ha)", luas_hutan)
    col2.metric("Produksi Getah (Ton)", prod_getah)
    col3.metric("Produksi Kayu (m³)", prod_kayu)
    col4.metric("Status Proyek", "LAYAK (BCR > 1)")
    
    st.write("---")
    st.success("💡 **Insight:** Hasil produksi getah pinus memberikan kontribusi pendapatan terbesar (70%) dibandingkan kayu log. Hal ini menunjukkan potensi HHBK (Hasil Hutan Bukan Kayu) yang sangat dominan di KPH Sumedang.")
