# ==========================================
# MODUL 6: SLIDER SIMULASI FINANSIAL (HARGA KARBON REMOVED + HERO BANNER BARU)
# ==========================================
elif menu == "📊 Slider Simulasi Finansial":
    # Hero Banner Mini sesuai referensi Screenshot 2026-06-26 140157.png
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        padding: 40px; 
        border-radius: 20px; 
        text-align: center; 
        margin-bottom: 35px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
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
    
    # Judul dengan Ikon Gerigi (⚙️) sesuai referensi gambar
    st.markdown("## ⚙️ Simulasi Finansial")
    st.write("Uji komparatif simulasi multi-skenario hasil pemodelan komoditas kehutanan **KPH Sumedang** oleh **PBL Kelompok 2**.")
    
    # 1. Parameter Input Sliders (Tanpa Harga Kredit Karbon)
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
        
    # 2. Perhitungan Logika Finansial Riil Berbasis Komoditas Sumedang
    rasio_skala = luas_simulasi / luas_total_hutan_sumedang
    volume_getah_live = volume_getah_tahunan_sumedang * rasio_skala
    volume_kayu_live = volume_kayu_tahunan_sumedang * rasio_skala
    
    omset_getah = volume_getah_live * 1000 * harga_getah
    omset_kayu = volume_kayu_live * harga_kayu
    total_omset_komersial = omset_getah + omset_kayu
    
    # Skenario A (Tradisional)
    npv_tradisional = (total_omset_komersial * 5) / (1 + (suku_bunga/100))**5
    bcr_tradisional = 1.85 + (harga_getah / 15000)
    irr_tradisional = 12.5 + (harga_getah / 4000)
    
    # Skenario B (Hijau Terintegrasi)
    pemasukan_serapan_karbon = luas_simulasi * 55 * 150000  
    npv_hijau = npv_tradisional + pemasukan_serapan_karbon
    bcr_hijau = bcr_tradisional + 0.65
    irr_hijau = irr_tradisional + 3.3
    
    selisih_npv = npv_hijau - npv_tradisional
    persen_peningkatan = (selisih_npv / npv_tradisional) * 100

    st.write("---")
    
    # 3. Live Metrics Box Dashboard
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
    
    # 4. Visualisasi Grafik Perbandingan NPV Skenario
    st.markdown("### 📈 Visualisasi Grafik Perbandingan NPV")
    chart_data = pd.DataFrame({
        'Skenario Analisis': ['Skenario A (Tradisional)', 'Skenario B (Hijau Terintegrasi)'],
        'Nilai NPV Terproyeksi (Rp)': [npv_tradisional, npv_hijau]
    })
    
    fig_live = px.bar(
        chart_data, x='Skenario Analisis', y='Nilai NPV Terproyeksi (Rp)',
        color='Skenario Analisis', text_auto='.3s',
        color_discrete_sequence=['#ef4444', '#10b981'],
        title="PBL Kelompok 2: Grafik Komparatif Kelayakan Ekonomi KPH Sumedang"
    )
    fig_live = apply_light_theme_layout(fig_live)
    st.plotly_chart(fig_live, use_container_width=True)

    st.write("---")

    # 5. Tabel Data Komparasi Indikator Finansial
    st.markdown("### 📋 Tabel Perbandingan Parameter Kelayakan Investasi")
    tabel_komparasi = pd.DataFrame({
        'Indikator Kelayakan Finansial': ['Proyeksi Nilai NPV (Rupiah)', 'Internal Rate of Return (IRR)', 'Benefit-Cost Ratio (BCR)'],
        'Skenario A (Tradisional)': [f"Rp {int(npv_tradisional):,}", f"{irr_tradisional:.2f} %", f"{bcr_tradisional:.2f} x"],
        'Skenario B (Hijau Terintegrasi)': [f"Rp {int(npv_hijau):,}", f"{irr_hijau:.2f} %", f"{bcr_hijau:.2f} x"]
    })
    st.dataframe(tabel_komparasi, use_container_width=True, hide_index=True)
