"""Structural regression checks for Tim's process-industry scope and carveouts."""
import pathlib
import unittest

RULES = pathlib.Path(__file__).resolve().parents[1] / 'rules/TIM_PIPELINE_RULES_CANONICAL.txt'

class ProcessIndustryPolicyTest(unittest.TestCase):
    def setUp(self):
        self.text = RULES.read_text()
        self.section = self.text.split('SECTION=GLOBAL_PROCESS_INDUSTRY_EXCLUSION\n')[1].split('SECTION=')[0]

    def test_single_stable_ruling(self):
        self.assertEqual(self.text.count('SECTION=GLOBAL_PROCESS_INDUSTRY_EXCLUSION\n'), 1)
        self.assertEqual(self.section.count('RULING_ID=TIM-20261112-PROCESS-INDUSTRY'), 1)
        self.assertIn('REASON=NEVER_CONSIDER — PROCESS_INDUSTRY', self.section)
        self.assertEqual(sum(line.startswith('- Exclude employers whose PRIMARY business') for line in self.section.splitlines()), 1)
        for term in ('bulk chemical production', 'refining', 'raw-material production'):
            self.assertIn(term, self.section)

    def test_discrete_supplier_and_unknown_boundaries(self):
        for term in ('Do not exclude discrete manufacturing', 'stamping, molding or machining',
                     'Do not exclude industrial suppliers', 'diversified manufacturers',
                     'solely because they serve an excluded industry',
                     'does not add a mandatory employer-site lookup', 'remains visible and progresses',
                     'classify only the identified client'):
            self.assertIn(term, self.section)

    def test_protected_history_and_separate_activation(self):
        for term in ('Preserve applications, terminal history', 'explicit Tim decisions',
                     'does not authorize deletion or replay', 'separate deployment setting'):
            self.assertIn(term, self.section)
        self.assertIn('RULING_ID=ASK-20261023-CLAUDE-1312', self.text)

if __name__ == '__main__':
    unittest.main()
