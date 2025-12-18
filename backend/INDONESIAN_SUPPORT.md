# Dukungan Bahasa Indonesia

Aplikasi ini telah dioptimalkan khusus untuk review dalam bahasa Indonesia dengan peningkatan akurasi sentiment analysis dan key points extraction.

## Fitur Peningkatan untuk Bahasa Indonesia

### 1. Sentiment Analysis yang Dioptimalkan

#### Hybrid Approach (Pendekatan Gabungan)
- **Rule-based Analysis**: Analisis berbasis aturan khusus untuk bahasa Indonesia
- **ML Model**: Menggunakan model Hugging Face sebagai pendukung
- **Smart Combination**: Menggabungkan kedua metode untuk akurasi maksimal

#### Kata Kunci Bahasa Indonesia yang Didukung

**Positif Kuat:**
- sangat bagus, sangat baik, sangat puas, sangat memuaskan
- luar biasa, sempurna, mantap banget, keren banget
- terbaik, paling bagus, sangat direkomendasikan
- worth it, sangat worth it, recommended

**Positif Sedang:**
- bagus, baik, puas, memuaskan, oke, lumayan
- keren, mantap, nice, good, great
- rekomendasi, direkomendasikan

**Negatif Kuat:**
- sangat jelek, sangat buruk, sangat kecewa
- sangat tidak puas, sangat mengecewakan
- terburuk, paling jelek, gagal total
- waste of money, buang uang, rugi

**Negatif Sedang:**
- jelek, buruk, kecewa, mengecewakan
- tidak puas, tidak memuaskan, tidak sesuai
- gagal, rusak, cacat, kurang baik

#### Deteksi Pola Negasi
Sistem dapat mendeteksi pola negasi dalam bahasa Indonesia:
- "tidak bagus" → Negatif
- "belum puas" → Negatif
- "kurang baik" → Negatif
- "bukan jelek" → Positif (negasi dari negatif)

### 2. Key Points Extraction yang Dioptimalkan

#### Deteksi Bahasa yang Ditingkatkan
- **Lebih Banyak Indikator**: 50+ kata kunci bahasa Indonesia
- **Pola Khusus**: Deteksi pola seperti "sangat bagus", "paling baik", dll.
- **Akurasi Tinggi**: Deteksi bahasa Indonesia dengan akurasi >95%

#### Kata Kunci yang Diperluas

**Kategori Positif:**
- Semua kata positif standar + variasi (sangat bagus, bagus banget, dll.)
- Ekspresi emosi (suka banget, love it, terkesan)
- Rekomendasi (direkomendasikan, worth it, highly recommend)

**Kategori Negatif:**
- Semua kata negatif standar + variasi
- Masalah spesifik (ada masalah, banyak masalah, sering masalah)
- Ekspresi kekecewaan (sangat kecewa, mengecewakan, rugi)

**Kategori Fitur:**
- Kualitas, harga, pengiriman, pelayanan
- Packaging, ukuran, warna, material
- Warranty, return, refund

#### Prompt yang Dioptimalkan
- Instruksi lebih jelas dan spesifik untuk bahasa Indonesia
- Fokus pada informasi praktis untuk pembeli potensial
- Format output yang lebih natural dan mudah dibaca

### 3. Post-Processing untuk Bahasa Indonesia

#### Pembersihan Teks
- Menghapus frasa generik yang tidak perlu
- Membatasi panjang setiap poin (maksimal 100 karakter)
- Mempertahankan format yang mudah dibaca

#### Contoh Output

**Sebelum:**
```
Berikut adalah poin-poin penting dari review ini: 
1. Produk ini sangat bagus dan kualitasnya sangat memuaskan...
```

**Sesudah:**
```
• Produk sangat bagus dengan kualitas memuaskan
• Harga sesuai dengan kualitas yang diberikan
• Pengiriman cepat dan packaging rapi
```

## Cara Kerja

### Sentiment Analysis Flow

1. **Deteksi Bahasa**: Cek apakah review dalam bahasa Indonesia
2. **Rule-based Analysis**: Analisis menggunakan aturan khusus bahasa Indonesia
3. **ML Model Analysis**: Analisis menggunakan model Hugging Face
4. **Kombinasi**: Gabungkan hasil dengan prioritas pada rule-based untuk bahasa Indonesia
5. **Hasil Akhir**: Return sentiment (positive/negative/neutral)

### Key Points Extraction Flow

1. **Deteksi Bahasa**: Cek apakah review dalam bahasa Indonesia
2. **Gemini API**: Coba ekstrak menggunakan Gemini dengan prompt bahasa Indonesia
3. **Groq API**: Fallback ke Groq jika Gemini tidak tersedia
4. **Simple Extraction**: Fallback terakhir menggunakan keyword matching
5. **Post-processing**: Bersihkan dan format output untuk bahasa Indonesia

## Testing

### Contoh Review Bahasa Indonesia

**Review Positif:**
```
Produk ini sangat bagus! Kualitasnya luar biasa dan harga sangat worth it. 
Pengiriman cepat dan packaging rapi. Sangat direkomendasikan untuk yang 
mencari produk berkualitas dengan harga terjangkau.
```

**Expected Sentiment:** `positive`

**Expected Key Points:**
- Kualitas luar biasa dengan harga worth it
- Pengiriman cepat dan packaging rapi
- Sangat direkomendasikan untuk produk berkualitas

**Review Negatif:**
```
Sangat kecewa dengan produk ini. Kualitasnya tidak sesuai dengan harga yang 
dibayar. Ada banyak masalah dan tidak direkomendasikan. Buang uang saja.
```

**Expected Sentiment:** `negative`

**Expected Key Points:**
- Kualitas tidak sesuai dengan harga
- Banyak masalah ditemukan
- Tidak direkomendasikan, waste of money

## Tips untuk Hasil Terbaik

1. **Gunakan Bahasa Natural**: Tulis review seperti berbicara sehari-hari
2. **Sebutkan Spesifik**: Sebutkan aspek spesifik (kualitas, harga, pengiriman)
3. **Gunakan Ekspresi**: Gunakan ekspresi seperti "sangat", "banget", "sekali" untuk emphasis
4. **Jelas dalam Kritik**: Jika negatif, sebutkan masalah spesifiknya

## Troubleshooting

### Sentiment Tidak Akurat

Jika sentiment tidak akurat untuk review bahasa Indonesia:
1. Pastikan review menggunakan kata kunci yang jelas (bagus, jelek, puas, kecewa)
2. Hindari bahasa campuran (campur Indonesia-Inggris) jika memungkinkan
3. Gunakan ekspresi yang jelas (sangat bagus vs bagus saja)

### Key Points Tidak Relevan

Jika key points tidak relevan:
1. Pastikan review cukup panjang (minimal 50 karakter)
2. Sebutkan aspek spesifik produk (kualitas, harga, fitur)
3. Hindari review yang terlalu singkat atau tidak jelas

## Catatan Teknis

- Rule-based sentiment analysis lebih akurat untuk bahasa Indonesia dibanding ML model
- Sistem menggunakan hybrid approach untuk akurasi maksimal
- Deteksi bahasa menggunakan 50+ indikator bahasa Indonesia
- Post-processing memastikan output ringkas dan mudah dibaca


