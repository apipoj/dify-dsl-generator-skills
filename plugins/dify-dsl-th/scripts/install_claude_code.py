#!/usr/bin/env python3
"""Expose the source skills to Claude Code without overwriting other skills."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(destination: Path) -> None:
    sources = sorted(path.parent for path in (ROOT / 'skills').glob('*/SKILL.md'))
    if not sources:
        raise ValueError('No skills found')
    destination = destination.expanduser().resolve()
    # Check all conflicts before creating any links.
    for source in sources:
        target = destination / source.name
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        if target.exists() or target.is_symlink():
            raise ValueError(f'Refusing to overwrite: {target}')
    destination.mkdir(parents=True, exist_ok=True)
    for source in sources:
        target = destination / source.name
        if not target.is_symlink():
            target.symlink_to(os.path.relpath(source, destination), target_is_directory=True)
    print(f'Ready: {len(sources)} skills in {destination}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--user', action='store_true', help='Install for all local projects')
    group.add_argument('--dest', type=Path, help='Custom skills directory')
    args = parser.parse_args()
    destination = args.dest or (Path.home() / '.claude/skills' if args.user else ROOT / '.claude/skills')
    try:
        install(destination)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
