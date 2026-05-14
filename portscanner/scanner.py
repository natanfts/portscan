# Responsavel por rodar o programa via terminal, interpretar argumentos e chamar os modulos.

import argparse
import importlib
from pathlib import Path

from colorama import Fore, init

try:
    from core.scanner import scan_port
    from core.utils import append_scan_history, build_report_data, load_scan_history, save_results
    from core.services import identify_service
    from core.analysis import analyze_port
except ModuleNotFoundError:
    from portscanner.core.scanner import scan_port
    from portscanner.core.utils import append_scan_history, build_report_data, load_scan_history, save_results
    from portscanner.core.services import identify_service
    from portscanner.core.analysis import analyze_port


def _load_tqdm():
    try:
        return importlib.import_module("tqdm").tqdm
    except ModuleNotFoundError:
        return lambda iterable, desc=None: iterable


tqdm = _load_tqdm()

DEFAULT_OUTPUT = Path(__file__).resolve().parent / \
    "results" / "resultado_scan.txt"
DEFAULT_JSON_OUTPUT = Path(__file__).resolve().parent / \
    "results" / "resultado_scan.json"
DEFAULT_HISTORY_OUTPUT = Path(__file__).resolve().parent / \
    "results" / "historico_scans.json"
FAST_PORTS = [22, 80, 443, 3306, 21, 25, 53]


def show_menu():
    print(Fore.CYAN + "=== Port Scanner ===")
    print("1 - Scan rapido (portas comuns)")
    print("2 - Scan completo (1-65535)")
    print("3 - Scan personalizado (definir intervalo)")
    choice = input("Escolha uma opcao: ")
    return choice


def choose_report_format():
    print(Fore.CYAN + "\n=== Formato do Relatorio ===")
    print("1 - Salvar em TXT")
    print("2 - Salvar em JSON")
    print("3 - Mostrar na tela e salvar em ambos")
    choice = input("Escolha uma opcao: ")
    return choice


def resolve_scan_type(choice, fast_mode):
    if fast_mode or choice == "1":
        return "fast"
    if choice == "2":
        return "full"
    if choice == "3":
        return "custom"
    return "unknown"


def print_report(report_data):
    print(Fore.CYAN + "\n=== Resultados do Port Scanner ===")
    open_ports = [item["port"] for item in report_data["open_ports"]]
    print(f"Data/Hora: {report_data['timestamp']}")
    print(f"Alvo: {report_data['target']}")
    print(f"Portas abertas: {open_ports}\n")

    print("Tabela:")
    print(f"{'Porta':<6} | {'Servico':<10} | {'Analise':<52} | Status")
    print("-" * 95)

    if report_data["open_ports"]:
        for port_data in report_data["open_ports"]:
            status_color = Fore.GREEN
            if port_data["tone"] == "risk":
                status_color = Fore.RED
            elif port_data["tone"] == "attention":
                status_color = Fore.YELLOW

            status_text = f"{port_data['icon']} {port_data['label']}"
            row = (
                f"{port_data['port']:<6} | {port_data['service']:<10} | "
                f"{port_data['analysis']:<52} | "
            )
            print(row + status_color + status_text)
    else:
        print(Fore.YELLOW + "Nenhuma porta aberta encontrada.")


def print_scan_history(history_data):
    print("\nHistorico de Scans:")
    print(f"{'Data/Hora':<19} | {'Alvo':<13} | Portas abertas")
    print("-" * 70)

    if not history_data:
        print("Nenhum scan registrado.")
        return

    for item in history_data:
        print(
            f"{item['timestamp']:<19} | {item['target']:<13} | {item['open_ports']}")


def parse_port_range(port_range):
    try:
        start, end = map(int, port_range.split("-"))
    except (AttributeError, ValueError) as exc:
        raise ValueError(
            "Intervalo invalido. Use o formato inicio-fim (ex: 20-80).") from exc

    if start < 1 or end > 65535 or start > end:
        raise ValueError(
            "Intervalo invalido. Use portas entre 1 e 65535 com inicio <= fim.")

    return start, end


def resolve_ports_to_scan(choice, ports_arg, fast_mode):
    if fast_mode or choice == "1":
        return FAST_PORTS
    if choice == "2":
        return range(1, 65536)
    if choice == "3":
        if not ports_arg:
            raise ValueError("Para scan personalizado, informe -p inicio-fim.")
        start, end = parse_port_range(ports_arg)
        return range(start, end + 1)
    raise ValueError("Opcao invalida.")


def main():
    init(autoreset=True)
    parser = argparse.ArgumentParser(description="Port Scanner Profissional")
    parser.add_argument("-i", "--ip", required=True,
                        help="IP ou hostname alvo")
    parser.add_argument(
        "-p", "--ports", help="Intervalo de portas (ex: 20-80)")
    parser.add_argument("--fast", action="store_true",
                        help="Scan rapido (portas comuns)")
    args = parser.parse_args()

    choice = "1" if args.fast else show_menu()

    try:
        ports_to_scan = resolve_ports_to_scan(choice, args.ports, args.fast)
    except ValueError as exc:
        print(Fore.RED + str(exc))
        return

    report_format = choose_report_format()
    if report_format not in {"1", "2", "3"}:
        print(Fore.RED + "Formato de relatorio invalido.")
        return

    print(Fore.YELLOW + f"\nEscaneando {args.ip}...\n")
    open_ports = []
    for port in tqdm(ports_to_scan, desc="Progresso"):
        if scan_port(args.ip, port):
            service = identify_service(port)
            print(Fore.GREEN + f"Porta {port} aberta - {service}")
            open_ports.append(port)

    report_data = build_report_data(
        args.ip,
        open_ports,
        resolve_scan_type(choice, args.fast),
    )

    saved_files = save_results(
        report_data,
        report_format,
        DEFAULT_OUTPUT,
        DEFAULT_JSON_OUTPUT,
    )
    append_scan_history(report_data, DEFAULT_HISTORY_OUTPUT)

    print(Fore.CYAN + "Relatorio salvo em: " + ", ".join(str(path)
          for path in saved_files))
    print(Fore.CYAN + f"Historico atualizado em: {DEFAULT_HISTORY_OUTPUT}")

    if report_format == "3":
        print_report(report_data)
        history_data = load_scan_history(DEFAULT_HISTORY_OUTPUT)
        print_scan_history(history_data[-5:])


if __name__ == "__main__":
    main()
