#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPO_ROOT / "docs" / "dify-dsl-route-matrix.json"
ROUTE_START = "<!-- BEGIN ROUTE_MATRIX -->"
ROUTE_END = "<!-- END ROUTE_MATRIX -->"
PATH_START = "<!-- BEGIN MAIN_PATH -->"
PATH_END = "<!-- END MAIN_PATH -->"


@dataclass(frozen=True)
class FileSpec:
    path: str
    locale: str
    entry_style: str
    has_main_path: bool


FILE_SPECS = (
    FileSpec("docs/README.md", "th", "linked", False),
    FileSpec("docs/dify-dsl-subagent-review-overview.th.md", "th", "linked", True),
    FileSpec("README.zh-CN.md", "zh", "plain", True),
    FileSpec("README.en.md", "en", "plain", True),
    FileSpec("docs/dify-dsl-subagent-review-overview.zh-CN.md", "zh", "plain", True),
    FileSpec("docs/dify-dsl-subagent-review-overview.md", "en", "plain", True),
    FileSpec("skills/dify-dsl-foundations/references/task-routing.md", "zh", "linked", False),
)


def load_source() -> dict:
    return json.loads(SOURCE_PATH.read_text(encoding="utf-8"))


def join_entries(entries: list[dict], file_path: Path, locale: str, style: str) -> str:
    parts: list[str] = []
    for entry in entries:
        if style == "plain":
            parts.append(f"`{entry['name']}`")
            continue
        relative = os.path.relpath(REPO_ROOT / entry["path"], file_path.parent)
        parts.append(f"[{entry['name']}]({Path(relative).as_posix()})")
    separator = {"zh": " 或 ", "en": " or ", "th": " หรือ "}[locale]
    return separator.join(parts)


def render_route_matrix(source: dict, spec: FileSpec) -> str:
    headers = {
        "zh": "| 用户目标 | 推荐入口 | 常见下一步 |",
        "en": "| User goal | Recommended entry | Common next step |",
        "th": "| เป้าหมาย | Skill เริ่มต้น | ขั้นตอนถัดไป |",
    }
    lines = [headers[spec.locale], "| --- | --- | --- |"]
    for row in source["rows"]:
        entry = join_entries(row["entries"], REPO_ROOT / spec.path, spec.locale, spec.entry_style)
        lines.append(f"| {row[f'goal_{spec.locale}']} | {entry} | {row[f'next_{spec.locale}']} |")
    return "\n".join(lines)


def render_main_path(source: dict, locale: str) -> str:
    lines = source[f"main_path_{locale}"]
    return "```text\n" + "\n".join(lines) + "\n```"


def replace_block(content: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = content.find(start_marker)
    end = content.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"缺少标记: {start_marker} / {end_marker}")
    prefix = content[: start + len(start_marker)]
    suffix = content[end:]
    return prefix + "\n" + replacement.rstrip() + "\n" + suffix


def render_expected(path: Path, spec: FileSpec, source: dict) -> str:
    content = path.read_text(encoding="utf-8")
    content = replace_block(content, ROUTE_START, ROUTE_END, render_route_matrix(source, spec))
    if spec.has_main_path:
        content = replace_block(content, PATH_START, PATH_END, render_main_path(source, spec.locale))
    return content


def write_docs() -> int:
    source = load_source()
    for spec in FILE_SPECS:
        path = REPO_ROOT / spec.path
        path.write_text(render_expected(path, spec, source), encoding="utf-8")
        print(f"已同步: {path}")
    return 0


def check_docs() -> int:
    source = load_source()
    mismatches: list[str] = []
    for spec in FILE_SPECS:
        path = REPO_ROOT / spec.path
        expected = render_expected(path, spec, source)
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(str(path))
    if mismatches:
        for path in mismatches:
            print(f"错误: route matrix 文档未同步 -> {path}", file=sys.stderr)
        print("提示: 运行 `python3 scripts/route_matrix_docs.py --write` 同步文档。", file=sys.stderr)
        return 1
    print("通过: route matrix 文档已与单一事实源保持同步")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="同步或校验 Dify DSL 路由矩阵文档")
    parser.add_argument("--write", action="store_true", help="把 route matrix 写回文档")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.write:
        return write_docs()
    return check_docs()


if __name__ == "__main__":
    raise SystemExit(main())
