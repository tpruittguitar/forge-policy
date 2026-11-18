"""NC-008 healthcare services carries machine fields the Writer classifier reads (card a9c0469)."""
import pathlib
import re
import unittest

RULES = pathlib.Path(__file__).resolve().parents[1] / 'rules/TIM_PIPELINE_RULES_CANONICAL.txt'


def nc_section(text):
    return text.split('SECTION=NEVER_CONSIDER\n')[1].split('\nSECTION=')[0]


def field(line, key):
    m = re.search(r'(?:^|[;\s])' + key + r'\s*=\s*([^;]*)', line)
    return [p.strip() for p in m.group(1).split('|')] if m else []


class Nc008HealthcarePolicyTest(unittest.TestCase):
    def setUp(self):
        self.lines = [l for l in nc_section(RULES.read_text()).splitlines() if l.startswith('- NC-')]

    def line(self, rule_id):
        hits = [l for l in self.lines if l.startswith('- ' + rule_id + ' ')]
        self.assertEqual(len(hits), 1, rule_id)
        return hits[0]

    def test_nc008_has_business_fields(self):
        nc008 = self.line('NC-008')
        self.assertTrue(nc008.startswith('- NC-008 HEALTHCARE_SERVICES: '))
        business = field(nc008, 'employer_business_any')
        for term in ('healthcare services', 'hospital', 'vein', 'vascular'):
            self.assertIn(term, business)
        exempt = field(nc008, 'employer_business_exempt')
        for term in ('manufacturing', 'manufacturer', 'equipment', 'automation', 'supplier', 'recruiting', 'staffing'):
            self.assertIn(term, exempt)
        self.assertFalse(set(business) & set(exempt))
        self.assertTrue(all(p and '=' not in p for p in business + exempt))

    def test_united_vein_employer_line_points_to_nc008(self):
        hits = [l for l in self.lines if 'employer=United Vein & Vascular Centers;' in l]
        self.assertEqual(len(hits), 1)
        self.assertIn('rule=NC-008;', hits[0])
        self.assertIn('source_url=https://', hits[0])

    def test_rule_ids_unique(self):
        ids = [m.group(1) for m in (re.match(r'- (NC-\d+) [A-Z0-9_]+:', l) for l in self.lines) if m]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == '__main__':
    unittest.main()
