import sys
import socket
from datetime import datetime
import threading

def scan_port(target,port): # Function to scan a port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target,port)) # Error indicator
        if result == 0:
            print(f"Port {port} is open.")
        s.close()

    except socket.error as e:
        print(f"ERROR: Socket error on port {port}: {e}.") # Error handling
    except Exception as e:
        print(f"ERROR: Unexpected error on port {port}: {e}.") # Error handling


# Main function - argument validation and target definition
def main(): 

    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        print("ERROR: Invalid number of arguments.")
        print("Usage: python scanner.py <TARGET>")
        sys.exit(1)

    # Resolve target hostname
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"ERROR: Unable to resolve hostname {target}.")
        sys.exit(1)

    print("-" * 50)
    print(f"Scanning target {target_ip}...")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    try:
        # Use multithreading to scan ports concurrently
        threads = []
        for port in range(1,65536):
            thread = threading.Thread(target=scan_port, args=(target_ip, port))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit(0)

    except socket.error as e:
        print(f"Socket Error: {e}")
        sys.exit(1)

    print("\nScan complete!")

if __name__ == "__main__":
    main()