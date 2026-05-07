# Responsável por rodar o programa via terminal, interpretar argumentos (argparse), aplicar cores (colorama) e chamar funções dos módulos.


import argparse
from pathlib import Path
try:
    from core.scanner import scan_ports
    from core.utils import save_results
    from core.services import grab_banner
except ModuleNotFoundError:
    from portscanner.core.scanner import scan_ports
    from portscanner.core.utils import save_results
    from portscanner.core.services import grab_banner
from colorama import Fore, Style, init

DEFAULT_OUTPUT = Path(__file__).resolve().parent / \
    "results" / "resultado_scan.txt"


def main():
    init(autoreset=True)

    parser = argparse.ArgumentParser(
        description="Mini Port Scanner - básico e bem feito")
    parser.add_argument("-i", "--ip", required=True,
                        help="IP ou hostname alvo (ex: 127.0.0.1)")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Intervalo de portas (ex: 20-80). Padrão: 1-1024")
    parser.add_argument("-t", "--timeout", type=int, default=1,
                        help="Timeout em segundos (padrão: 1)")
    parser.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT),
                        help="Arquivo para salvar resultado")
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))

    print(Fore.CYAN +
          f"Escaneando {args.ip} de {start_port} até {end_port}...\n")
    ports = scan_ports(args.ip, start_port, end_port, timeout=args.timeout)

    if ports:
        print(Fore.GREEN + "Portas abertas encontradas:")
        resultados = []
        for p in ports:
            banner = grab_banner(args.ip, p)
            print(Fore.GREEN + f" - Porta {p} | {banner}")
            resultados.append(f"{p} | {banner}")
        save_results(args.ip, resultados, args.output)
        print(Fore.YELLOW + f"\nResultado salvo em {args.output}")
    else:
        print(Fore.RED + "Nenhuma porta aberta encontrada.")


if __name__ == "__main__":
    main()
