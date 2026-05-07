# Funções auxiliares (salvar resultados).

import os


def save_results(target_ip, ports, filename="results/resultado_scan.txt"):
    output_dir = os.path.dirname(filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(filename, "w") as f:
        f.write(f"Portas abertas em {target_ip}:\n")
        for p in ports:
            f.write(f"{p}\n")
