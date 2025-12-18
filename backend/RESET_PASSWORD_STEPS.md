# 🔐 Reset Password PostgreSQL - Step by Step

## ✅ Anda Sudah Masuk ke psql!

Sekarang jalankan command berikut di dalam psql:

## 📝 Command yang Perlu Dijalankan

### Di dalam psql (setelah `postgres=#`), ketik:

```sql
ALTER USER postgres WITH PASSWORD '12345678';
```

**Ganti `12345678` dengan password yang Anda inginkan!**

### Setelah itu, ketik:

```sql
\q
```

Untuk keluar dari psql.

## 🔄 Langkah Lengkap

1. **Di psql prompt (`postgres=#`), ketik:**
   ```sql
   ALTER USER postgres WITH PASSWORD '12345678';
   ```
   
   Harus muncul: `ALTER ROLE`

2. **Keluar dari psql:**
   ```sql
   \q
   ```

3. **Update file `.env` di folder `backend`:**
   ```env
   DATABASE_URL=postgresql://postgres:12345678@localhost:5432/review_analyzer
   ```
   
   (Ganti `12345678` dengan password yang baru saja di-set)

4. **Test koneksi:**
   ```bash
   python start_server.py
   ```

## ⚠️ Catatan Penting

- **Password harus dalam tanda kutip tunggal** (`'password'`)
- **Jangan lupa titik koma** di akhir (`;`)
- **Setelah ALTER USER, harus muncul** `ALTER ROLE` sebagai konfirmasi
- **Password case-sensitive** - pastikan konsisten

## 🎯 Quick Copy-Paste

Jika ingin password `12345678`, copy-paste ini di psql:

```sql
ALTER USER postgres WITH PASSWORD '12345678';
\q
```

Kemudian update `.env` dengan password yang sama!

