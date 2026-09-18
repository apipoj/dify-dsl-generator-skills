from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_plugin_bundle import BUNDLE, NAME, build


class PluginDistributionTests(unittest.TestCase):
    def test_portable_marketplace_and_runtime_resources(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            first, second = build(temp / 'first.zip'), build(temp / 'second.zip')
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                for item in archive.infolist():
                    self.assertTrue(item.filename.startswith(BUNDLE + '/'))
                    self.assertNotIn('..', Path(item.filename).parts)
                    self.assertEqual(item.external_attr >> 16, 0o100644)
                archive.extractall(temp)
            marketplace = temp / BUNDLE
            plugin = marketplace / 'plugins' / NAME
            self.assertFalse((plugin / 'SKILL.md').exists())
            self.assertEqual(len(list((plugin / 'skills').glob('*/SKILL.md'))), 12)
            versions = []
            for platform, catalog_path in [('codex', '.agents/plugins/marketplace.json'), ('claude', '.claude-plugin/marketplace.json')]:
                catalog = json.loads((marketplace / catalog_path).read_text())
                entry = catalog['plugins'][0]
                source = entry['source']['path'] if platform == 'codex' else entry['source']
                self.assertEqual((marketplace / source).resolve(), plugin.resolve())
                manifest = json.loads((plugin / f'.{platform}-plugin/plugin.json').read_text())
                self.assertEqual(manifest['name'], plugin.name)
                versions.append(manifest['version'])
                self.assertNotIn('mcpServers', manifest)
                self.assertNotIn('hooks', manifest)
            self.assertEqual(versions[0], versions[1])
            for path in [*(plugin / 'skills').rglob('*.md'), *(plugin / 'docs').rglob('*.md')]:
                for raw in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                    target = raw.split('#', 1)[0]
                    if not target or re.match(r'^[a-z]+:', target):
                        continue
                    resolved = (path.parent / target).resolve()
                    self.assertTrue(resolved.is_relative_to(plugin.resolve()), (path, target))
                    self.assertTrue(resolved.exists(), (path, target))
            result = subprocess.run(
                [sys.executable, str(plugin / 'scripts/validate_generated_dsl.py'), str(plugin / 'examples/echo-workflow-0.7.0.yml')],
                cwd=temp, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            # The packaged builder can itself run without the original checkout.
            result = subprocess.run(
                [sys.executable, str(plugin / 'scripts/build_plugin_bundle.py'), '--output', str(temp / 'rebuilt.zip')],
                cwd=temp, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(first.read_bytes(), (temp / 'rebuilt.zip').read_bytes())
