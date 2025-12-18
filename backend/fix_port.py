"""
Script to find and kill process using port 8000
"""
import subprocess
import sys
import os

def find_process_on_port(port=8000):
    """Find process using specified port on Windows"""
    try:
        # Gunakan netstat untuk menemukan proses
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        lines = result.stdout.split('\n')
        processes = []
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    processes.append(pid)
        
        return list(set(processes))  # Remove duplicates
    except Exception as e:
        print(f"Error finding process: {e}")
        return []

def kill_process(pid):
    """Kill process by PID on Windows"""
    try:
        subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"Error killing process: {e}")
        return False

def main():
    port = 8000
    print(f"Finding processes using port {port}...")
    print("=" * 50)
    
    pids = find_process_on_port(port)
    
    if not pids:
        print(f"✓ No process found using port {port}")
        print("You can start the server now!")
        return
    
    print(f"Found {len(pids)} process(es) using port {port}:")
    for pid in pids:
        print(f"  PID: {pid}")
    
    print()
    response = input("Kill these processes? (y/n) [y]: ").strip().lower()
    
    if response == '' or response == 'y':
        print("\nKilling processes...")
        for pid in pids:
            print(f"  Killing PID {pid}...", end=" ")
            if kill_process(pid):
                print("✓ Done")
            else:
                print("✗ Failed")
        
        print("\n✓ All processes killed")
        print("You can now start the server with: python start_server.py")
    else:
        print("\nProcesses not killed.")
        print("You can:")
        print("1. Manually kill processes using Task Manager")
        print("2. Use different port (edit start_server.py)")
        print("3. Find and stop the other server instance")

if __name__ == "__main__":
    main()

