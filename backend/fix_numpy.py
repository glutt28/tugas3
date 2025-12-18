"""
Quick script to fix NumPy version issue
Run this if you see NumPy 2.x compatibility errors
"""
import subprocess
import sys

def fix_numpy():
    print("Fixing NumPy version...")
    print("Installing NumPy < 2.0.0...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "numpy<2.0.0", "--upgrade"
        ])
        print("✓ NumPy downgraded successfully")
        print("You can now run: python start_server.py")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install NumPy: {e}")
        print("\nTry manually:")
        print("  pip install 'numpy<2.0.0'")

if __name__ == "__main__":
    fix_numpy()

