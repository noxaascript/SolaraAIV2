# 🤖 SolaraAIV2

**SolaraAIV2** adalah sebuah *modular AI Operating System* berbasis terminal yang menggabungkan beberapa model AI, sistem otomasi browser, dan *runtime* terpadu dalam satu lingkungan terisolasi.

Proyek eksperimental ini dirancang layaknya sistem operasi ringan di dalam terminal. Sistem dapat memilih model AI secara dinamis berdasarkan jenis tugas (coding, penalaran, percakapan umum, atau perencanaan) melalui lapisan *routing* cerdas.

---

## ⚡ Fitur Utama

* **Dynamic AI Routing:** Mengarahkan input pengguna secara otomatis ke model AI terbaik (Qwen untuk percakapan/penalaran, Kimi untuk pengerjaan kode).
* **Memory Layer:** Menyimpan riwayat interaksi masa lalu untuk menjaga konteks percakapan jangka panjang.
* **Lightweight Browser Automation:** Mengambil halaman web (HTTP request) dan mengekstrak teks HTML agar bisa diringkas langsung oleh AI.
* **Terminal UI Runtime:** Antarmuka berbasis teks penuh yang interaktif dan responsif langsung dari command line.

---

## 🛠️ Cara Instalasi & Persyaratan

Pastikan komputer Anda sudah terinstal **Python 3.10 atau versi di atasnya** beserta manajer paket `pip`.

### 1. Kloning Repositori
```bash
git clone https://github.com/noxaascript/SolaraAIV2
cd SolaraAIV2
```

### 2. Instal Dependensi Utama
```bash
pip install requests beautifulsoup4 transformers torch accelerate
```

### 3. Pengaturan API Key (Opsional)
Jika Anda menggunakan model dari HuggingFace yang membutuhkan autentikasi token, masukkan perintah berikut di terminal Anda:
```bash
export HF_API_KEY="isi_token_huggingface_anda_disini"
```

---

## 🚀 Cara Menjalankan Sistem

Anda memiliki dua pilihan untuk mengeksekusi sistem runtime ini:

**Opsi A: Menggunakan Shell Script (Direkomendasikan)**
```bash
bash start.sh
```

**Opsi B: Menggunakan Python Langsung**
```bash
python main.py
```

---

## 🧠 Alur Kerja Sistem (System Behavior)

Saat aplikasi berjalan, setiap input teks Anda akan melewati tahapan berikut:
1. **Input Reception:** Teks diterima melalui antarmuka terminal.
2. **Classification & Routing:** Router menganalisis jenis tugas (chat, coding, atau planning).
3. **Model Selection:** Memilih otomatis antara backend **Qwen**, **Kimi**, atau API eksternal (**Groq / LLaMA**).
4. **Execution & Tools:** Mengaktifkan subsistem memori atau modul browser jika mendeteksi link web.
5. **Output Delivery:** Hasil pemrosesan akhir ditampilkan kembali ke layar terminal Anda.

---

## ⚠️ Catatan & Batasan Proyek
* **Kebutuhan Resource:** Menjalankan model berbasis Transformer lokal seperti Kimi membutuhkan spesifikasi perangkat keras (RAM/VRAM) yang cukup besar.
* **Keterbatasan Browser:** Fitur browser bersifat *lightweight* (hanya berbasis HTTP request & BeautifulSoup) dan tidak setara dengan browser penuh berbasis Chromium.

---

## 💀 Disclaimer
Proyek ini dibuat murni untuk tujuan **eksperimental dan edukasi**. Tidak disarankan atau ditujukan untuk lingkungan produksi (*production environment*). Gunakan dengan bijak dan penuh tanggung jawab.
