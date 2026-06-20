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

# Custom CSS Dark Mode & Vertikal Pendek agar anti-cut-off
st.markdown("""
<style>
    .block-container { padding: 2rem 4rem; background-color: #0e1117; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #4caf50; }
    .banner {
        background: linear-gradient(135deg, #1b5e20, #0d3c12);
        color: white; padding: 35px; border-radius: 20px; margin-bottom: 30px;
        border: 1px solid #2e7d32;
    }
    .metric-card {
        background: #1a1c23; border: 1px solid #2e7d32; border-radius: 15px;
        padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title { font-size: 13px; color: #a5d6a7; text-transform: uppercase; font-weight: bold; }
    .metric-value { font-size: 28px; font-weight: 700; color: #81c784; margin-top: 5px; }
    .info-card {
        background-color: #142116 !important; border-left: 5px solid #4caf50;
        padding: 20px; border-radius: 10px; margin-bottom: 20px; 
        color: #e8f5e9 !important; border-top: 1px solid #1b5e20;
        border-right: 1px solid #1b5e20; border-bottom: 1px solid #1b5e20;
    }
    .info-card h4 { color: #81c784 !important; margin-top: 0; }
    .info-card p, .info-card ul { color: #c8e6c9 !important; }
    /* Menyelaraskan teks standar Streamlit di dalam info-card */
    .info-card stMarkdown, .info-card p { color: #c8e6c9 !important; }
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
    hb = "".join([
        '<div class="banner">',
        '<h1 style="color: white; margin:0; font-size: 38px;">BABAKAN SILIWANGI</h1>',
        '<h3 style="color: #a5d6a7; margin: 5px 0 0 0; font-size: 22px; font-weight: bold;">PBL 6</h3>',
        '<p style="margin: 5px 0 15px 0; font-size: 16px; opacity: 0.9;">',
        'Valuasi Ekonomi & Monitoring Ekosistem Hutan Kota (2025)</p>',
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
        jenis_hutan = df_profil.loc[df_profil['Parameter'] == 'Jenis Hutan', 'Nilai'].values[0]
        status_hutan = df_profil.loc[df_profil['Parameter'] == 'Status', 'Nilai'].values[0]
        
        st.markdown('<div class="info-card"><h4>🌿 Deskripsi Kawasan</h4>', unsafe_allow_html=True)
        st.markdown(f"Babakan Siliwangi adalah **{jenis_hutan}** di Kota Bandung dengan status **{status_hutan}**. Kawasan ini berfungsi sebagai paru-paru kota sekaligus ruang terbuka hijau primer bagi masyarakat perkotaan.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        ketinggian = df_profil.loc[df_profil['Parameter'] == 'Ketinggian', 'Nilai'].values[0]
        curah_hujan = df_profil.loc[df_profil['Parameter'] == 'Curah Hujan (mm/tahun)', 'Nilai'].values[0]
        suhu = df_profil.loc[df_profil['Parameter'] == 'Suhu Rata-rata (C)', 'Nilai'].values[0]
        vegetasi = df_profil.loc[df_profil['Parameter'] == 'Dominan Vegetasi', 'Nilai'].values[0]
        
        st.markdown('<div class="info-card"><h4>📑 Parameter Lingkungan</h4>', unsafe_allow_html=True)
        st.markdown(f"- **Ketinggian:** {ketinggian} mdpl")
        st.markdown(f"- **Curah Hujan:** {curah_hujan} mm/tahun")
        st.markdown(f"- **Suhu Rata-rata:** {suhu}°C")
        st.markdown(f"- **Vegetasi Dominan:** {vegetasi}")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MENU 2: DASHBOARD PROFIL
# ==========================================
elif menu == "📊 Dashboard Profil":
    st.subheader("📊 Ringkasan Indikator Babakan Siliwangi")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Luas Wilayah</div><div class="metric-value">{float(luas_kawasan)} Ha</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Pengunjung/Thn</div><div class="metric-value">{int(total_pengunjung):,}</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Serapan Karbon</div><div class="metric-value">{int(float(serapan_karbon))} Ton</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Valuasi Total</div><div class="metric-value">Rp {float(total_valuasi):,.0f}</div></div>', unsafe_allow_html=True)

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
        # Menyesuaikan chart ke tema gelap
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.markdown("### Detail Parameter Vegetasi")
        st.table(df_veg)

# ==========================================
# MENU 3: ANALISIS EKONOMI
# ==========================================
elif menu == "📈 Analisis Ekonomi":
    st.subheader("📈 Tren Nilai Ekonomi vs Biaya Pengelolaan")
    
    kolom_y = []
    if "nilai_ekonomi" in df_trend.columns:
        kolom_y.append("nilai_ekonomi")
    else:
        kolom_y.append("Nilai Ekonomi (Rp)")
        
    if "biaya_pengelolaan" in df_trend.columns:
        kolom_y.append("biaya_pengelolaan")
    else:
        kolom_y.append("Biaya Pengelolaan (Rp)")
        
    kolom_x = "tahun" if "tahun" in df_trend.columns else "Tahun"
    kolom_visitor = "pengunjung" if "pengunjung" in df_trend.columns else "Pengunjung"

    fig_eco = px.line(
    df_trend,
    x=kolom_x,
    y=kolom_y,
    title="Perbandingan Jasa Lingkungan vs Biaya",
    markers=True,
    color_discrete_sequence=["#81c784", "#e53935"]
    )
    fig_eco.update_layout(template="plotly_dark", yaxis_title="Rupiah", hovermode="x unified", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_eco, use_container_width=True)
    
    st.write("---")
    
    fig_visitor = px.bar(
    df_trend,
    x=kolom_x,
    y=kolom_visitor,
    title="Tren Pertumbuhan Pengunjung Tahunan",
    color=kolom_visitor,
    color_continuous_scale="Greens"
    )
    fig_visitor.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_visitor, use_container_width=True)

    ta = "".join([
        '<div class="card" style="background: #1a1c23; padding: 15px; border-radius: 10px; ',
        'border-top: 4px solid #4caf50; box-shadow: 0 2px 8px rgba(0,0,0,0.5); color: #c8e6c9;">💡 ',
        '<b>Analisis:</b> Berdasarkan data historis, Nilai Ekonomi Lingkungan jauh melampaui ',
        'Biaya Pengelolaan. Hal ini menunjukkan efisiensi ekosistem dalam memberikan ',
        'jasa lingkungan bagi publik Kota Bandung.</div>'
    ])
    st.markdown(ta, unsafe_allow_html=True)
