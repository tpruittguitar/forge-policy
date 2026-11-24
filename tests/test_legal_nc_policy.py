"""NC-029/NC-030 legal policy machine fields for the canonical ruleset."""
import pathlib
import re
import unittest

RULES = pathlib.Path(__file__).resolve().parents[1] / 'rules/TIM_PIPELINE_RULES_CANONICAL.txt'


def nc_section(text):
    return text.split('SECTION=NEVER_CONSIDER\n')[1].split('\nSECTION=')[0]


def field(line, key):
    m = re.search(r'(?:^|[;\s])' + key + r'\s*=\s*([^;]*)', line)
    return [p.strip() for p in m.group(1).split('|')] if m else []


class NcLegalPolicyTest(unittest.TestCase):
    def setUp(self):
        self.lines = [l for l in nc_section(RULES.read_text()).splitlines() if l.startswith('- NC-')]

    def line(self, rule_id):
        hits = [l for l in self.lines if l.startswith('- ' + rule_id + ' ')]
        self.assertEqual(len(hits), 1, rule_id)
        return hits[0]

    def test_nc029_and_nc030_have_expected_fields(self):
        nc029 = self.line('NC-029')
        nc030 = self.line('NC-030')
        self.assertTrue(nc029.startswith('- NC-029 LAW_FIRMS_AND_LEGAL_SERVICES: '))
        self.assertTrue(nc030.startswith('- NC-030 LEGAL_ROLES: '))

        business_any = field(nc029, 'employer_business_any')
        for term in ('law firm', 'law firms', 'legal services', 'trial lawyer', 'trial lawyers', 'lawyers', 'law office', 'legal practice', 'attorney at law'):
            self.assertIn(term, business_any)
        business_exempt = field(nc029, 'employer_business_exempt')
        for term in ('manufacturing', 'manufacturer', 'equipment', 'automation', 'supplier', 'recruiting', 'staffing'):
            self.assertIn(term, business_exempt)
        self.assertFalse(set(business_any) & set(business_exempt))
        self.assertTrue(all(p and '=' not in p for p in business_any + business_exempt))

        title_any = field(nc030, 'title_any')
        for term in ('attorney', 'counsel', 'paralegal', 'legal operations', 'lawyer', 'legal ops', 'legal'):
            self.assertIn(term, title_any)
        for term in ('counseling', 'counselor', 'regulatory', 'compliance', 'quality'):
            self.assertNotIn(term, title_any)
        self.assertTrue(all(p and '=' not in p for p in title_any))

    def test_rule_ids_unique_and_include_legal_rules(self):
        ids = [m.group(1) for m in (re.match(r'- (NC-\d+) [A-Z0-9_]+:', l) for l in self.lines) if m]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn('NC-029', ids)
        self.assertIn('NC-030', ids)

    def test_role_families_sentence_mentions_nc030(self):
        text = RULES.read_text()
        self.assertIn('NC-030 LEGAL_ROLES', text)


if __name__ == '__main__':
    unittest.main()
