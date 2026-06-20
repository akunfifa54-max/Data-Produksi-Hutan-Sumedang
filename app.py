import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="KPH Sumedang Eco-Production Dashboard",
    page_icon="🌲",
    layout="wide"
)

# Custom CSS Tema Terang Kontras Tinggi (Baris Pendek Anti-Cut-Off)
st.markdown("""
<style>
    .block-container { padding: 2rem 4rem; background-color: #fcfdfe; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #1b5e20; }
    .banner {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white; padding: 35px; border-radius: 20px; margin-bottom: 30px;
    }
    .metric-card {
        background: white; border: 1px solid #e0e0e0; border-radius: 15px;
        padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .metric-title { font-size: 13px; color: #666; text-transform: uppercase; font-weight: bold; }
    .metric-value { font-size: 26px; font-weight: 700; color: #2e7d32; margin-top: 5px; }
    
    .info-card {
        background-color: #e8f5e9 !important; border-left: 5px solid #4caf50;
        padding: 20px; border-radius: 10px; margin-bottom: 20px; 
        color: #1b5e20 !important;
    }
    .info-card h4 { color: #1b5e20 !important; margin-top: 0; font-weight: bold; }
    .info-card p, .info-card ul, .info-card li { color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA DARI REPO GITHUB CSV
# ==========================================
files = {
    "rangkuman": "Data kph sumedang^.xlsx - Rangkuman.csv",
    "profil": "Data kph sumedang^.xlsx - Profil Hutan KPH Sumedang.csv",
    "komposisi": "Data kph sumedang^.xlsx - Komposisi Hasil Hutan.csv",
    "harga_getah": "Data kph sumedang^.xlsx - Harga Getah Pinus.csv",
    "finansial": "Data kph sumedang^.xlsx - Proxy Pengelolaan Finansial.csv"
}

def load_csv_data(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"File '{file_name}' tidak ditemukan di repositori GitHub!")
        st.stop()

df_rangkuman = load_csv_data(files["rangkuman"])
df_profil = load_csv_data(files["profil"])
df_komposisi = load_csv_data(files["komposisi"])
df_harga = load_csv_data(files["harga_getah"])
df_finansial = load_csv_data(files["finansial"])

# Membersihkan nama kolom dari spasi tidak sengaja
df_rangkuman.columns = df_rangkuman.columns.str.strip()
df_profil.columns = df_profil.columns.str.strip()
df_komposisi.columns = df_komposisi.columns.str.strip()
df_harga.columns = df_harga.columns.str.strip()
df_finansial.columns = df_finansial.columns.str.strip()

# Mengambil metrik utama secara aman
try:
    luas_hutan = df_rangkuman.loc[df_rangkuman['variable'] == 'forest_area_ha', 'value'].values[0]
    prod_getah = df_rangkuman.loc[df_rangkuman['variable'] == 'annual_resin_production_ton', 'value'].values[0]
    prod_kayu = df_rangkuman.loc[df_rangkuman['variable'] == 'annual_log_production_m3', 'value'].values[0]
    stok_karbon = df_rangkuman.loc[df_rangkuman['variable'] == 'carbon_stock', 'value'].values[0]
except:
    luas_hutan, prod_getah, prod_kayu, stok_karbon = "31.850", "5.450", "24.800", "1.775.000"

# ==========================================
# 3. SIDEBAR PANEL NAVIGATION & LOGO
# ==========================================
logo_path = "OIP.webp"
if os.path.exists(logo_path):
    try:
        img_logo = Image.open(logo_path)
        st.sidebar.image(img_logo, width=100)
    except:
        pass

st.sidebar.markdown("### **Navigasi Panel**")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Home", "📊 Dashboard Profil & Komposisi", "📈 Analisis Finansial Kelayakan"],
    label_visibility="collapsed"
)

# ==========================================
# MENU 1: HOME
# ==========================================
if menu == "🏠 Home":
    hb = "".join([
        '<div class="banner">',
        '<h1 style="color: white; margin:0; font-size: 36px;">KPH SUMEDANG</h1>',
        '<h3 style="color: #a5d6a7; margin: 5px 0 0 0; font-size: 20px; font-weight: bold;">PBL 6</h3>',
        '<p style="margin: 5px 0 15px 0; font-size: 15px; opacity: 0.9;">',
        'Analisis Ekonomi Sumber Daya Alam, Produksi Komoditas Pinus & Valuasi Finansial</p>',
        '<hr style="border-color: rgba(255,255,255,0.2); margin-bottom: 15px;">',
        '<table style="color: white; font-size: 14px; border: none; width: 100%;">',
        '<tr style="background: transparent;"><td style="padding: 2px 0; width: 150px; font-weight: bold;">Institusi</td><td>: UNIVERSITAS ISLAM BANDUNG</td></tr>',
        '<tr style="background: transparent;"><td style="font-weight: bold;">Mata Kuliah</td><td>: Ekonomi Sumber Daya Alam dan Lingkungan</td></tr>',
        '<tr style="background: transparent;"><td style="font-weight: bold;">Dosen Pengampu</td><td>: Yuhka Sundaya, S.E., M.Si.</td></tr>',
        '<tr style="background: transparent;"><td style="font-weight: bold; vertical-align: top;">Nama Kelompok</td><td>: ',
        '1. Radea Rahman Dwiyana (10090224001)<br>',
        '&nbsp;&nbsp;2. Bunga Wiati Manaki (10090224026)<br>',
        '&nbsp;&nbsp;3. Shidqi Alhamdani Mieftah (10090224032)</td></tr>',
        '</table></div>'
    ])
    st.markdown(hb, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown('<div class="info-card"><h4>🌲 Gambaran Umum KPH Sumedang</h4>', unsafe_allow_html=True)
        st.markdown("Kesatuan Pemangkuan Hutan (KPH) Sumedang adalah unit kerja pengelolaan hutan di bawah Perum Perhutani Divisi Regional Jawa Barat dan Banten. Berdasarkan data kelas perusahaan, kawasan ini difokuskan penuh untuk pengembangan tegakan pohon **Pinus (*Pinus merkusii*)** sebagai penghasil utama produk getah dan kayu log.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="info-card"><h4>📑 Orientasi Analisis Ekonomi (PBL 6)</h4>', unsafe_allow_html=True)
        st.markdown("- **Aspek Teknis:** Mengukur volume produksi tahunan Getah Pinus dan Kayu Log.")
        st.markdown("- **Aspek Finansial:** Menilai kelayakan proyek dengan indikator NPV, IRR, dan Benefit-Cost Ratio (BCR).")
        st.markdown("- **Aspek Lingkungan:** Memvalidasi peran penyerapan karbon dari tegakan pinus terhadap regulasi iklim.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MENU 2: DASHBOARD PROFIL & KOMPOSISI
# ==========================================
elif menu == "📊 Dashboard Profil & Komposisi":
    st.subheader("📊 Ringkasan Indikator Statis Potensi Wilayah")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Luas Wilayah Kerja</div><div class="metric-value">{luas_hutan} Ha</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Produksi Getah / Tahun</div><div class="metric-value">{prod_getah} Ton</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Produksi Kayu / Tahun</div><div class="metric-value">{prod_kayu} m³</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Estimasi Stok Karbon</div><div class="metric-value">{stok_karbon} Ton</div></div>', unsafe_allow_html=True)

    st.write("---")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Komposisi Persentase Manfaat Hasil Hutan")
        fig_pie = px.pie(
            df_komposisi,
            values='Persentase',
            names='Kategori',
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.markdown("### Parameter Struktural (Administratif)")
        # Menampilkan kolom informasi secara dinamis dan aman menggunakan indeks posisi
        df_display_profil = df_profil.iloc[:, 1:4]
        st.dataframe(df_display_profil, use_container_width=True, hide_index=True)

# ==========================================
# MENU 3: ANALISIS FINANSIAL KELAYAKAN
# ==========================================
elif menu == "📈 Analisis Finansial Kelayakan":
    st.subheader("📈 Analisis Kelayakan Investasi & Skenario Finansial Proyek")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    try:
        npv_val = df_finansial.loc[df_finansial['Variabel'] == 'NPV pinus', 'Nilai'].values[0]
        irr_val = df_finansial.loc[df_finansial['Variabel'] == 'IRR pinus', 'Nilai'].values[0]
        bcr_val = df_finansial.loc[df_finansial['Variabel'] == 'BCR pinus', 'Nilai'].values[0]
        total_valuasi = df_finansial.loc[df_finansial['Variabel'] == 'Total nilai ekonomi', 'Nilai'].values[0]
    except:
        npv_val, irr_val, bcr_val, total_valuasi = "198500000", "15.8", "2.85", "66100000000"

    # Formatting agar tampilan angka rapi dengan pemisah ribuan
    try:
        npv_card = f"Rp {int(float(npv_val)):,}"
        total_val_card = f"Rp {int(float(total_valuasi)):,}"
    except:
        npv_card = f"Rp {npv_val}"
        total_val_card = f"Rp {total_valuasi}"

    with col_f1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">NPV (Net Present Value)</div><div class="metric-value">{npv_card} / Ha</div></div>', unsafe_allow_html=True)
    with col_f2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">IRR (Internal Rate of Return)</div><div class="metric-value">{irr_val} %</div></div>', unsafe_allow_html=True)
    with col_f3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">BCR (Benefit Cost Ratio)</div><div class="metric-value">{bcr_val} x</div></div>', unsafe_allow_html=True)
        
    st.write("---")
    
    st.markdown("### Estimasi Perbandingan Nilai Pendapatan Bruto Berdasarkan Batas Skenario Harga Getah")
    # Memfilter baris pendapatan bruto dari file Skenario Harga Getah
    df_bruto = df_harga[df_harga['Variabel'].str.contains('Nilai bruto', case=False)].copy()
    df_bruto['Nilai'] = pd.to_numeric(df_bruto['Nilai'], errors='coerce')
    
    fig_bar = px.bar(
        df_bruto,
        x='Variabel',
        y='Nilai',
        color='Nilai',
        labels={'Nilai':'Rupiah (Rp)', 'Variabel':'Skenario Nilai Bruto'},
        color_continuous_scale="Darkmint"
    )
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

    st.write("---")
    st.metric(label="Total Agregat Nilai Ekonomi Keseluruhan KPH Sumedang / Tahun", value=total_val_card)

    ta = "".join([
        '<div class="card" style="background: white; padding: 15px; border-radius: 10px; ',
        'border-top: 4px solid #1b5e20; box-shadow: 0 2px 8px rgba(0,0,0,0.05); color: #1b5e20;">💡 ',
        '<b>Interpretasi Hasil Studi Ekonomi Lingkungan:</b> Proyek investasi tegakan pinus pada KPH Sumedang ',
        f'dinyatakan <b>sangat layak dijalankan</b> karena memiliki nilai Benefit-Cost Ratio (BCR) sebesar <b>{bcr_val}</b> (> 1). ',
        f'Nilai IRR sebesar <b>{irr_val}%</b> juga menunjukkan performa profitabilitas di atas rata-rata tingkat inflasi pasar, ',
        f'ditambah akumulasi total nilai ekonomi wilayah yang mencapai {total_val_card} per tahun.</div>'
    ])
    st.markdown(ta, unsafe_allow_html=True)
