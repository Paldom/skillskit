# Skill Evals

Skills are software: prompts are inputs, agent behavior is output, the description
is the routing layer. Test all three — **before** writing the skill body. If you
cannot write the eval cases, the scope isn't understood yet; that's a brief problem,
not a skill problem.

## evals.json format

`skills/<name>/evals/evals.json` (validated by `scripts/validate_skills.py`):

```json
{
  "skill": "example-skill",
  "cases": [
    { "type": "should_trigger", "prompt": "write tests for utils.py" },
    { "type": "should_trigger", "prompt": "can u add test coverage here" },
    { "type": "should_not_trigger", "prompt": "why is this test failing?" },
    { "type": "should_not_trigger", "prompt": "delete the flaky tests" },
    {
      "type": "quality",
      "prompt": "add tests for the parser module",
      "expected_behavior": [
        "creates a test file next to existing tests following repo conventions",
        "covers at least the happy path and one edge case per public function",
        "runs the new tests and reports the result"
      ]
    }
  ]
}
```

- **≥ 8 `should_trigger`**: vary formality, typos, terseness, explicitness — include
  at least two prompts that never name the skill.
- **≥ 8 `should_not_trigger`**: near-misses that share keywords but belong elsewhere
  (adjacent skills, native model competence). These catch over-triggering, which
  taxes every unrelated request.
- **3–5 `quality` cases**: 1 canonical, variations, 1–2 edge cases. Give each
  2–4 assertions that are plain-language but *checkable* — files created,
  commands run, exclusions respected — not exact output text and not vibes
  ("is helpful"); vague assertions turn any grader into a coin flip.

## Automated harness (official skill-creator)

If the official `skill-creator` skill is installed (plugin
`skill-creator:skill-creator` from Anthropic's marketplace), prefer it for
measurement: invoke it as a subskill via the Skill tool. It runs each quality
case as parallel subagents — one with the skill, one baseline — grades the
assertions, aggregates pass rate / time / tokens (mean ± stddev), and opens an
HTML review viewer; its description-optimization loop tests real triggering via
`claude -p` (3 runs per query, 60/40 train/test split, up to 5 iterations,
best description picked on held-out score).

This repo's `evals/evals.json` stays the source of truth; translate cases into
the harness's formats inside its `<name>-workspace/` (never rewrite the
committed file):

- `quality` cases → its `evals.json`: `{"skill_name": …, "evals": [{"id",
  "prompt", "expected_output", "files"}]}`, with each `expected_behavior` item
  becoming an assertion.
- `should_trigger` / `should_not_trigger` cases → its trigger eval set:
  `[{"query": "<prompt>", "should_trigger": true|false}]`.

Guardrails for the delegation (the harness is an external, unpinned skill —
treat its interface as a moving target and its numbers as untrusted until
checked):

- **Scope the invocation**: measure only — it writes solely to the sibling
  `<name>-workspace/` (never committed) and must not edit the skill itself;
  this repo's validator stays the final authority on anything applied back.
- **Trust but verify the numbers**: confirm it actually ran every translated
  case (cases-run == cases-sent) before believing a pass rate — silent schema
  drift can drop cases and report a clean 100%. Read at least a couple of run
  transcripts, not just the scores.
- **Description optimizer is opt-in** (it burns `claude -p` × 3 runs × queries
  × up to 5 iterations) and its held-out score only *ranks proposals*. The
  acceptance gate is ours: any `best_description` must pass the full committed
  case set — the near-miss negatives especially — plus this repo's rules
  (single physical line, "Not for …" kept) and the validator, or it's rejected
  and the previous description stays.
- **Keep a record**: note the date, plugin version, and pass rates with the
  results (workspace summary or CHANGELOG) so the next "improve triggering of
  X" has a before/after instead of anecdotes.

## Manual trigger protocol (fallback)

When the harness isn't installed, probe by hand (activation is stochastic);
the working protocol:

1. **Fresh session per probe** — `claude` in a clean context; prior turns contaminate
   routing. Paste the case prompt verbatim.
2. Ask "Which skill did you use?" afterwards — simple tasks may be solved without
   consulting any skill, which is a routing miss that looks like a pass.
3. Score: aim **≥ 80% activation** on should-trigger, **≤ 5% false positives** on
   should-not. Run flaky cases 3× before concluding anything — single runs lie.
4. Fix order: **trigger failures → quality failures → edge cases.**
   - Under-triggering → broaden verbs/nouns, add terse phrasings, be pushier.
   - Over-triggering → add a "Not for …" exclusion built from the actual
     false-positive prompts' overlapping words (don't delete positive triggers).
   - Don't paste failed queries verbatim into the description (overfitting).
5. Re-run the suite after any description edit, when adding sibling skills (trigger
   theft), and after model upgrades.

## Quality evals

Prefer the automated harness above — its baseline comparison is exactly this,
measured. Manually: run each quality case in a fresh session with the skill
installed; check every `expected_behavior` assertion. For subjective outputs,
have a *different* session (or model) grade against the assertions —
self-evaluation is near random. Compare against a no-skill baseline once: a
skill whose output matches baseline is context tax and should be deleted.
