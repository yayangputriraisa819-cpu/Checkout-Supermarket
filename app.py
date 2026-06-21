import streamlit as st
import time

st.set_page_config(
    page_title="Checkout Supermarket Advance", 
    page_icon="🛒", 
    layout="wide"
)

MENU_BARANG = {
    "Mie Instan": 3500,
    "Susu Kotak": 6000,
    "Roti Tawar": 15000,
    "Minyak Goreng 2L": 38000,
    "Sabun Mandi": 4500,
    "Air Mineral": 4000
}

KODE_DISKON = {
    "HEMAT10": 0.10, 
    "UNTUNG20": 0.20   
}

if "antrian_kasir" not in st.session_state:
    st.session_state.antrian_kasir = []

if "keranjang_sementara" not in st.session_state:
    st.session_state.keranjang_sementara = {}

daftar_antrian = st.session_state.antrian_kasir
keranjang = st.session_state.keranjang_sementara

st.title("🖥️ Checkout Supermarket (Edisi Advance)")
st.caption("Implementasi Struktur Data Queue (FIFO) dengan Fitur Transaksi Finansial Realistis")
st.markdown("---")

kolom_menu, kolom_kontrol, kolom_visual = st.columns([1.1, 1.1, 1.3])

with kolom_menu:
    st.header("🛍️ 1. Ambil Barang")
    
    for barang, harga in MENU_BARANG.items():
        col_item, col_btn = st.columns([2, 1])
        col_item.write(f"**{barang}** — Rp {harga:,}")
        if col_btn.button(f"Tambah ➕", key=f"add_{barang}"):
            keranjang[barang] = keranjang.get(barang, 0) + 1
            st.toast(f"{barang} dimasukkan!", icon="📥")

    st.write("---")
    st.write("### 🛒 Isi Keranjang Sekarang:")
    
    total_bruto = 0
    if keranjang:
        for barang, jumlah in list(keranjang.items()):
            subtotal = MENU_BARANG[barang] * jumlah
            total_bruto += subtotal
            st.caption(f"▪️ {barang} (x{jumlah}) — Rp {subtotal:,}")
        
        st.write(f"**Subtotal Belanja: Rp {total_bruto:,}**")
        
        if st.button("Kosongkan Keranjang 🗑️", use_container_width=True):
            st.session_state.keranjang_sementara = {}
            st.rerun()
    else:
        st.info("Keranjang kosong. Pilih barang di atas.")

with kolom_kontrol:
    st.header("⚙️ 2. Gerbang Antrian")
    
    st.write("### Fungsi Enqueue (Masuk Barisan)")
    with st.form(key="form_pendaftaran", clear_on_submit=True):
        nama_pelanggan = st.text_input("Nama Pelanggan:", placeholder="Nama pembeli...")
        kode_input = st.text_input("Kode Diskon (Opsional):", placeholder="Contoh: HEMAT10 / UNTUNG20").upper()
        tombol_masuk = st.form_submit_button(label="Giring ke Jalur Antrian ➡️")
        
        if tombol_masuk:
            if not nama_pelanggan.strip():
                st.error("Gagal: Nama pembeli tidak boleh kosong!")
            elif not keranjang:
                st.error("Gagal: Pelanggan belum belanja apapun!")
            else:
                potongan = KODE_DISKON.get(kode_input, 0.0)
                nilai_diskon = int(total_bruto * potongan)
                total_akhir = total_bruto - nilai_diskon
                
                data_pembeli = {
                    "nama": nama_pelanggan.strip(),
                    "item_belanja": keranjang.copy(),
                    "total_tagihan": total_akhir,
                    "diskon_didapat": nilai_diskon
                }
                daftar_antrian.append(data_pembeli)
                st.session_state.keranjang_sementara = {} 
                st.success(f"🎉 **{nama_pelanggan}** masuk antrian!")
                st.rerun()

    st.write("---")
    
    st.write("### Fungsi Dequeue (Proses Meja Kasir)")
    if len(daftar_antrian) > 0:
        p_depan = daftar_antrian[0]
        st.warning(f"Pelanggan Terdepan: **{p_depan['nama']}** (Tagihan: Rp {p_depan['total_tagihan']:,})")
        
        metode_bayar = st.radio("Metode Pembayaran:", ["Tunai (Cash)", "QRIS / Digital Payment"])
        
        uang_dibayar = 0
        pembayaran_sah = False
        
        if metode_bayar == "Tunai (Cash)":
            uang_dibayar = st.number_input("Jumlah Uang Tunai Pembeli (Rp):", min_value=0, step=5000)
            if uang_dibayar >= p_depan['total_tagihan']:
                st.success(f"Uang Pas/Lebih. Kembalian: Rp {uang_dibayar - p_depan['total_tagihan']:,}")
                pembayaran_sah = True
            else:
                st.error("Uang yang dimasukkan kurang!")
        else:
            st.info("Pindai Kode QR Berhasil. Pembayaran digital otomatis terverifikasi lunas.")
            pembayaran_sah = True
            
        if st.button("Selesaikan Pelayanan & Cetak Struk 💳", type="primary", use_container_width=True, disabled=not pembayaran_sah):
            pelanggan_keluar = daftar_antrian.pop(0)
            with st.spinner("Mencetak Nota Transaksi..."):
                time.sleep(1)
            st.success(f"Sukses! Struk belanja milik **{pelanggan_keluar['nama']}** telah dicetak.")
            st.balloons()
            st.rerun()
    else:
        st.info("Tidak ada transaksi berjalan. Antrian kosong.")

with kolom_visual:
    st.header("📋 3. Monitor & Pembatalan")
    
    total_orang = len(daftar_antrian)
    st.metric(label="Panjang Antrian Saat Ini", value=f"{total_orang} Pelanggan")
    
    st.write("### Visualisasi Lintasan Antrian:")
    if total_orang > 0:
        
        for urutan, p in enumerate(list(daftar_antrian), start=1):
            detail_barang = ", ".join([f"{k} (x{v})" for k, v in p['item_belanja'].items()])
            
            with st.container(border=True):
                col_info_antrian, col_aksi_batal = st.columns([3, 1])
                
                with col_info_antrian:
                    if urutan == 1:
                        st.markdown(f"🥇 **[URUTAN 1 - DI DEPAN KASIR]** — **{p['nama']}**")
                    else:
                        st.markdown(f"👤 **[Posisi {urutan}]** — **{p['nama']}**")
                    st.caption(f"🛒 Items: {detail_barang} | Potongan: Rp {p['diskon_didapat']:,}")
                    st.markdown(f"💰 **Total Tagihan: Rp {p['total_tagihan']:,}**")
                
                with col_aksi_batal:
                    st.write("") 
                    if st.button("Batal ❌", key=f"cancel_{urutan}_{p['nama']}"):
                        pembeli_batal = daftar_antrian.pop(urutan - 1)
                        st.toast(f"{pembeli_batal['nama']} keluar dari antrian!", icon="⚠️")
                        st.rerun()
                        
        st.caption("💡 *Catatan Teknis Presentasi: Menekan tombol 'Batal' menguji fungsi manipulasi indeks larik/list di luar fungsi Queue standar.*")
    else:
        st.success("🎉 Jalur kasir aman terkendali. Tidak ada antrian terdeteksi.")
        
    if st.button("Reset Sistem Menyeluruh 🔄", use_container_width=True):
        st.session_state.antrian_kasir = []
        st.session_state.keranjang_sementara = {}
        st.rerun()