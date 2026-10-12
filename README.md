# forge-policy

Standing Forge policy: rules, geo floors, scoring model, FLEX classes, salary estimation, Never-Consider list. Public by Tim's decision (2026-10-12).
Empty until Stage 3 of `FORGE_PLAN_GitHub_Migration_2026-10-12.txt`: the Writer and Pipeline Explorer must read policy from here before any file moves. Until then, the Drive copies remain live.

## Change rules
- Claude commits to `main` with messages starting `CLAUDE`; Tim's own commits start `TIM`.
- Grok or ChatGPT covering for Claude: commit to a branch `backup/<provider>-<YYYYMMDD-HHMM>` and open a pull request. Tim merges in the GitHub web UI.
- The `unreviewed-push-alarm` Action opens an issue (GitHub emails Tim) for any push to `main` whose commits are not labeled `CLAUDE` or `TIM` and are not a web merge. It detects; it does not block.
