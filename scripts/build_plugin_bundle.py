#!/usr/bin/env python3
"""Build a portable local marketplace for Codex and Claude Code from shared skills."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from build_claude_ai_bundle import NAME, ROOT, package_files

MARKETPLACE = 'personal'
BUNDLE = 'dify-dsl-plugins'


def bundle_files() -> dict[str, bytes]:
    payload = package_files()
    # Native hosts discover the 12 skills directly, without the Claude.ai wrapper.
    payload.pop('SKILL.md')
    for platform in ('codex', 'claude'):
        name = f'.{platform}-plugin/plugin.json'
        payload[name] = payload[f'packaging/{NAME}/{name}']
    manifests = [json.loads(payload[f'.{platform}-plugin/plugin.json']) for platform in ('codex', 'claude')]
    if any(m['name'] != NAME for m in manifests) or manifests[0]['version'] != manifests[1]['version']:
        raise ValueError('Plugin names and versions must agree across platforms')
    files = {f'plugins/{NAME}/{name}': data for name, data in payload.items()}
    catalogs = {
        '.agents/plugins/marketplace.json': {
            'name': MARKETPLACE, 'interface': {'displayName': 'Dify DSL ภาษาไทย'},
            'plugins': [{'name': NAME, 'source': {'source': 'local', 'path': f'./plugins/{NAME}'},
                         'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                         'category': 'Productivity'}],
        },
        '.claude-plugin/marketplace.json': {
            'name': MARKETPLACE, 'owner': {'name': 'apipoj'},
            'metadata': {'description': 'Thai Dify DSL skills for Claude Code and Codex.'},
            'plugins': [{'name': NAME, 'source': f'./plugins/{NAME}'}],
        },
    }
    for name, data in catalogs.items():
        files[name] = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    return files


def build(output: Path) -> Path:
    """Write deterministic bytes atomically; never modify installed plugins."""
    files = bundle_files()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        temporary = Path(directory) / 'bundle.zip'
        with ZipFile(temporary, 'w', ZIP_DEFLATED) as archive:
            for name, data in sorted(files.items()):
                entry = ZipInfo(f'{BUNDLE}/{name}', date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, data)
        temporary.replace(output)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist' / f'{BUNDLE}.zip')
    args = parser.parse_args()
    print(build(args.output.expanduser().resolve()))
