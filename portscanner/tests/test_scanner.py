import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from portscanner.core import scanner as core_scanner
from portscanner.core.services import identify_service
from portscanner.core.utils import (
    append_scan_history,
    build_report_data,
    clear_scan_history,
    load_scan_history,
    save_results,
)
from portscanner.scanner import (
    FAST_PORTS,
    parse_port_range,
    resolve_ports_to_scan,
    resolve_scan_type,
)


class ScannerCliLogicTests(unittest.TestCase):
    def test_parse_port_range_valid(self):
        self.assertEqual(parse_port_range("20-80"), (20, 80))

    def test_parse_port_range_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_port_range("2080")

    def test_parse_port_range_invalid_values(self):
        with self.assertRaises(ValueError):
            parse_port_range("70000-70010")

        with self.assertRaises(ValueError):
            parse_port_range("80-20")

    def test_resolve_ports_fast_mode(self):
        self.assertEqual(resolve_ports_to_scan("2", None, True), FAST_PORTS)

    def test_resolve_ports_custom_mode_requires_range(self):
        with self.assertRaises(ValueError):
            resolve_ports_to_scan("3", None, False)

    def test_resolve_ports_custom_mode_range(self):
        ports = list(resolve_ports_to_scan("3", "10-12", False))
        self.assertEqual(ports, [10, 11, 12])

    def test_resolve_scan_type(self):
        self.assertEqual(resolve_scan_type("1", False), "fast")
        self.assertEqual(resolve_scan_type("2", False), "full")
        self.assertEqual(resolve_scan_type("3", False), "custom")
        self.assertEqual(resolve_scan_type("2", True), "fast")


class ServiceAndCoreScannerTests(unittest.TestCase):
    def test_identify_service_known_and_unknown(self):
        self.assertEqual(identify_service(22), "SSH")
        self.assertEqual(identify_service(9999), "Desconhecido")

    @patch("portscanner.core.scanner.scan_port")
    def test_scan_ports_collects_open_ports(self, mock_scan_port):
        mock_scan_port.side_effect = (
            lambda target_ip, port, timeout=1: port if port % 2 == 0 else None
        )

        result = core_scanner.scan_ports(
            "127.0.0.1", 1, 6, timeout=1, max_threads=4)
        self.assertEqual(sorted(result), [2, 4, 6])


class ReportPersistenceTests(unittest.TestCase):
    def test_build_report_data_includes_metadata(self):
        report_data = build_report_data(
            "192.168.0.10",
            [22, 80, 3306],
            "fast",
            timestamp="2026-05-13T19:20:00",
        )

        self.assertEqual(report_data["target"], "192.168.0.10")
        self.assertEqual(report_data["scan_type"], "fast")
        self.assertEqual(report_data["timestamp"], "2026-05-13T19:20:00")
        self.assertEqual(report_data["total_open_ports"], 3)
        self.assertEqual(
            [item["port"] for item in report_data["open_ports"]],
            [22, 80, 3306],
        )
        self.assertEqual(report_data["open_ports"][0]["icon"], "⚠️")
        self.assertEqual(report_data["open_ports"][1]["tone"], "attention")
        self.assertEqual(report_data["open_ports"][2]["label"], "Risco")

    def test_save_results_txt_and_json(self):
        report_data = build_report_data(
            "192.168.0.10",
            [22, 80],
            "fast",
            timestamp="2026-05-13T19:20:00",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            txt_path = Path(temp_dir) / "resultado_scan.txt"
            json_path = Path(temp_dir) / "resultado_scan.json"

            saved_files = save_results(report_data, "3", txt_path, json_path)

            self.assertEqual(saved_files, [txt_path, json_path])
            self.assertTrue(txt_path.exists())
            self.assertTrue(json_path.exists())

            txt_content = txt_path.read_text(encoding="utf-8")
            json_content = json_path.read_text(encoding="utf-8")

            self.assertIn("Data/Hora: 2026-05-13T19:20:00", txt_content)
            self.assertIn("Alvo: 192.168.0.10", txt_content)
            self.assertIn("Portas abertas:", txt_content)
            self.assertIn('"target": "192.168.0.10"', json_content)
            self.assertIn('"total_open_ports": 2', json_content)

    def test_save_results_invalid_format(self):
        report_data = build_report_data("127.0.0.1", [], "fast")

        with self.assertRaises(ValueError):
            save_results(report_data, "9")

    def test_append_and_load_scan_history(self):
        first_report = build_report_data(
            "192.168.0.10",
            [22, 80],
            "fast",
            timestamp="2026-05-13 20:30:00",
        )
        second_report = build_report_data(
            "192.168.0.10",
            [22, 80, 3306],
            "fast",
            timestamp="2026-05-13 20:45:00",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "historico_scans.json"

            append_scan_history(first_report, history_path)
            append_scan_history(second_report, history_path)

            history = load_scan_history(history_path)

            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["timestamp"], "2026-05-13 20:30:00")
            self.assertEqual(history[0]["open_ports"], [22, 80])
            self.assertEqual(history[1]["timestamp"], "2026-05-13 20:45:00")
            self.assertEqual(history[1]["open_ports"], [22, 80, 3306])

    def test_clear_scan_history(self):
        report = build_report_data(
            "192.168.0.10",
            [22],
            "fast",
            timestamp="2026-05-13 20:30:00",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "historico_scans.json"
            append_scan_history(report, history_path)

            cleared_path = clear_scan_history(history_path)
            history = load_scan_history(history_path)

            self.assertEqual(cleared_path, history_path)
            self.assertEqual(history, [])


if __name__ == "__main__":
    unittest.main()
