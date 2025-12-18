# 🔧 Perbaikan Cepat: Kesalahan Kata Sandi Database

## Problem
Error: `fe_sendauth: no password supplied`

Ini terjadi karena password PostgreSQL tidak terisi saat setup.

## ✅ Perbaikan Cepat

### Opsi 1: Gunakan Script Fix (Direkomendasikan)

```bash
cd backend
venv\Scripts\activate
python fix_env.py
```

Script akan:
- Detect bahwa password missing
- Meminta password baru
- Update file `.env` dengan benar

### Option 2: Edit Manual File .env

1. Buka file `backend/.env`
2. Cari baris `DATABASE_URL=`
3. Pastikan formatnya:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer
   ```

**Contoh yang BENAR:**
```env
DATABASE_URL=postgresql://postgres:12345678@localhost:5432/review_analyzer
```

**Contoh yang SALAH (tidak ada password):**
```env
DATABASE_URL=postgresql://postgres:@localhost:5432/review_analyzer
```

### Option 3: Setup Ulang

```bash
cd backend
venv\Scripts\activate

# Hapus .env yang lama (opsional)
del .env

# Setup ulang
python setup_db.py
```

**Pastikan saat diminta password, Anda memasukkan password PostgreSQL yang benar!**

## 🔍 Verifikasi

Setelah fix, test koneksi:

```bash
python start_server.py
```

Harus muncul:
```
✓ Database connection successful
```

Jika masih error, pastikan:
1. PostgreSQL running
2. Password di `.env` benar
3. Database `review_analyzer` sudah dibuat

## 💡 Tips

- Jika PostgreSQL tidak pakai password, gunakan format:
  ```env
  DATABASE_URL=postgresql://postgres@localhost:5432/review_analyzer
  ```
  (tanpa `:` setelah username)

- Untuk test password, coba login manual:
  ```bash
  psql -U postgres -h localhost
  ```

