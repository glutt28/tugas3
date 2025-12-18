# Analisis Ulasan Produk

Aplikasi full-stack yang menganalisis ulasan produk menggunakan analisis sentimen berbasis AI dan ekstraksi poin utama.

## Fitur

- 📝 **Input Ulasan Produk**: Pengguna dapat mengirimkan teks ulasan produk
- 🤖 **Analisis Sentimen**: Menganalisis sentimen (positif/negatif/netral) menggunakan Hugging Face transformers
  - **Dukungan Bahasa Indonesia yang Ditingkatkan**: Analisis berbasis aturan dioptimalkan khusus untuk ulasan berbahasa Indonesia
  - **Pendekatan Hibrida**: Menggabungkan model ML dengan analisis berbasis aturan untuk akurasi lebih baik
- 💡 **Ekstraksi Poin Utama**: Mengekstrak poin-poin kunci dari ulasan menggunakan Google Gemini AI
  - **Dukungan Multi-bahasa**: Dioptimalkan untuk ulasan berbahasa Indonesia dan Inggris
  - **Fallback Pintar**: Gemini → Groq → ekstraksi sederhana dengan pemrosesan yang peka bahasa
  - **Dioptimalkan untuk Bahasa Indonesia**: Deteksi kata kunci dan ekstraksi yang ditingkatkan untuk ulasan berbahasa Indonesia
- 💾 **Penyimpanan Database**: Menyimpan semua hasil analisis ke database PostgreSQL
- 🎨 **Antarmuka React Modern**: Frontend yang cantik dan responsif dengan efek glassmorphism
  - **Terlokalisasi Sepenuhnya**: Antarmuka lengkap berbahasa Indonesia
- 🌙 **Mode Gelap**: Transisi tema yang halus
- 🎭 **Animasi**: Animasi menggunakan Framer Motion di seluruh aplikasi
- 📱 **Desain Responsif**: Ramah seluler dengan tata letak split-screen
- 🎠 **Carousel**: Carousel interaktif untuk menelusuri ulasan
- ⚡ **Analisis Waktu-nyata**: Respons API cepat dengan indikator pemuatan dan penanganan error
- 🎯 **Aksesibilitas**: Kontras tinggi, navigasi keyboard, dukungan pembaca layar

## Teknologi

### Backend
- **FastAPI**: Framework web Python modern
- **SQLAlchemy**: ORM untuk operasi database
- **PostgreSQL**: Database relasional
- **Hugging Face Transformers**: Model untuk analisis sentimen
- **Google Gemini API**: Ekstraksi poin-poin utama

### Frontend
- **React 18**: Perpustakaan UI
- **Vite**: Alat build frontend generasi baru
- **Tailwind CSS 4**: Framework CSS utility-first
- **Framer Motion**: Perpustakaan animasi
- **Radix UI**: Komponen aksesibel
- **shadcn/ui**: Perpustakaan komponen berkualitas tinggi
- **Embla Carousel**: Komponen carousel
- **Lucide React**: Perpustakaan ikon
- **Mode Gelap**: Pergantian tema dengan transisi halus

