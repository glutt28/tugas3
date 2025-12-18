# 🔌 Perbaiki Kesalahan: Port 8000 Sudah Digunakan

## Problem
Error: `[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): only one usage of each socket address (protocol/network address/port) is normally permitted`

Ini berarti port 8000 sudah digunakan oleh proses lain (kemungkinan instance server yang masih running).

## ✅ Perbaikan Cepat

### Option 1: Kill Process dengan Script (Recommended)

```bash
cd backend
venv\Scripts\activate
python fix_port.py
```

Script akan:
- Mencari proses yang menggunakan port 8000
- Menawarkan untuk kill proses tersebut
- Setelah itu, server bisa start

### Option 2: Kill Process Manual

**Windows PowerShell:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (ganti PID dengan angka dari command di atas)
taskkill /F /PID <PID>
```

**Contoh:**
```powershell
# Step 1: Find PID
netstat -ano | findstr :8000
# Output: TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING    12345

# Step 2: Kill process (PID = 12345)
taskkill /F /PID 12345
```

### Option 3: Gunakan Port Lain

Server sudah otomatis coba port 8001 jika 8000 tidak tersedia.

Atau edit `start_server.py` untuk menggunakan port lain:

```python
uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
```

**Jangan lupa update frontend** jika ganti port:
- Edit `frontend/vite.config.js`:
  ```js
  proxy: {
    '/api': {
      target: 'http://localhost:8001',  // Ganti 8000 ke 8001
      changeOrigin: true,
    }
  }
  ```

### Option 4: Task Manager

1. Buka **Task Manager** (Ctrl+Shift+Esc)
2. Tab **Details**
3. Cari proses Python yang menggunakan port 8000
4. Klik kanan → **End Task**

## 🔍 Periksa Status Port

```powershell
# Periksa apa yang menggunakan port 8000
netstat -ano | findstr :8000

# Periksa semua port yang mendengarkan
netstat -ano | findstr LISTENING
```

## ✅ Verifikasi

Setelah kill process, start server lagi:

```bash
python start_server.py
```

Harus muncul:
```
Starting server on http://localhost:8000
```

Tanpa error port!

## 💡 Tips

1. **Selalu stop server dengan CTRL+C** sebelum start lagi
2. **Check apakah ada terminal lain** yang masih running server
3. **Gunakan script fix_port.py** untuk otomatis kill process

## 🚀 Quick Commands

```bash
# Perbaiki masalah port
python fix_port.py

# Start server
python start_server.py
```

