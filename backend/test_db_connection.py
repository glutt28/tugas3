"""
Test database connection dengan berbagai konfigurasi
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection(username, password, host="localhost", port=5432, database="postgres"):
    """Test koneksi database dengan kredensial tertentu"""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            """
            Test database connection dengan berbagai konfigurasi
            """
            import psycopg2
            import os
            from dotenv import load_dotenv

            load_dotenv()


            def test_connection(username, password, host="localhost", port=5432, database="postgres"):
                """Test koneksi database dengan kredensial tertentu"""
                try:
                    conn = psycopg2.connect(
                        host=host,
                        port=port,
                        user=username,
                        password=password,
                        database=database,
                        connect_timeout=5
                    )
                    conn.close()
                    return True, "Success"
                except psycopg2.OperationalError as e:
                    return False, str(e)
                except Exception as e:
                    return False, str(e)


            def main():
                print("=" * 60)
                print("Database Connection Tester")
                print("=" * 60)
                print()

                # Ambil konfigurasi saat ini dari .env
                db_url = os.getenv("DATABASE_URL", "")
                print(f"Current DATABASE_URL from .env:")
                if db_url:
                    # Sembunyikan password untuk ditampilkan
                    masked_url = db_url
                    if '@' in db_url and ':' in db_url.split('@')[0]:
                        parts = db_url.split('@')
                        auth = parts[0].split('://')[1] if '://' in parts[0] else parts[0]
                        if ':' in auth:
                            user, pwd = auth.split(':', 1)
                            masked_url = db_url.replace(f":{pwd}@", ":***@")
                    print(f"  {masked_url}")
                else:
                    print("  Not found in .env")
                print()

                # Parse konfigurasi saat ini
                if db_url and '://' in db_url:
                    try:
                        # Ekstrak bagian-bagian
                        url_part = db_url.split('://')[1]
                        auth_part = url_part.split('@')[0]
                        rest_part = url_part.split('@')[1] if '@' in url_part else url_part

                        if ':' in auth_part:
                            current_user, current_pass = auth_part.split(':', 1)
                        else:
                            current_user = auth_part
                            current_pass = ""

                        if ':' in rest_part:
                            host_port, current_db = rest_part.rsplit('/', 1)
                            if ':' in host_port:
                                current_host, current_port = host_port.split(':')
                            else:
                                current_host = host_port
                                current_port = "5432"
                        else:
                            current_host = "localhost"
                            current_port = "5432"
                            current_db = rest_part

                        print("Current configuration:")
                        print(f"  Username: {current_user}")
                        print(f"  Password: {'***' if current_pass else '(empty)'}")
                        print(f"  Host: {current_host}")
                        print(f"  Port: {current_port}")
                        print(f"  Database: {current_db}")
                        print()
                    except:
                        print("Could not parse DATABASE_URL")
                        current_user = "postgres"
                        current_pass = ""
                        current_host = "localhost"
                        current_port = 5432
                        current_db = "postgres"
                else:
                    current_user = "postgres"
                    current_pass = ""
                    current_host = "localhost"
                    current_port = 5432
                    current_db = "postgres"

                # Uji konfigurasi saat ini
                print("Testing current configuration...")
                success, error = test_connection(
                    current_user,
                    current_pass,
                    current_host,
                    int(current_port),
                    current_db,
                )

                if success:
                    print("✓ Connection successful!")
                    print(f"  Can connect to database '{current_db}' as user '{current_user}'")
                    return

                print(f"✗ Connection failed: {error}")
                print()

                # Coba password yang berbeda
                print("Let's try to find the correct password...")
                print()

                common_passwords = [
                    "",  # Tanpa password
                    "postgres",
                    "admin",
                    "123456",
                    "12345678",
                    "password",
                ]

                # Tambahkan password saat ini jika belum ada dalam daftar
                if current_pass and current_pass not in common_passwords:
                    common_passwords.insert(0, current_pass)

                print("Testing common passwords:")
                for pwd in common_passwords:
                    pwd_display = pwd if pwd else "(empty)"
                    print(f"  Trying password: {pwd_display}...", end=" ")
                    success, error = test_connection(
                        current_user,
                        pwd,
                        current_host,
                        int(current_port),
                        "postgres",  # Coba koneksi ke database default 'postgres' terlebih dahulu
                    )
                    if success:
                        print("✓ SUCCESS!")
                        print()
                        print("=" * 60)
                        print("Found working password!")
                        print("=" * 60)
                        print(f"Username: {current_user}")
                        print(f"Password: {pwd_display}")
                        print(f"Host: {current_host}")
                        print(f"Port: {current_port}")
                        print()
                        print("Update your .env file with:")
                        if pwd:
                            print(
                                f'DATABASE_URL=postgresql://{current_user}:{pwd}@{current_host}:{current_port}/{current_db}'
                            )
                        else:
                            print(f'DATABASE_URL=postgresql://{current_user}@{current_host}:{current_port}/{current_db}')
                        return
                    else:
                        print("✗ Failed")

                print()
                print("=" * 60)
                print("Could not find working password automatically")
                print("=" * 60)
                print()
                print("Options:")
                print("1. Reset PostgreSQL password:")
                print("   - Open pgAdmin or psql")
                print("   - Run: ALTER USER postgres WITH PASSWORD 'newpassword';")
                print()
                print("2. Use a different PostgreSQL user:")
                print("   - Create new user or use existing one")
                print("   - Update DATABASE_URL in .env")
                print()
                print("3. Test connection manually:")
                print("   psql -U postgres -h localhost")
                print("   (This will prompt for password)")
                print()
                print("4. Check if PostgreSQL uses different authentication:")
                print("   - Check pg_hba.conf file")
                print("   - May need to change authentication method")


            if __name__ == "__main__":
                main()

