"""
Alternative server starter that handles errors gracefully
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def check_dependencies():
    """Check if all required dependencies are available"""
    # Periksa versi NumPy terlebih dahulu
    try:
        import numpy as np
        if np.__version__.startswith('2.'):
            print("⚠ Warning: NumPy 2.x detected. PyTorch requires NumPy < 2.0")
            print("  Run: pip install 'numpy<2.0.0'")
    except ImportError:
        pass
    
    try:
        import torch
        import transformers
        print("✓ PyTorch and Transformers loaded successfully")
    except ImportError as e:
        print(f"⚠ Warning: {e}")
        print("Some features may not work without these dependencies")
    except Exception as e:
        print(f"⚠ Warning loading PyTorch: {e}")
        print("  This might be a NumPy version issue. Try: pip install 'numpy<2.0.0'")
    
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            print("✓ Gemini API configured")
        else:
            print("⚠ GEMINI_API_KEY not found in .env")
    except Exception as e:
        print(f"⚠ Gemini API setup issue: {e}")
    
    # Periksa API Groq
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            print("✓ Groq API configured (fallback)")
        else:
            print("⚠ GROQ_API_KEY not found in .env - will use simple extraction if Gemini unavailable")
    except Exception as e:
        print(f"⚠ Groq API setup issue: {e}")

def check_database():
    """Check database connection"""
    try:
        from database import engine
        # Coba untuk terhubung
        with engine.connect() as conn:
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease check:")
        print("1. PostgreSQL is running")
        print("2. DATABASE_URL in .env is correct")
        print("3. Database 'review_analyzer' exists")
        print("\nYou can create the database with:")
        print("  CREATE DATABASE review_analyzer;")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Product Review Analyzer - Backend Server")
    print("=" * 50)
    print()
    
    # Periksa dependensi
    check_dependencies()
    print()
    
    # Periksa database
    db_ok = check_database()
    print()
    
    if not db_ok:
        print("⚠ Starting server anyway, but database operations will fail")
        print("  Fix the database connection and restart the server")
        print()
    
    # Coba jalankan server
    try:
        import uvicorn
        
        # Impor `main` setelah pengecekan untuk menghindari koneksi database terlalu awal
        print("Loading application...")
        from main import app
        
        print("Starting server on http://localhost:8000")
        print("API docs available at http://localhost:8000/docs")
        print("Press CTRL+C to stop")
        print("=" * 50)
        print()
        
        # Periksa apakah port tersedia, jika tidak gunakan alternatif
        import socket
        port = 8000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('0.0.0.0', port))
            sock.close()
        except OSError:
            print(f"⚠ Port {port} is already in use!")
            print(f"   Trying alternative port 8001...")
            port = 8001
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('0.0.0.0', port))
                sock.close()
            except OSError:
                print(f"✗ Port {port} also in use. Please free a port or kill the process.")
                print("\nTo kill process on port 8000, run:")
                print("  python fix_port.py")
                sys.exit(1)
        
        uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if database connection is correct in .env file")
        print("2. Make sure PostgreSQL is running")
        print("3. Try: pip install 'numpy<2.0.0' if you see NumPy errors")
        sys.exit(1)

