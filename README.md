# forge-policy

Standing Forge policy: rules, geo floors, scoring model, FLEX classes, salary estimation, Never-Consider list. Public by Tim's decision (2026-10-12).
Live policy source from 2026-10-17 (Stage 3 of `FORGE_PLAN_GitHub_Migration_2026-10-12.txt`, Tim 2026-10-17). The Writer and Pipeline Explorer read and save policy here; the Drive copies are superseded. See `MANIFEST.txt` for the copy record.

## Files
| Path | What it is | Read by |
|---|---|---|
| `rules/TIM_PIPELINE_RULES_CANONICAL.txt` | Canonical pipeline rules: core, URL, discovery, Never-Consider, compensation and geo floors, degree/FLEX, ownership, title, states, decline codes, protected states, Writer and reporting rules, and the Target Companies registry (`SECTION=TARGET_COMPANIES`) | Writer (intake, FLEX, Never-Consider), Pipeline Explorer (Rules and Target Companies screens, culture score), every AI lane |
| `scoring/PIPELINE_SCORING_MODEL.json` | Published weighted job rating model (weights, geo control points, salary curve) | Writer, Pipeline Explorer, AI lanes |
| `directives/WRITER_ACCESS_DIRECTIVE_V9_2026-10-02.txt` | How AI lanes reach the Writer | AI lanes |

Edit the rules and Target Companies through the Pipeline Explorer when possible: its save re-reads the file, passes the blob SHA (a concurrent change is refused, never overwritten), commits with a `TIM` message and reads the result back.

## Change rules
- Claude commits to `main` with messages starting `CLAUDE`; Tim's own commits start `TIM`.
- Grok or ChatGPT covering for Claude: commit to a branch `backup/<provider>-<YYYYMMDD-HHMM>` and open a pull request. Tim merges in the GitHub web UI.
- The `unreviewed-push-alarm` Action opens an issue (GitHub emails Tim) for any push to `main` whose commits are not labeled `CLAUDE` or `TIM` and are not a web merge. It detects; it does not block.
