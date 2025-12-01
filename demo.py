import nmap
import sys # Import sys for better error handling

TARGET_HOST = " 10.37.0.1"


OPTIONS = "-sV -sC -T4"

# Define a short range of ports for a quick test
TARGET_PORTS = '20-100'
try:
    # Initialize the PortScanner object
    nm = nmap.PortScanner()

    print(f"[+] Starting scan on {TARGET_HOST} for ports {TARGET_PORTS} with arguments: {OPTIONS}")
    

    nm.scan(TARGET_HOST, TARGET_PORTS, arguments=OPTIONS)

    if not nm.all_hosts():
        print("-" * 50)
        print(f"[!] Scan returned NO HOSTS. Check if {TARGET_HOST} is online or if your firewall is blocking Nmap.")
        print("-" * 50)
        sys.exit(1) # Exit if no host is found
    
    # --- Print Results ---
    print("\n" + "=" * 60)
    print(f"SCAN RESULTS FOR: {TARGET_HOST}")
    print("=" * 60)
    
    # Use the existing iteration loop, but with f-string formatting (modern Python)
    for host in nm.all_hosts():
        # Host information
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        print("-" * 60)
        
        # Protocol and Port information
        for protocol in nm[host].all_protocols():
            print(f"Protocol: {protocol.upper()}")
            port_info = nm[host][protocol]
            
            # Use sorted() to print ports in order
            for port in sorted(port_info.keys(), key=int): 
                state = port_info[port]['state']
                name = port_info[port]['name']
                product = port_info[port]['product']
                
                print(f"  Port: {port}/{protocol.lower()}\t| State: {state.upper()}\t| Service: {name} ({product})")
        
    print("=" * 60)

except nmap.PortScannerError as e:
    # Catches permission errors (like needing root/admin for -sS scan)
    print(f"\n[CRITICAL ERROR] Nmap Scan Failed: {e}")
    print("[HINT] On Windows/Linux, certain scan types (-sS) require Administrator/root privileges.")
    print("[HINT] Try running your terminal as Administrator, or change OPTIONS to '-sT' (TCP Connect Scan).")
except Exception as e:
    print(f"\n[FATAL ERROR] An unexpected error occurred: {e}")

print("\n[+] Script execution complete.")
