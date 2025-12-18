# 🚀 Groq API Setup - Fallback untuk Gemini

## 📋 Apa itu Groq?

Groq adalah AI inference platform yang:
- ✅ **Sangat cepat** - Inference dalam milliseconds
- ✅ **Free tier lebih baik** - 14,400 requests/hari (vs Gemini 20/hari)
- ✅ **Multiple models** - Llama, Mixtral, dll
- ✅ **No credit card required** untuk free tier

## 🔑 Mendapatkan Groq API Key

### Step 1: Daftar di Groq
1. Kunjungi: https://console.groq.com/
2. Sign up dengan Google/GitHub/Email
3. Verifikasi email jika diperlukan

### Step 2: Generate API Key
1. Login ke https://console.groq.com/
2. Klik **API Keys** di sidebar
3. Klik **Create API Key**
4. Copy API key yang dihasilkan

### Step 3: Tambahkan ke .env
Edit file `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Atau gunakan setup script:
```bash
python setup_db.py
```

## ✅ Verifikasi Setup

Test Groq API:

```bash
python -c "from key_points_extractor import _try_groq_extraction; print(_try_groq_extraction('This product is great!'))"
```

## 🎯 Cara Kerja Fallback

Aplikasi akan mencoba dalam urutan:

1. **Gemini API** (jika tersedia dan quota OK)
2. **Groq API** (jika Gemini tidak tersedia/quota habis)
3. **Simple Extraction** (jika semua API tidak tersedia)

## 📊 Perbandingan

| Feature | Gemini Free | Groq Free | Simple Extraction |
|---------|------------|-----------|-------------------|
| Requests/day | 20 | 14,400 | Unlimited |
| Speed | Fast | Very Fast | Instant |
| Quality | Excellent | Excellent | Good |
| Cost | Free | Free | Free |

## 💡 Rekomendasi

### Setup Keduanya:
- **Gemini**: Untuk hasil terbaik (jika quota tersedia)
- **Groq**: Fallback yang sangat baik (quota besar)
- **Simple**: Ultimate fallback (selalu tersedia)

### Priority:
1. Gemini (jika quota OK)
2. Groq (jika Gemini tidak tersedia)
3. Simple (jika semua API tidak tersedia)

## 🔗 Resources

- [Groq Console](https://console.groq.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [Groq Models](https://console.groq.com/docs/models)
- [Get API Key](https://console.groq.com/keys)

## ✅ Status

Setelah setup Groq:
- ✅ Aplikasi akan otomatis menggunakan Groq jika Gemini tidak tersedia
- ✅ Tidak perlu konfigurasi tambahan
- ✅ Fallback chain: Gemini → Groq → Simple

## 🎯 Quick Start

```bash
# 1. Dapatkan API key di https://console.groq.com/
# 2. Update .env
GROQ_API_KEY=your_api_key_here

# 3. Install Groq library
pip install groq

# 4. Restart server
python start_server.py
```

Selesai! Aplikasi akan otomatis menggunakan Groq sebagai fallback.

