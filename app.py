import streamlit as st
import pandas as pd
import plotly.express as px
import os
from PIL import Image

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Babakan Siliwangi Eco-Valuation",
    page_icon="🌳",
    layout="wide"
)

# Custom CSS untuk gaya visual yang bersih dan aman dari error
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
    .metric-value { font-size: 28px; font-weight: 700; color: #2e7d32; margin-top: 5px; }
    .info-card {
        background-color: #f1f8e9; border-left: 5px solid #4caf50;
        padding: 20px; border-radius: 10px; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA DARI GITHUB CSV
# ==========================================
files = {
    "ringkasan": "df_ringkasan.csv",
    "profil": "df_profil.csv",
    "jasa_lingkungan": "df_jasa_lingkungan.csv",
    "tutupan_lahan": "df_tutupan_lahan.csv",
    "trend": "df_trend.csv"
}

def load_csv_data(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"File '{file_name}' tidak ditemukan!")
        st.stop()

df_ringkasan = load_csv_data(files["ringkasan"])
df_profil = load_csv_data(files["profil"])
df_jaling = load_csv_data(files["jasa_lingkungan"])
df_veg = load_csv_data(files["tutupan_lahan"])
df_trend = load_csv_data(files["trend"])

# Ekstraksi Variabel Kunci
try:
    luas_kawasan = df_ringkasan.loc[df_ringkasan['Variabel'] == 'Luas Kawasan', 'Nilai'].values[0]
    total_pengunjung = df_ringkasan.loc[df_ringkasan['Variabel'] == 'Jumlah Pengunjung', 'Nilai'].values[0]
    total_valuasi = df_ringkasan.loc[df_ringkasan['Variabel'] == 'Nilai Ekonomi Lingkungan', 'Nilai'].values[0]
    serapan_karbon = df_jaling.loc[df_jaling['Indikator'].str.contains('Serapan Karbon'), 'Nilai'].values[0]
except Exception as e:
    st.error("Gagal memproses kolom data CSV.")
    st.stop()

# ==========================================
# 3. SIDEBAR NAVIGATION & LOGO
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
    ["🏠 Home", "📊 Dashboard Profil", "📈 Analisis Ekonomi"],
    label_visibility="collapsed"
)

# ==========================================
# MENU 1: HOME
# ==========================================
if menu == "🏠 Home":
    st.markdown("""
    <div class="banner">
        <h1 style="color: white; margin:0; font-size: 38px;">BABAKAN SILIWANGI CITY FOREST</h1>
        <h3 style="color: #a5d6a7; margin: 5px 0 0 0; font-size: 22px; font-weight: bold;">PBL 6</h3>
        <p style="margin: 5px 0 15px 0; font-size: 16px; opacity: 0.9;">
            Valuasi Ekonomi & Monitoring Ekosistem Hutan Kota (Tahun Acuan 2025)
        </p>
        <hr style="border-color: rgba(255,255,255,0.2); margin-bottom: 15px;">
        <table style="color: white; font-size: 14px; border: none; width: 100%;">
            <tr style="background: transparent;">
                <td style="padding: 2px 0; width: 150px; font-weight: bold;">Institusi</td>
                <td style="padding: 2px 0;">: UNIVERSITAS ISLAM BANDUNG</td>
            </tr>
            <tr style="background: transparent;">
                <td style="padding: 2px 0; font-weight: bold;">Mata Kuliah</td>
                <td style="padding: 2px 0;">: Ekonomi Sumber Daya Alam dan Lingkungan</td>
            </tr>
            <tr style="background: transparent;">
                <td style="padding: 2px 0; font-weight: bold;">Dosen Pengampu</td>
                <td style="padding: 2px 0;">: Yuhka Sundaya, S.E., M.Si.</td>
            </tr>
            <tr style="background: transparent;">
                <td style="padding: 2px 0; font-weight: bold; vertical-align: top;">Nama Kelompok</td>
                <td style="padding: 2px 0;">: 
                    1. Radea Rahman Dwiyana (10090224001)<br>
                    &nbsp;&nbsp;2. Bunga Wiati Manaki (10090224026)<br>
                    &nbsp;&nbsp;3. Shidqi Alhamdani Mieftah (10090224032)
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        jenis_hutan = df_profil.loc[df_profil['Parameter'] == 'Jenis Hutan', 'Nilai'].values[0]
        status_hutan = df_profil.loc[df_profil['Parameter'] == 'Status', 'Nilai'].values[0]
        st.markdown(f"""
        <div class="info-card">
            <h4>🌿 Deskripsi Kawasan</h4>
            <p>Babakan Siliwangi (Baksil) adalah <b>{jenis_hutan}</b> di Kota Bandung dengan status <b>{status_hutan}</b>. 
            Kawasan ini berfungsi sebagai paru-paru kota sekaligus ruang terbuka hijau primer bagi masyarakat ekosistem perkotaan.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        ketinggian = df_profil.loc[df_profil['Parameter'] == 'Ketinggian', 'Nilai'].values[0]
        curah_hujan = df_profil.loc[df_profil['Parameter'] == 'Curah Hujan (mm/tahun)', 'Nilai'].values[0]
        suhu = df_profil.loc[df_profil['Parameter'] == 'Suhu Rata-rata (C)', 'Nilai'].values[0]
        vegetasi = df_profil.loc[df_profil['Parameter'] == 'Dominan Vegetasi', 'Nilai'].values[0]
        st.markdown(f"""
        <div class="info-card">
            <h4>📑 Parameter Lingkungan</h4>
            <ul>
                <li><b>Ketinggian:</b> {ketinggian} mdpl</li>
                <li><b>Curah Hujan:</b> {curah_hujan} mm/tahun</li>
                <li><b>Suhu Rata-rata:</b> {suhu}°C</li>
                <li><b>Veget
