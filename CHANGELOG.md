# Changelog

All notable changes to this repository's skills are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org) on the plugin manifest
(breaking skill-interface change → major, new skill → minor, fix → patch).

## [Unreleased]

### Added

- Codex support in-checkout: `.agents/skills/` symlinks expose the four
  skills (skill-from-research, add-skill, create-skill-repo, publish-repo)
  to Codex and other Agent-Skills-standard agents when working inside this
  repo — verified live with `codex exec`; skills.sh installs remain the
  distribution path.

- `skill-from-research` now documents the researchkit pack shape in
  `references/research-pack.md` (report.md as synthesis, materials
  frontmatter as citable primary sources, index.json fetched-only rule,
  result.json run-complete gate, subprojects recursion) — pinned to
  researchkit's `docs/research-pack.md` v1 contract.

### Added
- Initial skillskit release: create-skill-repo, add-skill, publish-repo, skill-from-research.

### Changed
- seed/verify install commands (publish-repo + deploying docs, root + template): dropped `--skill '*'` — the wildcard deliberately opts into internal skills; plain `add` is the consumer-faithful install.
- bundled dev skills (template add-skill/publish-repo): marked `metadata.internal: true` so skills.sh consumer installs skip them (CLI honors it; maintainers opt in with INSTALL_INTERNAL_SKILLS=1 or --include-internal); publish-repo pre-flight now asserts they stay out of `add . --list`.
- publish-repo and deploying docs (root + template): document skills.sh burst throttling — when publishing several repos, seed one at a time ~5 minutes apart (burst install events from one machine are throttled server-side; audit runs, listing never materializes).
- publish-repo (and the template's bundled copy): seamless-deploy fixes learned from a live deployment — seed installs must run with `env -u DISABLE_TELEMETRY -u DO_NOT_TRACK` (any value disables the install report, even `0`), pin `npx skills@latest` against stale npx caches, `gh` < 2.90 fallback for the release step (`gh release create` + topics), concrete listing verification (canonical page URL within minutes; badge 200 proves nothing; 404 >15 min = suppressed telemetry, not cache), and a note that agent harnesses may permission-block public-surface commands.
- validate_skills.py (root + template): validates `skills.sh.json` against the live skills.sh schema — required `groupings` with `title`/`skills`, unknown-key rejection with `groups`→`groupings`/`name`→`title` hints, size limits, cross-checks that every distributed skill sits in exactly one grouping and every reference exists.
- add-skill (root + template) and docs/deploying.md (root + template): document the exact `skills.sh.json` schema shape and the telemetry/gh-version/npx-cache gotchas in the deploy path and troubleshooting table.
- add-skill: new Measure step — delegates quality-eval runs, baseline benchmarking, and description optimization to Anthropic's official skill-creator skill (`skill-creator:skill-creator`) as a subskill when installed; the manual protocol in `references/evals.md` remains the fallback.
