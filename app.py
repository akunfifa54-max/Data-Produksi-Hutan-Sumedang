import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Eco-Forest Valuation KPH Cepu",
    page_icon="🌳",
    layout="wide"
)

# --- HEADER APLIKASI ---
st.title("🌳 Eco-Forest Valuation Dashboard")
st.subheader("Analisis Nilai Ekonomi Total (Total Economic Value) - KPH Cepu")
st.markdown("---")

# --- SIDEBAR: INPUT DATA & PARAMETER ---
st.sidebar.header("📊 Parameter Valuasi")

# Pilihan Input Data
data_source = st.sidebar.radio("Pilih Sumber Data:", ("Gunakan Data Standar (Simulasi)", "Unggah File CSV/Excel"))

# Default Data jika user tidak upload file
default_data = pd.DataFrame({
    'Blok/Resort': ['Blok A', 'Blok B', 'Blok C', 'Blok D'],
    'Luas_Ha': [120, 250, 85, 190],
    'Volume_Kayu_M3': [2400, 5200, 1600, 3900],
    'Estimasi_Karbon_Ton': [3600, 7500, 2550, 5700]
})

if data_source == "Unggah File CSV/Excel":
    uploaded_file = st.sidebar.file_uploader("Unggah file Anda di sini", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("File berhasil diunggah!")
    else:
        st.sidebar.info("Menampilkan data simulasi sementara.")
        df = default_data
else:
    df = default_data

# Nilai Asumsi Ekonomi (Bisa diubah-ubah oleh user via Sidebar)
st.sidebar.markdown("### 💰 Asumsi Harga Pasar")
harga_kayu = st.sidebar.number_input("Harga Kayu rata-rata (Rp / m³)", value=2500000, step=100000)
harga_karbon = st.sidebar.number_input("Harga Karbon Per Ton (Rp)", value=150000, step=10000)
jasa_air = st.sidebar.number_input("Nilai Jasa Air & Wisata (Rp / Hektar / Tahun)", value=500000, step=50000)


# --- PROSES PERHITUNGAN VALUASI ---
# 1. Valuasi Kayu
df['Nilai_Ekonomi_Kayu'] = df['Volume_Kayu_M3'] * harga_kayu

# 2. Valuasi Karbon
df['Nilai_Ekonomi_Karbon'] = df['Estimasi_Karbon_Ton'] * harga_karbon

# 3. Valuasi Jasa Lingkungan
df['Nilai_Jasa_Lingkungan'] = df['Luas_Ha'] * jasa_air

# 4. Total Nilai Ekonomi per Blok
df['Total_Valuasi'] = df['Nilai_Ekonomi_Kayu'] + df['Nilai_Ekonomi_Karbon'] + df['Nilai_Jasa_Lingkungan']


# --- DISPLAY UTAMA ---

# Tampilan Metrics Ringkasan Total
total_luas = df['Luas_Ha'].sum()
total_valuasi_idr = df['Total_Valuasi'].sum()
total_karbon_ton = df['Estimasi_Karbon_Ton'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🌳 Total Luas Area Analisis", value=f"{total_luas:,} Ha")
with col2:
    st.metric(label="🌱 Total Serapan Karbon", value=f"{total_karbon_ton:,} Ton")
with col3:
    st.metric(label="💰 Total Nilai Ekonomi (TEV)", value=f"Rp {total_valuasi_idr:,.0f}")

st.markdown("---")

# Layout Grafik dan Tabel
tab1, tab2 = st.tabs(["📊 Grafik Analisis", "📋 Tabel Data"])

with tab1:
    st.write("### Komposisi Nilai Ekonomi Hutan")
    
    # Transformasi data untuk grafik stacked bar
    df_melted = df.melt(id_vars=['Blok/Resort'], 
                        value_vars=['Nilai_Ekonomi_Kayu', 'Nilai_Ekonomi_Karbon', 'Nilai_Jasa_Lingkungan'],
                        var_name='Jenis Valuasi', value_name='Nilai (Rp)')
    
    # Ganti nama label biar rapi di grafik
    df_melted['Jenis Valuasi'] = df_melted['Jenis Valuasi'].str.replace('_', ' ')

    fig = px.bar(df_melted, x='Blok/Resort', y='Nilai (Rp)', color='Jenis Valuasi',
                 title="Distribusi Nilai Ekonomi Berdasarkan Blok/Resort di KPH Cepu",
                 barmode='stack', text_auto='.2s')
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write("### Detail Data Hasil Perhitungan")
    
    # Format mata uang untuk tampilan tabel
    df_formatted = df.copy()
    for col in ['Nilai_Ekonomi_Kayu', 'Nilai_Ekonomi_Karbon', 'Nilai_Jasa_Lingkungan', 'Total_Valuasi']:
        df_formatted[col] = df_formatted[col].apply(lambda x: f"Rp {x:,.0f}")
        
    st.dataframe(df_formatted, use_container_width=True)

# Fitur Unduh Hasil Analisis
st.markdown("---")
st.write("### 📥 Ekspor Hasil")
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Unduh Data Valuasi (.CSV)",
    data=csv_data,
    file_name='Hasil_Valuasi_EcoForest_KPH_Cepu.csv',
    mime='text/csv',
)
