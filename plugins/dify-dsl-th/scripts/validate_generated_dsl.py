#!/usr/bin/env python3
"""Check the current output contract, then run the existing DSL linter.

Historical fixture/review validation remains available through lint_dsl.py.
This check does not import or execute a workflow in Dify.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/dify-dsl-quality/scripts'))
from lint_dsl import lint_dsl, load_yaml_via_ruby

CURRENT_VERSIONS = {'app': '0.7.0', 'rag_pipeline': '0.1.0'}


def validate_output(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ['DSL must be a YAML mapping']
    kind = data.get('kind')
    if not isinstance(kind, str) or kind not in CURRENT_VERSIONS:
        return ['kind must be app or rag_pipeline']
    expected = CURRENT_VERSIONS[kind]
    if data.get('version') != expected:
        errors.append(f'{kind} output requires version: "{expected}" (string)')
    if kind == 'app':
        app = data.get('app')
        if not isinstance(app, dict) or app.get('mode') not in ('workflow', 'advanced-chat'):
            errors.append('This pack supports app modes workflow and advanced-chat only')
    elif not isinstance(data.get('rag_pipeline'), dict):
        errors.append('rag_pipeline metadata is required')
    workflow = data.get('workflow')
    graph = workflow.get('graph') if isinstance(workflow, dict) else None
    if not isinstance(graph, dict) or not isinstance(graph.get('nodes'), list) or not isinstance(graph.get('edges'), list):
        errors.append('workflow.graph requires nodes and edges lists')
        return errors
    if not graph['nodes']:
        errors.append('workflow.graph.nodes must not be empty')
    for node in graph['nodes']:
        if not isinstance(node, dict) or not isinstance(node.get('data'), dict):
            errors.append('Every node requires a data mapping')
            continue
        node_data = node['data']
        if node_data.get('type') == 'agent-v2' or 'agent_binding' in node_data or 'agent_job' in node_data:
            errors.append('Portable Agent nodes require separate schema/runtime review; this checker does not validate them')
    if any(not isinstance(edge, dict) for edge in graph['edges']):
        errors.append('Every edge must be a mapping')
    if 'agent' in data or 'agent_packages' in data:
        errors.append('Portable Agent packages are outside this pack\'s validated output scope')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    path = args.path.expanduser().resolve()
    try:
        data = load_yaml_via_ruby(path)
        errors = validate_output(data)
        if errors:
            print(json.dumps({'output_contract_errors': errors}, ensure_ascii=False, indent=2))
            return 1
        report = lint_dsl(path, data)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if report['error_count'] else 0
    except Exception as exc:
        print(f'Validation failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
