# 🔐 Reset PostgreSQL Password

Jika password PostgreSQL tidak sesuai, berikut cara resetnya.

## 🚀 Cara 1: Test Password dengan Script

Pertama, coba test koneksi untuk menemukan password yang benar:

```bash
cd backend
venv\Scripts\activate
python test_db_connection.py
```

Script ini akan:
- Test password yang ada di .env
- Coba password umum (postgres, admin, 123456, dll)
- Beri tahu password yang benar jika ditemukan

## 🛠️ Cara 2: Reset Password via psql

### Step 1: Login sebagai superuser

**Windows:**
```bash
# Cari lokasi PostgreSQL bin
# Biasanya di: C:\Program Files\PostgreSQL\14\bin

# Masuk ke psql
psql -U postgres
```

Jika diminta password dan tidak tahu, coba:
- Password kosong (tekan Enter)
- `postgres`
- `admin`
- Password default saat install

### Step 2: Reset password

Setelah masuk ke psql, jalankan:

```sql
ALTER USER postgres WITH PASSWORD 'password_baru_anda';
```

Contoh:
```sql
ALTER USER postgres WITH PASSWORD '12345678';
```

### Step 3: Update .env

Update file `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:password_baru_anda@localhost:5432/review_analyzer
```

## 🔧 Cara 3: Reset via pgAdmin

1. Buka **pgAdmin**
2. Connect ke PostgreSQL server
3. Klik kanan pada **Login/Group Roles** → **postgres**
4. Pilih **Properties**
5. Tab **Definition**
6. Masukkan password baru di field **Password**
7. Klik **Save**

## 🔍 Cara 4: Cek Password Saat Install

Jika baru install PostgreSQL:
- Password biasanya di-set saat install
- Cek dokumentasi install atau catatan Anda
- Atau coba password default: `postgres`, `admin`, atau kosong

## 🧪 Cara 5: Test Manual

Test koneksi manual untuk verifikasi password:

```bash
# Test dengan password tertentu
psql -U postgres -h localhost -d postgres
# Akan prompt password - coba masukkan password
```

## 📝 Update .env Setelah Reset

Setelah reset password, update file `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:password_baru@localhost:5432/review_analyzer
GEMINI_API_KEY=your_api_key_here
```

**Ganti `password_baru` dengan password yang baru saja di-set!**

## ✅ Verifikasi

Setelah update .env, test koneksi:

```bash
python start_server.py
```

Harus muncul:
```
✓ Database connection successful
```

## 🆘 Masih Tidak Bisa?

### Option 1: Buat User Baru

```sql
-- Login sebagai superuser
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE review_analyzer OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE review_analyzer TO myuser;
```

Kemudian update .env:
```env
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/review_analyzer
```

### Option 2: Gunakan Trust Authentication (Development Only)

**⚠️ Hanya untuk development, jangan di production!**

Edit file `pg_hba.conf` (biasanya di `C:\Program Files\PostgreSQL\14\data\`):

Ubah dari:
```
host    all             all             127.0.0.1/32            md5
```

Menjadi:
```
host    all             all             127.0.0.1/32            trust
```

Restart PostgreSQL service setelah perubahan.

## 💡 Tips

1. **Simpan password** di tempat aman setelah reset
2. **Jangan commit .env** ke Git (sudah di .gitignore)
3. **Gunakan password kuat** untuk production
4. **Test koneksi** setelah setiap perubahan

## 🔗 Quick Commands

```bash
# Test koneksi
python test_db_connection.py

# Reset password (setelah login ke psql)
ALTER USER postgres WITH PASSWORD 'newpassword';

# Update .env
# Edit backend/.env dan update DATABASE_URL

# Test server
python start_server.py
```

