"""
Quick script to fix .env file, especially for password issues
"""
import os
import re

def fix_env_file():
    """Fix .env file, especially DATABASE_URL"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"✗ {env_file} not found. Run setup_db.py first.")
        return
    
    print(f"Reading {env_file}...")
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Periksa DATABASE_URL saat ini
    match = re.search(r'DATABASE_URL=(.+)', content)
    if match:
        current_url = match.group(1).strip()
        print(f"Current DATABASE_URL: {current_url}")
        
        # Periksa apakah password hilang
        if '://' in current_url:
            parts = current_url.split('://', 1)
            if len(parts) == 2:
                auth_part = parts[1].split('@')[0] if '@' in parts[1] else ''
                if ':' not in auth_part or auth_part.endswith(':'):
                    print("\n⚠ Password appears to be missing in DATABASE_URL")
                    print("\nLet's fix it:")
                    
                    username = input("PostgreSQL username [postgres]: ").strip() or "postgres"
                    password = input("PostgreSQL password: ").strip()
                    
                    if not password:
                        use_no_password = input("No password? Use empty password? (y/n) [n]: ").strip().lower()
                        if use_no_password != 'y':
                            print("Password is required. Exiting.")
                            return
                    
                    # Extract host, port, database from current URL
                    url_parts = current_url.split('@')
                    if len(url_parts) == 2:
                        rest = url_parts[1]
                    else:
                        # Coba ekstrak dari format tanpa @
                        rest = current_url.split('://')[1] if '://' in current_url else current_url
                        host = input("PostgreSQL host [localhost]: ").strip() or "localhost"
                        port = input("PostgreSQL port [5432]: ").strip() or "5432"
                        database = input("Database name [review_analyzer]: ").strip() or "review_analyzer"
                        rest = f"{host}:{port}/{database}"
                    
                    # Build new URL
                    if password:
                        new_url = f"postgresql://{username}:{password}@{rest}"
                    else:
                        new_url = f"postgresql://{username}@{rest}"
                    
                    # Replace in content
                    content = re.sub(
                        r'DATABASE_URL=.*',
                        f'DATABASE_URL={new_url}',
                        content
                    )
                    
                    # Write back
                    with open(env_file, 'w') as f:
                        f.write(content)
                    
                    print(f"\n✓ {env_file} updated!")
                    print(f"New DATABASE_URL: {new_url}")
                else:
                    print("✓ DATABASE_URL looks correct")
    else:
        print("✗ DATABASE_URL not found in .env file")
        print("Run setup_db.py to create it.")

if __name__ == "__main__":
    fix_env_file()

