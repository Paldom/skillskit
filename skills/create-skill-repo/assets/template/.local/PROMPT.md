/goal Build production-quality Agent Skills in this repository until `make check` passes with zero errors and every skill meets the Definition of Done. Work autonomously; use the bundled add-skill skill for each skill. NEVER run git commit or git push - leave every change in the working tree for me to review and commit.

Idea / scope: {{IDEA}}

Method:
1. Read ALL of `.local/` recursively (every subfolder/file is source material) and docs/skill-authoring.md + docs/evals.md before writing anything.
2. Research beyond `.local/`: web-search for current facts, official docs, prior art; verify every load-bearing claim against primary sources. Cleaned, verified findings go into each skill's references/ (never cite `.local/` paths).
3. Split the idea into single-purpose skills (one folder each under skills/); if a skill needs "and" to describe, split it. Cross-validate the split and any contested/high-stakes topics (APIs, schemas, security claims) with /cross BEFORE writing bodies.
4. Per skill, eval-first via add-skill: write evals/evals.json (>=8 should-trigger, >=8 should-not-trigger, 3-5 quality cases) BEFORE the SKILL.md body; then draft SKILL.md per docs/skill-authoring.md; then `make check` and fix everything.
5. Cross-validate every skill with /cross (concept, description, body) once its evals + draft exist; fix or reject-with-evidence each finding, re-run `make check`. If /cross is unavailable, note that per skill.
6. Descriptions: single line, third person, triggers + "Not for ..." exclusion, 150-400 chars, disjoint across skills (no trigger theft).
7. Deterministic steps go to scripts/ (non-zero exit on failure; reference them via ${CLAUDE_SKILL_DIR}); long material to references/ (one level deep, TOC if >100 lines). SKILL.md under 500 lines.
8. After each skill: update the README catalog table, CHANGELOG.md, and its skills.sh.json grouping (every skill in exactly one group; engaging one-sentence group descriptions - that file is the skills.sh listing copy).
9. If the skills compose into a workflow, author docs/setup-prompt.md: a paste-ready /goal (max 4000 chars) orchestrating them - ordering constraints, parallel agents only on disjoint file surfaces, per-skill verifier gates, verification bracketing, no git actions (the owner commits). Fact-check its commands against the shipped skills; link it from the README.

Definition of Done:
- `make check` exits 0 with no errors (warnings triaged or fixed)
- every skill has evals and a single-line, disjoint description
- every skill /cross-validated (findings dispositioned) or absence noted; contested topics researched + validated before authoring
- README catalog, CHANGELOG, skills.sh.json current and consistent; no template placeholder tokens remain
- multi-skill repos ship docs/setup-prompt.md linked from the README
- a triggering self-test (description-only routing vs the full catalog) was performed per skill and reported in your final summary
- zero git commits/pushes were made; the final summary lists exactly what changed for my review
