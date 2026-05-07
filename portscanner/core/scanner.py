#Funções de escaneamento com threading.

import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target_ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((target_ip, port))
    sock.close()
    if result == 0:
        return port
    return None

def scan_ports(target_ip, start_port=1, end_port=1024, timeout=1, max_threads=100):
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_port, target_ip, port, timeout) for port in range(start_port, end_port + 1)]
        for future in futures:
            port = future.result()
            if port:
                open_ports.append(port)
    return open_ports
