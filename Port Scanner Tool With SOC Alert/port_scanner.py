import socket
from concurrent.futures import ThreadPoolExecutor

target = input("Enter the target IP to scan: ")

consent = (
    input(f"Do you have explicit authorization to scan {target}? (yes/no): ")
    .strip()
    .lower()
)
if consent != "yes":
    print(
        "Scan cancelled. Only scan systems you own or have explicit written permission to test."
    )
    exit()

mode = (
    input("Scan a range or specific ports? (type 'range' or 'specific'): ")
    .strip()
    .lower()
)

if mode == "range":
    start_port = int(input("Enter start port (e.g. 1): "))
    end_port = int(input("Enter end port (e.g. 1024, max 65535): "))
    ports_to_scan = range(start_port, end_port + 1)

elif mode == "specific":
    port_list = input("Enter port numbers separated by commas (e.g. 22,80,443): ")
    ports_to_scan = [int(p.strip()) for p in port_list.split(",")]

else:
    print("Invalid choice. Please type 'range' or 'specific'.")
    exit()


def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    sock.close()

    if result == 0:
        print(f"Port {port} is OPEN")


print(f"Scanning {target} ...")

with ThreadPoolExecutor(max_workers=200) as executor:
    executor.map(scan_port, ports_to_scan)

print("Scan complete.")
