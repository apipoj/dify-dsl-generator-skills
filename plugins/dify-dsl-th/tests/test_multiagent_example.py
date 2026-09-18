"""Static wiring checks; these do not invoke models or claim Dify import success."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_generated_dsl import validate_output, load_yaml_via_ruby, lint_dsl


class MultiAgentExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / 'examples/research-writing-review-th-0.7.0.yml'
        cls.data = load_yaml_via_ruby(cls.path)
        cls.graph = cls.data['workflow']['graph']
        cls.nodes = {n['id']: n['data'] for n in cls.graph['nodes']}

    def test_current_output_contract_and_lint(self):
        self.assertEqual(validate_output(self.data), [])
        self.assertEqual(lint_dsl(self.path, self.data)['error_count'], 0)

    def test_agent_chain_and_final_provenance(self):
        self.assertEqual([(e['source'], e['target']) for e in self.graph['edges']],
                         [('start', 'research'), ('research', 'writing'), ('writing', 'review'), ('review', 'end')])
        self.assertEqual({o['variable']: o['value_selector'] for o in self.nodes['end']['outputs']},
                         {'final_document': ['review', 'text'], 'research_notes': ['research', 'text'], 'first_draft': ['writing', 'text']})
        order = ['start', 'research', 'writing', 'review', 'end']
        for node_id in ('research', 'writing', 'review'):
            params = self.nodes[node_id]['agent_parameters']
            for field in ('query', 'instruction'):
                for source, variable in re.findall(r'\{\{#([^.]+)\.([^#]+)#\}\}', params[field]['value']):
                    self.assertLess(order.index(source), order.index(node_id))
                    if source == 'start':
                        self.assertIn(variable, {v['variable'] for v in self.nodes['start']['variables']})
                    else:
                        self.assertEqual(variable, 'text')
        self.assertIn('{{#research.text#}}', self.nodes['review']['agent_parameters']['query']['value'])
        self.assertIn('{{#writing.text#}}', self.nodes['review']['agent_parameters']['query']['value'])

    def test_runtime_configuration_and_tool_boundaries(self):
        for node_id in ('research', 'writing', 'review'):
            node = self.nodes[node_id]
            self.assertEqual(node['type'], 'agent')
            self.assertEqual(node['agent_strategy_name'], 'function_calling')
            params = node['agent_parameters']
            self.assertTrue({'query', 'instruction', 'model', 'tools', 'maximum_iterations'} <= params.keys())
            self.assertEqual(params['model']['value']['model_type'], 'llm')
            self.assertGreaterEqual(params['maximum_iterations']['value'], 1)
            self.assertLessEqual(params['maximum_iterations']['value'], 5)
        self.assertEqual(self.nodes['writing']['agent_parameters']['tools']['value'], [])
        for node_id in ('research', 'review'):
            tool, = self.nodes[node_id]['agent_parameters']['tools']['value']
            self.assertTrue(tool['enabled'])
            self.assertEqual(tool['tool_name'], 'ddgo_search')
            self.assertEqual(tool['parameters']['query']['auto'], 1)
            self.assertEqual(tool['settings']['max_results']['value'], 5)
            self.assertNotIn('credential_id', tool)


if __name__ == '__main__':
    unittest.main()
