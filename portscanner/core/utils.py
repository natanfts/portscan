# Funções auxiliares (salvar resultados).

from datetime import datetime

def save_results(target_ip, ports, filename="results/resultado_scan.txt"):
    with open(filename, "w") as f:
        f.write(f"Portas abertas em {target_ip}:\n")
        for p in ports:
            f.write(f"{p}\n")

def log_monitor(ip, port, status, filename="results/monitor.log"):
    """Salva cada checagem do monitor em um arquivo .log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {ip}:{port} - {status}\n")
