# Funcoes auxiliares de persistencia de resultados.

import json
import importlib
from datetime import datetime
from pathlib import Path

try:
    from core.services import identify_service
except ModuleNotFoundError:
    from portscanner.core.services import identify_service

try:
    from core.analysis import get_port_risk
except ModuleNotFoundError:
    from portscanner.core.analysis import get_port_risk


def _load_analyze_port():
    module_candidates = ["core.analysis", "portscanner.core.analysis"]
    for module_name in module_candidates:
        try:
            module = importlib.import_module(module_name)
            return module.analyze_port
        except (ModuleNotFoundError, ImportError):
            continue

    return lambda port: "Sem analise disponivel"


analyze_port = _load_analyze_port()
DEFAULT_HISTORY_FILE = Path("results/historico_scans.json")


def build_report_data(target_ip, ports, scan_type, timestamp=None):
    report_timestamp = timestamp or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    open_ports = [
        {
            **get_port_risk(port),
            "port": port,
            "service": identify_service(port),
            "status": "open",
            "analysis": analyze_port(port),
        }
        for port in ports
    ]

    return {
        "target": target_ip,
        "scan_type": scan_type,
        "timestamp": report_timestamp,
        "open_ports": open_ports,
        "total_open_ports": len(open_ports),
    }


def _ensure_output_path(filename):
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def append_scan_history(report_data, filename=DEFAULT_HISTORY_FILE):
    output_path = _ensure_output_path(filename)
    history = []

    if output_path.exists():
        try:
            history = json.loads(output_path.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                history = []
        except json.JSONDecodeError:
            history = []

    history.append(
        {
            "timestamp": report_data["timestamp"],
            "target": report_data["target"],
            "open_ports": [port_data["port"] for port_data in report_data["open_ports"]],
        }
    )

    with output_path.open("w", encoding="utf-8") as file_obj:
        json.dump(history, file_obj, indent=4, ensure_ascii=False)

    return output_path


def load_scan_history(filename=DEFAULT_HISTORY_FILE):
    output_path = Path(filename)
    if not output_path.exists():
        return []

    try:
        history = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if not isinstance(history, list):
        return []

    return history


def clear_scan_history(filename=DEFAULT_HISTORY_FILE):
    output_path = _ensure_output_path(filename)
    with output_path.open("w", encoding="utf-8") as file_obj:
        json.dump([], file_obj, indent=4, ensure_ascii=False)
    return output_path


def save_results_txt(report_data, filename="results/resultado_scan.txt"):
    output_path = _ensure_output_path(filename)

    with output_path.open("w", encoding="utf-8") as file_obj:
        file_obj.write("=== Relatorio Final ===\n\n")
        file_obj.write(f"Data/Hora: {report_data['timestamp']}\n")
        file_obj.write(f"Alvo: {report_data['target']}\n")
        file_obj.write(f"Tipo de Scan: {report_data['scan_type']}\n")
        file_obj.write(
            f"Total de portas abertas: {report_data['total_open_ports']}\n\n"
        )
        file_obj.write("Portas abertas:\n")

        if report_data["open_ports"]:
            for port_data in report_data["open_ports"]:
                file_obj.write(
                    f"- {port_data['port']} ({port_data['service']}) - "
                    f"{port_data['status']} - {port_data['analysis']}\n"
                )
        else:
            file_obj.write("Nenhuma porta aberta encontrada.\n")


def save_results_json(report_data, filename="results/resultado_scan.json"):
    output_path = _ensure_output_path(filename)

    with output_path.open("w", encoding="utf-8") as file_obj:
        json.dump(report_data, file_obj, indent=4, ensure_ascii=False)


def save_results(report_data, report_format, txt_filename=None, json_filename=None):
    txt_output = txt_filename or "results/resultado_scan.txt"
    json_output = json_filename or "results/resultado_scan.json"

    if report_format == "1":
        save_results_txt(report_data, txt_output)
        return [txt_output]
    if report_format == "2":
        save_results_json(report_data, json_output)
        return [json_output]
    if report_format == "3":
        save_results_txt(report_data, txt_output)
        save_results_json(report_data, json_output)
        return [txt_output, json_output]

    raise ValueError("Formato de relatorio invalido.")
