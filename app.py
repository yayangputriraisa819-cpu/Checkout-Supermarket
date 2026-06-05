class CheckoutSupermarket:
    def __init__(self):
        # Inisialisasi antrian kosong
        self.antrian = []

    def tambah_pelanggan(self, nama_pelanggan):
        """Fungsi Enqueue: Menambahkan pelanggan ke belakang antrian"""
        self.antrian.append(nama_pelanggan)
        print(f"🛒 {nama_pelanggan} telah masuk ke antrian checkout.")

    def layani_pelanggan(self):
        """Fungsi Dequeue: Melayani pelanggan di urutan paling depan (FIFO)"""
        if not self.apakah_kosong():
            # Mengambil elemen pertama (indeks 0) sesuai prinsip FIFO
            pelanggan_dilayani = self.antrian.pop(0)
            print(f"💳 Kasir sedang melayani: {pelanggan_dilayani}. Selesai!")
        else:
            print("🔔 Semua antrian kasir kosong. Tidak ada pelanggan yang mengantri.")

    def lihat_antrian(self):
        """Menampilkan semua pelanggan yang sedang mengantri saat ini"""
        if not self.apakah_kosong():
            print("\n--- DAFTAR ANTRIAN KASIR SUPERMARKET ---")
            for urutan, pelanggan in enumerate(self.antrian, start=1):
                print(f"{urutan}. {pelanggan}")
            print("----------------------------------------")
        else:
            print("ℹ️ Antrian saat ini kosong.")

    def apakah_kosong(self):
        """Mengecek apakah antrian sedang kosong"""
        return len(self.antrian) == 0

    def total_antrian(self):
        """Melihat jumlah orang yang sedang mengantri"""
        return len(self.antrian)


# === SIMULASI PENGGUNAAN KASIR SUPERMARKET ===
kasir_1 = CheckoutSupermarket()

# 1. Pelanggan mulai berdatangan dan masuk antrian
kasir_1.tambah_pelanggan("Andi")
kasir_1.tambah_pelanggan("Budi")
kasir_1.tambah_pelanggan("Citra")

# 2. Melihat kondisi antrian saat ini
kasir_1.lihat_antrian()
print(f"Total orang mengantri: {kasir_1.total_antrian()} orang.\n")

# 3. Kasir mulai melayani pelanggan (FIFO: Andi harus dilayani duluan)
kasir_1.layani_pelanggan()
kasir_1.layani_pelanggan()

# 4. Melihat sisa antrian setelah dua orang dilayani
kasir_1.lihat_antrian()

# 5. Pelanggan baru datang lagi
kasir_1.tambah_pelanggan("Dewi")
kasir_1.lihat_antrian()