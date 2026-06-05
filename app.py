import streamlit as st

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Simulasi Kasir Supermarket", page_icon="🛒", layout="centered")

# --- INISIALISASI QUEUE DI SESSION STATE ---
# Ini penting agar data antrian tetap tersimpan saat halaman merefresh otomatis
if "antrian_supermarket" not in st.session_state:
    st.session_state.antrian_supermarket = []

# Variabel bantuan untuk mempermudah pembacaan kode
antrian = st.session_state.antrian_supermarket

# --- JUDUL APLIKASI ---
st.title("🛒 Simulasi Checkout Supermarket")
st.caption("Struktur Data: Queue (First In, First Out - FIFO)")
st.write("---")

# --- TAMPILAN UTAMA (LAYOUT KOLOM) ---
kolom_kiri, kolom_kanan = st.columns([1, 1])

# --- KOLOM KIRI: KONTROL ANTRIAN ---
with kolom_kiri:
    st.subheader("⚙️ Panel Kontrol Kasir")
    
    # Form untuk Tambah Pelanggan (Enqueue)
    with st.form(key="form_tambah", clear_on_submit=True):
        nama_baru = st.text_input("Nama Pelanggan Baru:", placeholder="Masukkan nama...")
        tombol_tambah = st.form_submit_button(label="Masuk Antrian ➕")
        
        if tombol_tambah:
            if nama_baru.strip() != "":
                antrian.append(nama_baru.strip()) # Operasi Enqueue (tambah ke belakang)
                st.success(f"**{nama_baru}** berhasil masuk antrian!")
            else:
                st.warning("Nama tidak boleh kosong!")

    st.write("") # Jarak spacer

    # Tombol untuk Melayani Pelanggan (Dequeue)
    st.markdown("**Aksi Kasir:**")
    if st.button("Layani Pelanggan Depan 💳", type="primary", use_container_width=True):
        if len(antrian) > 0:
            pelanggan_dilayani = antrian.pop(0) # Operasi Dequeue (ambil indeks 0 / paling depan)
            st.toast(f"🎉 {pelanggan_dilayani} selesai dilayani!", icon="✅")
            st.info(f"⚡ Sedang dilayani & selesai: **{pelanggan_dilayani}**")
        else:
            st.error("Antrian kosong! Tidak ada pelanggan untuk dilayani.")
            
    # Tombol Reset
    if st.button("Kosongkan Semua Antrian 🔄", use_container_width=True):
        st.session_state.antrian_supermarket = []
        st.rerun()

# --- KOLOM KANAN: MONITOR ANTRIAN ---
with kolom_kanan:
    st.subheader("📋 Visualisasi Antrian")
    
    total_orang = len(antrian)
    st.metric(label="Total Antrian Saat Ini", value=f"{total_orang} Orang")
    
    if total_orang > 0:
        st.write("**Urutan Barisan (Depan ➡️ Belakang):**")
        
        # Menampilkan daftar antrian dengan visual menarik
        for indeks, pelanggan in enumerate(antrian):
            if indeks == 0:
                # Pelanggan paling depan diberi tanda khusus
                st.info(f"🥇 **[1] {pelanggan}** ← *Giliran berikutnya!*")
            else:
                st.markdown(f"👤 **[{indeks + 1}]** {pelanggan}")
    else:
        st.info("Jalur kasir kosong. Silakan tambah pelanggan di panel sebelah kiri.")