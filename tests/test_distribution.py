from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_claude_ai_bundle import build, NAME
from install_claude_code import install
from validate_generated_dsl import validate_output


def output(kind='app', version='0.7.0'):
    return {
        'kind': kind, 'version': version,
        'app': {'mode': 'workflow'}, 'rag_pipeline': {'name': 'test'},
        'workflow': {'graph': {'nodes': [{'id': 'start', 'data': {'type': 'start'}}], 'edges': []}},
    }


class OutputContractTests(unittest.TestCase):
    def test_app_version_and_type(self):
        self.assertEqual(validate_output(output()), [])
        for version in ('0.6.0', '0.7', 0.7, None, '0.8.0'):
            with self.subTest(version=version):
                self.assertTrue(validate_output(output(version=version)))

    def test_rag_uses_its_own_version(self):
        self.assertEqual(validate_output(output('rag_pipeline', '0.1.0')), [])
        self.assertTrue(validate_output(output('rag_pipeline', '0.7.0')))

    def test_malformed_shapes(self):
        for data in (None, [], {'kind': []}, {'kind': 'app', 'version': '0.7.0'}, {'kind': 'snippet'}):
            with self.subTest(data=data):
                self.assertTrue(validate_output(data))

    def test_new_agent_scope_is_not_silently_accepted(self):
        data = output()
        data['workflow']['graph']['nodes'][0]['data']['type'] = 'agent-v2'
        self.assertTrue(validate_output(data))
        data = output()
        data['agent_packages'] = {}
        self.assertTrue(validate_output(data))
        data = output()
        data['app']['mode'] = 'agent-chat'
        self.assertTrue(validate_output(data))

    def test_real_example_and_legacy_cli(self):
        command = [sys.executable, str(ROOT / 'scripts/validate_generated_dsl.py')]
        current = subprocess.run(command + [str(ROOT / 'examples/echo-workflow-0.7.0.yml')], capture_output=True, text=True)
        self.assertEqual(current.returncode, 0, current.stdout + current.stderr)
        legacy = subprocess.run(command + [str(ROOT / 'tests/fixtures/dsl/min-workflow.yml')], capture_output=True, text=True)
        self.assertNotEqual(legacy.returncode, 0)
        self.assertIn('0.7.0', legacy.stdout)


class InstallationTests(unittest.TestCase):
    def test_install_is_repeatable_and_preserves_links(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skills'
            install(destination)
            install(destination)
            links = list(destination.iterdir())
            self.assertEqual(len(links), 12)
            for link in links:
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), ROOT / 'skills' / link.name)

    def test_conflict_is_detected_before_partial_install(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            conflict = destination / 'using-dify-dsl'
            conflict.write_text('keep me')
            with self.assertRaises(ValueError):
                install(destination)
            self.assertEqual(list(destination.iterdir()), [conflict])
            self.assertEqual(conflict.read_text(), 'keep me')

    def test_dangling_link_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            (destination / 'using-dify-dsl').symlink_to('missing')
            with self.assertRaises(ValueError):
                install(destination)
            self.assertTrue((destination / 'using-dify-dsl').is_symlink())


class BundleTests(unittest.TestCase):
    def test_bundle_is_reproducible_and_self_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            first, second = build(temp / 'a.zip'), build(temp / 'b.zip')
            self.assertEqual(hashlib.sha256(first.read_bytes()).digest(), hashlib.sha256(second.read_bytes()).digest())
            with ZipFile(first) as archive:
                names = archive.namelist()
                self.assertTrue(all(name.startswith(NAME + '/') for name in names))
                self.assertFalse(any('__pycache__' in name or '/.git/' in name or name.endswith('.pyc') for name in names))
                archive.extractall(temp / 'extracted')
            package = (temp / 'extracted' / NAME).resolve()
            self.assertEqual(len(list((package / 'skills').glob('*/SKILL.md'))), 12)
            self.assertEqual((package / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
            for path in [package / 'SKILL.md', *(package / 'skills').rglob('*.md')]:
                for raw in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                    target = raw.split('#', 1)[0]
                    if not target or re.match(r'^[a-z]+:', target):
                        continue
                    resolved = (path.parent / target).resolve()
                    self.assertTrue(resolved.is_relative_to(package), (path, target))
                    self.assertTrue(resolved.exists(), (path, target))
            # Execute from the extracted package with an unrelated working directory.
            result = subprocess.run(
                [sys.executable, str(package / 'scripts/validate_generated_dsl.py'), str(package / 'examples/echo-workflow-0.7.0.yml')],
                cwd=temp, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
