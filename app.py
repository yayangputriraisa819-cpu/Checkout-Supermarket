import streamlit as st
import time

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="Sistem Kasir & Antrian Supermarket", 
    page_icon="🛒", 
    layout="wide"
)

# 2. DAFTAR MENU BARANG SUPERMARKET (DATABASE)
MENU_BARANG = {
    "Mie Instan": 3500,
    "Susu Kotak": 6000,
    "Roti Tawar": 15000,
    "Minyak Goreng 2L": 38000,
    "Sabun Mandi": 4500,
    "Kopi Sachet": 2000,
    "Cemilan Keripik": 8500,
    "Air Mineral": 4000
}

# 3. MANAJEMEN STATE (MEMORI PERSISTEN STREAMLIT)
if "antrian_kasir" not in st.session_state:
    st.session_state.antrian_kasir = []  # Menyimpan list dari dictionary pelanggan

if "keranjang_sementara" not in st.session_state:
    st.session_state.keranjang_sementara = {}  # Menyimpan item yang sedang dipilih sebelum masuk antrian

# Referensi variabel state agar kode lebih pendek
daftar_antrian = st.session_state.antrian_kasir
keranjang = st.session_state.keranjang_sementara

# 4. HEADER & JUDUL APLIKASI
st.title("🖥️ Sistem Integrasi: Menu Belanja & Antrian Kasir")
st.subheader("Implementasi Struktur Data: Linear Queue (First In, First Out - FIFO)")
st.write("Simulasi nyata kasir supermarket: Pelanggan memilih barang belanjaan, masuk antrian, lalu dilayani sesuai urutan kedatangan.")
st.markdown("---")

# 5. PEMBAGIAN LAYAR (3 KOLOM UTAMA)
kolom_menu, kolom_kontrol, kolom_visual = st.columns([1.2, 1.1, 1.3])

# ==================== KOLOM 1: MENU BELANJA & KERANJANG ====================
with kolom_menu:
    st.header("🛍️ 1. Menu Belanjaan")
    st.write("Pilih barang yang ingin dibeli pelanggan saat ini:")
    
    # Menampilkan daftar barang dalam bentuk interaktif
    for barang, harga in MENU_BARANG.items():
        col_item, col_btn = st.columns([2, 1])
        col_item.write(f"**{barang}** — Rp {harga:,}")
        
        # Tombol tambah ke keranjang sementara
        if col_btn.button(f"Tambah ➕", key=f"btn_{barang}"):
            if barang in keranjang:
                keranjang[barang] += 1
            else:
                keranjang[barang] = 1
            st.toast(f"{barang} dimasukkan ke keranjang!", icon="📥")

    st.write("---")
    st.write("### 🛒 Keranjang Belanja Saat Ini:")
    
    total_belanja_sementara = 0
    if keranjang:
        for barang, jumlah in list(keranjang.items()):
            subtotal = MENU_BARANG[barang] * jumlah
            total_belanja_sementara += subtotal
            st.caption(f"▪️ {barang} (x{jumlah}) — Rp {subtotal:,}")
        
        st.write(f"**Total Sementara: Rp {total_belanja_sementara:,}**")
        
        # Tombol reset keranjang belanjaan
        if st.button("Kosongkan Keranjang 🗑️"):
            st.session_state.keranjang_sementara = {}
            st.rerun()
    else:
        st.info("Keranjang belanja masih kosong. Silakan klik 'Tambah'.")

# ==================== KOLOM 2: PANEL KONTROL KASIR ====================
with kolom_kontrol:
    st.header("⚙️ 2. Operasi Queue")
    
    # --- OPERASI ENQUEUE (MASUKKAN PELANGGAN BESERTA BELANJAANNYA) ---
    st.write("### Enqueue (Masuk Antrian)")
    with st.form(key="form_antrian", clear_on_submit=True):
        nama_pelanggan = st.text_input("Nama Pelanggan:", placeholder="Masukkan nama...")
        tombol_masuk = st.form_submit_button(label="Kirim ke Jalur Kasir ➡️")
        
        if tombol_masuk:
            if not nama_pelanggan.strip():
                st.error("Gagal: Nama pelanggan harus diisi!")
            elif not keranjang:
                st.error("Gagal: Pelanggan belum mengambil barang di Menu Belanja!")
            else:
                # Membuat objek data pelanggan baru untuk disimpan di Queue
                data_pelanggan = {
                    "nama": nama_pelanggan.strip(),
                    "item_belanja": keranjang.copy(),
                    "total_harga": total_belanja_sementara
                }
                # ENQUEUE: Tambahkan ke data paling belakang list
                daftar_antrian.append(data_pelanggan)
                
                # Reset keranjang sementara untuk pelanggan berikutnya
                st.session_state.keranjang_sementara = {}
                st.success(f"🎉 **{nama_pelanggan}** resmi mengantri!")
                st.rerun()

    st.write("---")

    # --- OPERASI DEQUEUE (LAYANI PELANGGAN TERDEPAN) ---
    st.write("### Dequeue (Proses Kasir)")
    if st.button("Layani Pelanggan Terdepan 💳", type="primary", use_container_width=True):
        if len(daftar_antrian) > 0:
            # DEQUEUE: Mengambil dan menghapus elemen indeks ke-0 (paling depan)
            pelanggan_dilayani = daftar_antrian.pop(0)
            
            # Animasi visual pemindaian barang
            with st.spinner(f"Kasir sedang memindai belanjaan {pelanggan_dilayani['nama']}..."):
                time.sleep(1.5)
            
            st.success(f"✅ Selesai! **{pelanggan_dilayani['nama']}** membayar sebesar **Rp {pelanggan_dilayani['total_harga']:,}**")
            st.balloons()
        else:
            st.warning("⚠️ Operasi Gagal: Jalur antrian kasir kosong!")

    st.write("")
    if st.button("Reset Seluruh Sistem 🔄", use_container_width=True):
        st.session_state.antrian_kasir = []
        st.session_state.keranjang_sementara = {}
        st.rerun()

# ==================== KOLOM 3: MONITOR VISUALISASI ====================
with kolom_visual:
    st.header("📋 3. Monitor Kasir")
    
    jumlah_antrian = len(daftar_antrian)
    st.metric(label="Total Orang di Jalur Kasir", value=f"{jumlah_antrian} Pelanggan")
    
    st.write("### Garis Antrian Riil:")
    if jumlah_antrian > 0:
        for urutan, p in enumerate(daftar_antrian, start=1):
            # Menghias tampilan detail belanjaan per orang di antrian
            detail_barang = ", ".join([f"{k} (x{v})" for k, v in p['item_belanja'].items()])
            
            if urutan == 1:
                st.info(
                    f"🥇 **[URUTAN DEPAN]** — **{p['nama']}**\n"
                    f"🛒 Belanjaan: *{detail_barang}*\n\n"
                    f"💰 **Total Tagihan: Rp {p['total_harga']:,}**"
                )
            else:
                st.markdown(
                    f"👤 **[Urutan {urutan}]** — **{p['nama']}**\n"
                    f"📦 Barang: *{detail_barang}* | Total: Rp {p['total_harga']:,}\n"
                    f"---"
                )
        st.caption("⬆️ Pelanggan posisi teratas akan diproses keluar terlebih dahulu (FIFO).")
    else:
        st.success("😎 Jalur kasir kosong bersih! Semua pelanggan telah selesai dilayani.")