## Prasyarat

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Kunci API Google Gemini ([Dapatkan di sini](https://makersuite.google.com/app/apikey))

## Instalasi

### 1. Clone repositori

```bash
git clone <repository-url>
cd Analisis-Review-Mathew
```

### 2. Persiapan Backend

```bash
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Di Windows:
venv\Scripts\activate
# Di macOS/Linux:
source venv/bin/activate

# Pasang dependensi
pip install -r requirements.txt
```

### 3. Pengaturan Database

Buat database PostgreSQL:

```sql
CREATE DATABASE review_analyzer;
```

### 4. Konfigurasi Environment

Buat file `.env` di direktori `backend`:

```bash
cp .env.example .env
```

Edit `.env` dan tambahkan konfigurasi Anda:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Persiapan Frontend

```bash
cd frontend

# Pasang dependensi
npm install

# (Opsional) Buat file .env untuk URL API kustom
# VITE_API_URL=http://localhost:8000
```

## Menjalankan Aplikasi

### 1. Jalankan PostgreSQL

Pastikan PostgreSQL berjalan di sistem Anda.

### 2. Jalankan Backend

```bash
cd backend
# Aktifkan virtual environment jika belum aktif
python main.py
```

Atau menggunakan uvicorn langsung:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API akan tersedia di `http://localhost:8000`

### 3. Jalankan Frontend

```bash
cd frontend
npm run dev
```

Frontend akan tersedia di `http://localhost:3000`

## Endpoint API

### POST `/api/analyze-review`

Menganalisis sebuah ulasan produk baru.

**Request Body:**
```json
{
  "review_text": "This product is amazing! Great quality and fast shipping."
}
```

**Response:**
```json
{
  "id": 1,
  "review_text": "This product is amazing! Great quality and fast shipping.",
  "sentiment": "positive",
  "key_points": "• Positive overall impression\n• Mentions quality\n• Praises shipping speed",
  "created_at": "2024-01-15T10:30:00"
}
```

### GET `/api/reviews`

Mengambil semua ulasan dengan paginasi.

**Query Parameters:**
- `skip` (opsional): Jumlah record yang dilewati (default: 0)
- `limit` (opsional): Maksimum record yang dikembalikan (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "review_text": "...",
    "sentiment": "positive",
    "key_points": "...",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### DELETE `/api/reviews/{review_id}`

Menghapus ulasan berdasarkan ID.

**Response:**
```json
{
  "message": "Review deleted successfully",
  "id": 1
}
```

### GET `/api/health`

Endpoint pemeriksaan kesehatan (health check).

## Struktur Proyek

```
Analisis-Review-Mathew/
├── backend/
│   ├── main.py                 # Aplikasi FastAPI
│   ├── database.py             # Konfigurasi database
│   ├── models.py               # Model SQLAlchemy
│   ├── schemas.py              # Skema Pydantic
│   ├── sentiment_analyzer.py   # Analisis sentimen Hugging Face
│   ├── key_points_extractor.py # Integrasi API Gemini
│   ├── requirements.txt        # Dependensi Python
│   └── .env.example            # Template variabel environment
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Komponen React utama
│   │   ├── main.jsx           # Titik masuk React (Vite)
│   │   ├── components/
│   │   │   ├── ReviewForm.jsx # Form input ulasan
│   │   │   └── ReviewList.jsx # Tampilan daftar ulasan
│   │   └── *.css             # Berkas gaya
│   ├── index.html            # Template HTML (Vite)
│   ├── vite.config.js        # Konfigurasi Vite
│   └── package.json          # Dependensi Node
├── README.md                  # Berkas ini
└── .gitignore                 # Aturan git ignore
```

## Penanganan Error

Aplikasi ini memiliki penanganan error yang komprehensif:

- **Backend**: Mengembalikan kode status HTTP dan pesan error yang sesuai
- **Frontend**: Menampilkan pesan error yang ramah pengguna
- **Loading States**: Menampilkan indikator pemuatan selama panggilan API
- **Validasi**: Validasi input untuk mencegah ulasan kosong

## Pemecahan Masalah (Troubleshooting)

### Masalah Backend

1. **Kesalahan Koneksi Database**:
  - Pastikan PostgreSQL berjalan
  - Periksa `DATABASE_URL` di file `.env`
  - Pastikan database sudah dibuat

2. **Kesalahan API Gemini**:
  - Pastikan `GEMINI_API_KEY` sudah diset dengan benar
  - Periksa validitas API key
  - Pastikan koneksi internet tersedia

3. **Download Model**:
  - Pada menjalankan pertama kali, model Hugging Face akan diunduh (~500MB)
  - Pastikan koneksi internet stabil

### Masalah Frontend

1. **Kesalahan CORS**:
  - Periksa pengaturan CORS di `main.py`
  - Periksa URL API di frontend

2. **Connection Refused**:
  - Pastikan backend berjalan di port 8000
  - Periksa `VITE_API_URL` di file .env (atau gunakan default http://localhost:8000)
  - Proxy Vite dikonfigurasi di vite.config.js

## Pengembangan

### Pengembangan Backend

```bash
cd backend
uvicorn main:app --reload
```

### Pengembangan Frontend

```bash
cd frontend
npm run dev
```

## Lisensi

Proyek ini bersifat open source dan tersedia di bawah Lisensi MIT.

## Kontribusi

Kontribusi dipersilakan! Silakan ajukan Pull Request.

