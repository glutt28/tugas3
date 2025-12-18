# Troubleshooting Guide

## Frontend Issues

### Kesalahan Tailwind CSS
**Error**: `It looks like you're trying to use tailwindcss directly as a PostCSS plugin`

**Solution**: 
- Tailwind CSS v4 alpha memerlukan `@tailwindcss/postcss` sebagai plugin terpisah
- Atau gunakan Tailwind CSS v3 (lebih stabil)
- Sudah diperbaiki dengan downgrade ke Tailwind v3.4.1

### Kesalahan Impor/Ekspor
**Error**: `No matching export in "src/components/ReviewList.jsx" for import "ReviewList"`

**Solution**: 
- Pastikan komponen diekspor dengan benar
- Sudah diperbaiki dengan menambahkan named export

### Backend Issues

#### NumPy Version Conflict
**Error**: `A module that was compiled using NumPy 1.x cannot be run in NumPy 2.3.5`

**Solution**:
```bash
pip install "numpy<2"
```

#### Kesalahan Koneksi Database
**Error**: `password authentication failed for user "postgres"`

**Solution**:
1. Pastikan PostgreSQL running
2. Buat file `.env` di folder `backend`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/review_analyzer
GEMINI_API_KEY=your_api_key_here
```
3. Ganti `username` dan `password` dengan kredensial PostgreSQL Anda
4. Pastikan database `review_analyzer` sudah dibuat

## Perbaikan Cepat

### Reinstall Dependencies
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd backend
pip install -r requirements.txt
```

### Clear Cache
```bash
# Frontend
rm -rf node_modules/.vite

# Backend
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

## Common Issues

### Port Sudah Digunakan
- Frontend: Change port in `vite.config.js`
- Backend: Change port in `main.py` or use `--port` flag

### Kesalahan CORS
- Pastikan backend CORS settings di `main.py` mengizinkan origin frontend
- Default: `http://localhost:3000`

### Module Not Found
- Pastikan semua dependencies terinstall
- Restart dev server setelah install dependencies baru

