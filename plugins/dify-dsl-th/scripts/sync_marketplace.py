#!/usr/bin/env python3
"""Materialize the Git-installable marketplace; --check detects release drift."""
from __future__ import annotations

import argparse
from pathlib import Path

from build_plugin_bundle import ROOT, bundle_files


def sync(root: Path, check: bool = False) -> list[str]:
    expected = bundle_files()
    managed = root / 'plugins' / 'dify-dsl-th'
    actual = {
        path.relative_to(root).as_posix()
        for path in managed.rglob('*')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc'
    }
    stale = actual - expected.keys()
    changed = [name for name, data in expected.items()
               if not (root / name).is_file() or (root / name).read_bytes() != data]
    if not check:
        for name in stale:
            (root / name).unlink()
        for name in changed:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected[name])
    return sorted(stale | set(changed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changes = sync(ROOT, args.check)
    if args.check and changes:
        print('Marketplace is stale. Run python3 scripts/sync_marketplace.py')
        print('\n'.join(changes))
        raise SystemExit(1)
    print(f'Marketplace {"checked" if args.check else "synced"}: {len(changes)} changed files')
