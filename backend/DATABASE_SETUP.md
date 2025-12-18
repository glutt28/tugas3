# 📊 Panduan Konfigurasi Database

Panduan lengkap untuk setup database PostgreSQL untuk Product Review Analyzer.

## 📋 Prerequisites

1. **PostgreSQL terinstall** di sistem Anda
2. **PostgreSQL service running**
3. **Akses ke PostgreSQL** (username dan password)

## 🚀 Cara 1: Setup Otomatis (Recommended)

Gunakan script helper yang sudah disediakan:

```bash
cd backend
venv\Scripts\activate  # Windows
python setup_db.py
```

Script akan meminta:
- PostgreSQL username (default: `postgres`)
- PostgreSQL password
- Host (default: `localhost`)
- Port (default: `5432`)
- Database name (default: `review_analyzer`)
- Gemini API Key (opsional)

File `.env` akan dibuat otomatis dengan konfigurasi yang benar.

## 🛠️ Cara 2: Setup Manual

### Langkah 1: Buat Database

Buka PostgreSQL (psql, pgAdmin, atau DBeaver) dan jalankan:

```sql
-- Buat database baru
CREATE DATABASE review_analyzer;

-- Verifikasi database dibuat
\l
```

### Langkah 2: Buat File .env

Buat file `.env` di folder `backend` dengan isi:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer
GEMINI_API_KEY=your_gemini_api_key_here
```

**Ganti:**
- `username` → Username PostgreSQL Anda (biasanya `postgres`)
- `password` → Password PostgreSQL Anda
- `localhost` → Host PostgreSQL (jika berbeda)
- `5432` → Port PostgreSQL (jika berbeda)
- `review_analyzer` → Nama database (jika berbeda)

### Contoh Konfigurasi:

#### Default PostgreSQL Installation:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/review_analyzer
GEMINI_API_KEY=your_api_key_here
```

#### Dengan Password Kustom:
```env
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/review_analyzer
GEMINI_API_KEY=your_api_key_here
```

#### Remote Database:
```env
DATABASE_URL=postgresql://user:pass@192.168.1.100:5432/review_analyzer
GEMINI_API_KEY=your_api_key_here
```

## 🔍 Format DATABASE_URL

Format lengkap:
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Komponen:**
- `postgresql://` - Protocol (bisa juga `postgresql+psycopg2://`)
- `[user]` - Username PostgreSQL
- `[password]` - Password PostgreSQL
- `[host]` - Hostname atau IP (localhost, 127.0.0.1, atau IP remote)
- `[port]` - Port PostgreSQL (default: 5432)
- `[database]` - Nama database

## ✅ Verifikasi Konfigurasi

### Tes 1: Periksa File .env

Pastikan file `.env` ada di folder `backend`:

```bash
cd backend
dir .env  # Windows
# atau
ls .env   # Linux/Mac
```

### Test 2: Test Koneksi Database

Jalankan script test:

```bash
python -c "from database import engine; engine.connect(); print('✓ Database connected!')"
```

Atau gunakan start_server.py yang akan check otomatis:

```bash
python start_server.py
```

Jika berhasil, akan muncul:
```
✓ Database connection successful
```

Jika gagal, akan muncul error dengan detail masalahnya.

## 🐛 Troubleshooting

### Kesalahan: "password authentication failed"

**Penyebab:** Username atau password salah

**Solusi:**
1. Pastikan username dan password di `.env` benar
2. Test login ke PostgreSQL dengan kredensial yang sama:
   ```bash
   psql -U postgres -h localhost
   ```
3. Jika lupa password, reset password PostgreSQL

### Kesalahan: "database does not exist"

**Penyebab:** Database belum dibuat

**Solusi:**
```sql
CREATE DATABASE review_analyzer;
```

### Kesalahan: "connection refused" atau "could not connect"

**Penyebab:** PostgreSQL service tidak running

**Solusi:**

**Windows:**
```powershell
# Periksa status layanan
Get-Service postgresql*

# Start service
Start-Service postgresql-x64-14  # Ganti dengan versi Anda
```

**Linux/Mac:**
```bash
# Periksa status
sudo systemctl status postgresql

# Start service
sudo systemctl start postgresql
```

### Kesalahan: "connection timeout"

**Penyebab:** 
- Firewall blocking
- PostgreSQL tidak listen di port yang benar
- Host/IP salah

**Solusi:**
1. Check firewall settings
2. Verify PostgreSQL listening port:
   ```bash
   # Windows
   netstat -an | findstr 5432
   
   # Linux/Mac
   netstat -an | grep 5432
   ```
3. Check `postgresql.conf` untuk `listen_addresses`

### Kesalahan: "role does not exist"

**Penyebab:** Username PostgreSQL tidak ada

**Solusi:**
```sql
-- List semua users
\du

-- Buat user baru jika perlu
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE review_analyzer TO your_username;
```

## 🔐 Security Best Practices

1. **Jangan commit file `.env`** ke Git (sudah ada di `.gitignore`)
2. **Gunakan password yang kuat** untuk production
3. **Limit database permissions** - jangan gunakan superuser untuk aplikasi
4. **Gunakan SSL** untuk remote connections:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
   ```

## 📝 Checklist Setup Database

- [ ] PostgreSQL terinstall dan running
- [ ] Database `review_analyzer` sudah dibuat
- [ ] File `.env` ada di folder `backend`
- [ ] `DATABASE_URL` di `.env` sudah dikonfigurasi dengan benar
- [ ] Test koneksi berhasil (dengan `start_server.py`)
- [ ] Tables otomatis terbuat saat pertama kali run

## 🎯 Quick Start Commands

```bash
# 1. Masuk ke folder backend
cd backend

# 2. Aktifkan virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Setup database (otomatis)
python setup_db.py

# 4. Atau buat database manual di PostgreSQL
# CREATE DATABASE review_analyzer;

# 5. Test koneksi
python start_server.py

# 6. Jika semua OK, server akan start di http://localhost:8000
```

## 💡 Tips

1. **Gunakan pgAdmin** atau DBeaver untuk visual database management
2. **Backup database** secara berkala
3. **Monitor database size** jika banyak review
4. **Index columns** yang sering di-query untuk performa lebih baik

## 📚 Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Connection Strings](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

## ❓ Masih Ada Masalah?

1. Check log error di terminal untuk detail
2. Verify PostgreSQL logs untuk connection attempts
3. Test koneksi dengan `psql` command line tool
4. Pastikan semua prerequisites terpenuhi

