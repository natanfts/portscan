"""
Aplicacao web Flask para exibir resultados do Port Scanner em interface visual.
"""

from flask import Flask, jsonify, redirect, render_template, request, url_for
from datetime import datetime

# Ajustar imports para funcionar de ambas as formas
try:
    from core.scanner import scan_port
    from core.utils import (
        append_scan_history,
        build_report_data,
        clear_scan_history,
        load_scan_history,
    )
except ModuleNotFoundError:
    from portscanner.core.scanner import scan_port
    from portscanner.core.utils import (
        append_scan_history,
        build_report_data,
        clear_scan_history,
        load_scan_history,
    )

app = Flask(__name__, template_folder="templates")


def _resolve_scan_ports(port_range_str=None, fast=True):
    if fast:
        return [22, 80, 443, 3306, 21, 25, 53], "fast"
    if port_range_str:
        start, end = map(int, port_range_str.split("-"))
        return range(start, end + 1), "custom"
    return range(1, 1025), "standard"


def run_scan(target_ip, port_range_str=None, fast=True):
    """Executa scan e retorna dados formatados."""
    try:
        ports_to_scan, scan_type = _resolve_scan_ports(port_range_str, fast)

        open_ports = []
        for port in ports_to_scan:
            if scan_port(target_ip, port, timeout=2):
                open_ports.append(port)

        results = build_report_data(
            target_ip,
            open_ports,
            scan_type,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        append_scan_history(results)
        results["error"] = None
        return results

    except Exception as exc:
        return {
            "target": target_ip,
            "scan_type": "error",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "open_ports": [],
            "total_open_ports": 0,
            "error": str(exc),
        }


@app.route("/", methods=["GET", "POST"])
def index():
    """Pagina inicial com formulario de scan."""
    data = None
    history = list(reversed(load_scan_history()))

    if request.method == "POST":
        target_ip = request.form.get("ip", "").strip()
        port_range = request.form.get("port_range", "").strip()
        fast = request.form.get("fast") == "on"

        if target_ip:
            data = run_scan(target_ip, port_range if not fast else None, fast)
            history = list(reversed(load_scan_history()))
        else:
            data = {"error": "IP ou hostname nao informado", "open_ports": []}

    return render_template(
        "index.html",
        data=data if data else {"error": None, "open_ports": []},
        history=history,
    )


@app.route("/api/scan", methods=["POST"])
def api_scan():
    """Endpoint API para scans programaticos."""
    payload = request.get_json()
    target_ip = payload.get("ip", "").strip()
    port_range = payload.get("port_range", "").strip()
    fast = payload.get("fast", True)

    if not target_ip:
        return jsonify({"error": "IP nao informado"}), 400

    result = run_scan(target_ip, port_range if not fast else None, fast)
    return jsonify(result)


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Limpa o historico de scans do dashboard."""
    clear_scan_history()
    return redirect(url_for("index", cleared="1"))


@app.route("/api/history/clear", methods=["POST"])
def api_clear_history():
    """Endpoint API para limpar historico de scans."""
    clear_scan_history()
    return jsonify({"ok": True, "message": "Historico limpo com sucesso."})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
