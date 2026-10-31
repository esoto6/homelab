"""Offline regression tests: render actual inventory without connecting to LXCs."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AlloyTelemetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache = Path.home() / '.cache/homelab-alloy-tests'
        cache.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=cache)
        cls.output = Path(cls.temp.name)
        binary = os.environ.get('ANSIBLE_PLAYBOOK', str(ROOT / '.venv/bin/ansible-playbook'))
        result = subprocess.run([binary, 'tests/render_alloy.yml', '-e', 'alloy_test_output=' + str(cls.output), '-e', 'hermes_tempo_otlp_http_endpoint=http://tempo.example.test:4318'], cwd=ROOT, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        cls.rendered = {p.stem: p.read_text() for p in cls.output.glob('*.alloy')}
        if not cls.rendered:
            raise RuntimeError('No inventory hosts rendered')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_hermes_loopback_receiver_routes_all_three_signals(self):
        config = self.rendered['hermes']
        self.assertIn('otelcol.receiver.otlp "hermes_gateway"', config)
        self.assertIn('endpoint = "127.0.0.1:4318"', config)
        self.assertIn('metrics = [otelcol.exporter.prometheus.hermes_gateway.input]', config)
        self.assertIn('logs = [otelcol.exporter.loki.hermes_gateway.input]', config)
        self.assertIn('traces = [otelcol.exporter.otlphttp.hermes_gateway.input]', config)
        self.assertIn('endpoint = "http://tempo.example.test:4318"', config)
        self.assertNotIn('drop_otlp_logs', config)
        self.assertNotIn('otelcol.receiver.otlp "applications"', config)

    def test_hermes_host_vars_contain_no_ip_literals(self):
        source = (ROOT / "inventory/host_vars/hermes.yml").read_text()
        self.assertNotRegex(source, r"[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+")

    def test_hermes_receiver_is_opt_in(self):
        for host, config in self.rendered.items():
            if host != 'hermes':
                with self.subTest(host=host):
                    self.assertNotIn('"hermes_gateway"', config)

    def test_docker_preserves_existing_otlp_behavior(self):
        config = self.rendered['docker']
        self.assertIn('otelcol.receiver.otlp "applications"', config)
        self.assertIn('endpoint = "0.0.0.0:4318"', config)
        self.assertIn('logs = [otelcol.processor.filter.drop_otlp_logs.input]', config)
        self.assertIn('endpoint = "tempo:4317"', config)

if __name__ == '__main__':
    unittest.main(verbosity=2)
