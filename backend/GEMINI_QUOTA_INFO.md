# 📊 Gemini API Quota Information

## ⚠️ Kuota Terlampaui

Jika Anda mendapat error `429 Quota exceeded`, ini berarti Anda telah mencapai batas quota harian untuk Gemini API.

## 📈 Free Tier Limits

**Gemini API Free Tier:**
- **20 requests per day** per model
- Reset setiap 24 jam
- Per model (gemini-2.5-flash, gemini-2.5-pro, dll memiliki limit terpisah)

## ✅ Solution Implemented

Aplikasi sudah diupdate untuk:
- **Otomatis fallback** ke simple extraction jika quota habis
- **Tetap berfungsi** meskipun quota exceeded
- **Tidak crash** atau return error

## 🔄 Behavior

### Saat Quota Habis:
1. Aplikasi akan mencoba model pertama (gemini-2.5-flash)
2. Jika quota exceeded, langsung fallback ke simple extraction
3. Tidak akan mencoba model lain (karena kemungkinan quota habis juga)
4. Aplikasi tetap berfungsi normal

### Simple Extraction:
- Menggunakan text analysis dasar
- Extract kalimat penting dari review
- Format sebagai bullet points
- **Tidak memerlukan API** - selalu tersedia

## 💡 Tips

### 1. Monitor Quota Usage
- Check usage di: https://ai.dev/usage?tab=rate-limit
- Plan penggunaan harian

### 2. Upgrade Plan (Jika Perlu)
- Free tier: 20 requests/day
- Paid plan: Higher limits
- Check: https://ai.google.dev/pricing

### 3. Optimize Usage
- Simple extraction sudah cukup untuk kebanyakan use case
- Gunakan Gemini hanya untuk review yang kompleks
- Cache results jika memungkinkan

### 4. Wait for Reset
- Quota reset setiap 24 jam
- Check kapan quota akan reset
- Retry setelah reset

## 🎯 Current Status

**Aplikasi akan:**
- ✅ Tetap berfungsi dengan simple extraction
- ✅ Tidak crash atau error
- ✅ Memberikan hasil yang berguna
- ⚠️ Menggunakan Gemini jika quota tersedia

## 📝 Contoh

**Dengan Gemini (jika quota tersedia):**
```
• Excellent product quality and fast shipping
• Great value for money
• Highly recommend to others
```

**Dengan Simple Extraction (fallback):**
```
• This product is amazing! Great quality and fast shipping.
• Highly recommend!
• Great value for money.
```

Kedua hasil tetap berguna, meskipun Gemini memberikan hasil yang lebih terstruktur.

## 🔗 Resources

- [Gemini API Quota Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Check Usage](https://ai.dev/usage?tab=rate-limit)
- [Pricing](https://ai.google.dev/pricing)

## ✅ No Action Required

Aplikasi sudah handle quota exceeded dengan baik. Tidak perlu konfigurasi tambahan - aplikasi akan otomatis menggunakan simple extraction saat quota habis.

