import subprocess
import sys


def test_scan_engine_does_not_import_snmp_scanner_eagerly():
    script = """
import changeme.scan_engine
import sys
raise SystemExit('changeme.scanners.snmp' in sys.modules)
"""
    result = subprocess.run([sys.executable, '-c', script])

    assert result.returncode == 0
