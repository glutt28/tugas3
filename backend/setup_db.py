"""
Script to help setup database connection
"""
import os
from dotenv import load_dotenv

load_dotenv()

def setup_env_file():
    """Create or update .env file with database configuration"""
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"✓ {env_file} already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'DATABASE_URL' in content:
                print("  DATABASE_URL is already configured")
                return
    else:
        print(f"Creating {env_file} file...")
    
    print("\nDatabase Configuration:")
    print("=" * 50)
    
    username = input("PostgreSQL username [postgres]: ").strip() or "postgres"
    
    # Dapatkan password dengan konfirmasi
    while True:
        password = input("PostgreSQL password: ").strip()
        if not password:
            use_no_password = input("No password? Some PostgreSQL setups don't require password. Use empty password? (y/n) [n]: ").strip().lower()
            if use_no_password == 'y':
                break
            else:
                print("Password is required. Please enter password.")
                continue
        break
    
    host = input("PostgreSQL host [localhost]: ").strip() or "localhost"
    port = input("PostgreSQL port [5432]: ").strip() or "5432"
    database = input("Database name [review_analyzer]: ").strip() or "review_analyzer"
    
    # Bangun DATABASE_URL - tangani password kosong
    if password:
        database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    else:
        database_url = f"postgresql://{username}@{host}:{port}/{database}"
    
    gemini_key = input("\nGemini API Key (optional, press Enter to skip): ").strip()
    groq_key = input("Groq API Key (optional, press Enter to skip): ").strip()
    
    with open(env_file, 'w') as f:
        f.write(f"DATABASE_URL={database_url}\n")
        if gemini_key:
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
        else:
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
        if groq_key:
            f.write(f"GROQ_API_KEY={groq_key}\n")
        else:
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
    
    print(f"\n✓ {env_file} created successfully!")
    print(f"\nDATABASE_URL: {database_url}")
    print("\nNext steps:")
    print("1. Make sure PostgreSQL is running")
    print(f"2. Create database: CREATE DATABASE {database};")
    print("3. Run: python start_server.py")

if __name__ == "__main__":
    setup_env_file()

