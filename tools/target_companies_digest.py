#!/usr/bin/env python3
"""Write derived/TARGET_COMPANIES_PRIORITY.txt from SECTION=TARGET_COMPANIES of the canonical rules.
The digest is what discovery lanes read (small file, no copy of the list lives anywhere else).
Usage: python3 tools/target_companies_digest.py [rules_path] [out_path] [source_sha]"""
import json, re, sys
rules = sys.argv[1] if len(sys.argv) > 1 else 'rules/TIM_PIPELINE_RULES_CANONICAL.txt'
out = sys.argv[2] if len(sys.argv) > 2 else 'derived/TARGET_COMPANIES_PRIORITY.txt'
sha = sys.argv[3] if len(sys.argv) > 3 else ''
text = open(rules, encoding='utf-8').read()
m = re.search(r'(?:^|\n)SECTION=TARGET_COMPANIES\s*\n([\s\S]*?)(?=\nSECTION=|\nEND TIM_PIPELINE_RULES_CANONICAL|$)', text)
if not m: sys.exit('SECTION=TARGET_COMPANIES not found')
order = ['DREAM', 'P1', 'P2', 'P3', 'WATCH', 'PAUSED']   # DREAM above P1 (Tim 2026-10-19, REV-040)
cadence = {'DREAM': 'every discovery run, first', 'P1': 'every discovery run', 'P2': 'at least daily', 'P3': 'rotating weekly coverage', 'WATCH': 'opportunistic', 'PAUSED': 'no targeted search'}
groups = {k: [] for k in order}; seen = set(); bad = 0
for line in m.group(1).splitlines():
    x = re.match(r'^TARGET_COMPANY=(\{.*\})\s*$', line)
    if not x: continue
    try: c = json.loads(x.group(1))
    except ValueError: bad += 1; continue
    name = str(c.get('company', '')).strip(); key = name.lower()
    if not name or key in seen: continue
    seen.add(key)
    p = str(c.get('priority', '')).strip().upper(); p = p if p in groups else 'WATCH'
    locs = '; '.join(c.get('locations') or [])
    groups[p].append(f"{name} | careers: {c.get('careers_url') or 'UNKNOWN'} | {locs}")
lines = ['TARGET COMPANIES PRIORITY DIGEST (generated from canonical rules; do not edit, edit the registry in the Pipeline Explorer)',
         f'SOURCE=tpruittguitar/forge-policy/{rules}' + (f' @ {sha}' if sha else ''),
         f'COMPANIES={len(seen)}' + (f' UNPARSEABLE_LINES={bad}' if bad else ''),
         'Priority sets discovery intensity and the culture score only. It never overrides pay, geography, FLEX, scope/fit, Never-Consider, protected states or dedupe.']
for p in order:
    lines.append('')
    lines.append(f'{p} ({cadence[p]}): {len(groups[p])}')
    lines.extend('- ' + g for g in groups[p])
lines.append('END TARGET COMPANIES PRIORITY DIGEST')
open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(f'{out}: {len(seen)} companies, ' + ', '.join(f'{p} {len(groups[p])}' for p in order))
