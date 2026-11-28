"""NC-031 regression checks for sourced employer-primary-business evidence."""
import re
import unittest

from test_legal_nc_policy import RULES, field, nc_section


class NcIndustrialGasPolicyTest(unittest.TestCase):
    def setUp(self):
        lines = [line for line in nc_section(RULES.read_text()).splitlines()
                 if line.startswith('- NC-031 ')]
        self.assertEqual(len(lines), 1)
        self.rule = lines[0]
        self.assertTrue(self.rule.startswith('- NC-031 INDUSTRIAL_GAS_PRODUCERS_AND_DISTRIBUTORS: '))
        self.business_terms = field(self.rule, 'employer_business_any')

    def disposition(self, primary_business):
        # Exercise the canonical machine field against sourced primary business.
        # The production Writer is not part of this policy repository.
        if any(re.search(r'\b' + re.escape(term) + r'\b', primary_business, re.IGNORECASE)
               for term in self.business_terms):
            return 'NEVER_CONSIDER_EXCLUDED'
        return 'ALLOW_INTAKE'

    def test_plant_operations_roles_at_named_employers_are_excluded(self):
        title = 'Plant Operations Director'
        for employer, business in (
            ('MATHESON (Matheson Tri-Gas)', 'industrial gas production'),
            ('Linde', 'industrial gas producer'),
            ('Air Products', 'industrial gas production and distribution'),
            ('Airgas', 'industrial gas distributor'),
        ):
            with self.subTest(employer=employer, title=title):
                self.assertIn(employer, self.rule)
                self.assertEqual(self.disposition(business), 'NEVER_CONSIDER_EXCLUDED')

    def test_gas_buyer_and_unrelated_air_employer_are_not_excluded(self):
        for employer, business in (
            ('Precision Stampings', 'metal stamping that buys industrial gases'),
            ('Air Motion Systems', 'industrial fan manufacturing'),
        ):
            with self.subTest(employer=employer, title='Plant Operations Director'):
                self.assertEqual(self.disposition(business), 'ALLOW_INTAKE')
