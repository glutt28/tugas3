# 🔧 Gemini API Troubleshooting

## Problem: No Available Gemini Model Found

Jika semua model Gemini tidak tersedia, ikuti langkah berikut:

## 🔍 Langkah 1: Periksa Model yang Tersedia

Jalankan script untuk check model yang tersedia:

```bash
cd backend
venv\Scripts\activate
python check_gemini_models.py
```

Script ini akan:
- Check API key
- List semua model yang tersedia
- Rekomendasikan model yang bisa digunakan

## ✅ Langkah 2: Perbaiki Berdasarkan Hasil

### Jika Model Ditemukan

Update `key_points_extractor.py` untuk menggunakan model yang tersedia:

```python
# Ganti models_to_try dengan model yang tersedia
models_to_try = [
    'gemini-1.5-flash',  # atau model lain yang tersedia
]
```

### Jika Tidak Ada Model

**Kemungkinan penyebab:**

1. **API Key Invalid**
   - Check API key di `.env` file
   - Pastikan API key valid di [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Generate API key baru jika perlu

2. **API Key Tidak Memiliki Akses**
   - Pastikan API key memiliki permission untuk Gemini API
   - Check di Google Cloud Console

3. **API Key Region/Restriction**
   - Beberapa region mungkin tidak support Gemini
   - Coba dengan VPN atau check region settings

## 🔄 Step 3: Fallback Solution

Kode sudah diupdate dengan **simple extraction fallback**. Jika Gemini tidak tersedia, aplikasi akan:
- Tetap berfungsi dengan simple text extraction
- Extract key points dari kalimat penting
- Tidak crash atau return error

## 🛠️ Perbaikan Manual

### Option 1: Update API Key

1. Dapatkan API key baru di: https://makersuite.google.com/app/apikey
2. Update file `backend/.env`:
   ```env
   GEMINI_API_KEY=your_new_api_key_here
   ```

### Opsi 2: Periksa Izin Kunci API

1. Buka [Google AI Studio](https://aistudio.google.com/)
2. Check API key settings
3. Pastikan Gemini API enabled

### Opsi 3: Gunakan Cadangan Saja

Jika Gemini tidak bisa digunakan, aplikasi akan otomatis menggunakan simple extraction. Tidak perlu konfigurasi tambahan.

## 📝 Verifikasi Perbaikan

Setelah fix, test lagi:

```bash
# Periksa model
python check_gemini_models.py

# Restart server
python start_server.py

# Test dengan submit review
```

## 💡 Tips

1. **Simple extraction sudah cukup** untuk kebanyakan use case
2. **Gemini memberikan hasil lebih baik** tapi tidak wajib
3. **Aplikasi tetap berfungsi** meskipun Gemini tidak tersedia
4. **Check API quota** jika masih error

## 🔗 Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Get API Key](https://makersuite.google.com/app/apikey)

## ✅ Expected Behavior

Setelah fix:
- Jika Gemini tersedia: menggunakan Gemini untuk extraction
- Jika Gemini tidak tersedia: menggunakan simple extraction (fallback)
- Aplikasi tetap berfungsi dalam kedua kondisi

