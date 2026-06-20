import streamlit as st
import pandas as pd
import plotly.express as px
import os

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
        st.error(f"File data '{file_name}' tidak ditemukan di GitHub!")
        st.stop()

df_ringkasan = load_csv_data(files["ringkasan"])
df_profil = load_csv_data(files["profil"])
df_jaling = load_csv_data(files["jasa_lingkungan"])
df_veg = load_csv_data(files["tutupan_lahan"])
df_trend = load_csv_data(files["trend"])

# Ekstraksi Variabel Kunci secara Dinamis dari CSV
try:
    luas_kawasan = df_ringkasan.loc[df_ringkasan['Variabel'] == 'Luas Kawasan', 'Nilai'].values[0]
    total_pengunjung = df_ringkasan.loc[df_ringkasan['Variabel'] == 'Jumlah Pengunjung', 'Nilai'].values[0]
    total_valuasi = df_ringkasan.loc[df_ringkasan['Variabel'] == 'Nilai Ekonomi Lingkungan', 'Nilai'].values[0]
    serapan_karbon = df_jaling.loc[df_jaling['Indikator'].str.contains('Serapan Karbon'), 'Nilai'].values[0]
except Exception as e:
    st.error("Gagal memproses kolom data CSV. Periksa isi file Anda.")
    st.stop()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616561.png", width=80)
st.sidebar.markdown("### **Navigasi Panel**")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Home", "📊 Dashboard Profil", "📈 Analisis Ekonomi"],
    label_visibility="collapsed"
)

# ==========================================
# MENU 1: HOME (Judul & Identitas)
# ==========================================
if menu == "🏠 Home":
    st.markdown("""
    <div class="banner">
        <h1 style="color: white; margin:0; font-size: 38px;">BABAKAN SILIWANGI CITY FOREST</h1>
        <p style="margin: 5px 0 15px 0; font-size: 18px; opacity: 0.9;">
            Valuasi Ekonomi & Monitoring Ekosistem Hutan Kota (Tahun Acuan 2025)
        </p>
        <hr style="border-color: rgba(255,255,255,0.2);">
        <p style="margin:0; font-size: 15px;"><strong>UNIVERSITAS ISLAM BANDUNG</strong></p>
        <p style="margin:0; font-size: 14px;">Ekonomi Sumber Daya Alam dan Lingkungan</p>
        <br>
        <p style="margin:0; font-size: 13px; font-weight: bold;">KELOMPOK 2:</p>
        <p style="margin:0; font-size: 13px;">1. Dadang (Ketua) | 2. Anggota 2 | 3. Anggota 3 | 4. Anggota 4</p>
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
                <li><b>Vegetasi Dominan:</b> {vegetasi}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# MENU 2: DASHBOARD PROFIL
# ==========================================
elif menu == "📊 Dashboard Profil":
    st.subheader("📊 Ringkasan Indikator Babakan Siliwangi")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Luas Wilayah</div><div class="metric-value">{float(luas_kawasan)} Ha</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Pengunjung/Thn</div><div class="metric-value">{int(total_pengunjung):,}</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Serapan Karbon</div><div class="metric-value">{int(float(serapan_karbon))} Ton</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Valuasi Total</div><div class="metric-value">Rp {float(total_valuasi):,.0f}</div></div>""", unsafe_allow_html=True)

    st.write("---")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Komposisi Tata Guna Lahan")
        fig_pie = px.pie(
            df_veg, 
            values='Persentase', 
            names='Kategori', 
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.markdown("### Detail Parameter Vegetasi")
        st.table(df_veg)

# ==========================================
# MENU 3: ANALISIS EKONOMI
# ==========================================
elif menu == "📈 Analisis Ekonomi":
    st.subheader("📈 Tren Nilai Ekonomi vs Biaya Pengelolaan")
    
    # Grafik 1: Perbandingan Finansial (Line Chart)
    fig_eco = px.line(
        df_trend, 
        x="Tahun", 
        y=["Nilai Ekonomi (Rp)", "Biaya Pengelolaan (Rp)"],
        title="Perbandingan Nilai Jasa Lingkungan vs Biaya Operasional",
        markers=True, 
        color_discrete_sequence=["#2e7d32", "#e53935"]
    )
    fig_eco.update_layout(yaxis_title="Rupiah (Rp)", hovermode="x unified")
    st.plotly_chart(fig_eco, use_container_width=True)
    
    st.write("---")
    
    # Grafik 2: Tren Pengunjung (Bar Chart)
    fig_visitor = px.bar(
        df_trend, 
        x="Tahun", 
        y="Pengunjung", 
        title="Tren Pertumbuhan Pengunjung Tahunan",
        color="Pengunjung", 
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig_visitor, use_container_width=True)

    st.markdown("""
    <div class="card" style="background: white; padding: 15px; border-radius: 10px; border-top: 4px solid #1b5e20; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        💡 <b>Analisis:</b> Berdasarkan data historis hingga tahun target, Nilai Ekonomi Lingkungan jauh melampaui 
        Biaya Pengelolaan operasional kawasan. Hal ini menunjukkan efisiensi ekosistem dalam memberikan 
        jasa lingkungan yang sangat menguntungkan bagi ekonomi publik serta masyarakat Kota Bandung.
    </div>
    """, unsafe_allow_html=True)
