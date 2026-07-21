<p align="center">
  <img src="assets/icon.svg" alt="skillskit icon" width="128"/>
</p>

# skillskit

[![CI](https://github.com/Paldom/skillskit/actions/workflows/ci.yml/badge.svg)](https://github.com/Paldom/skillskit/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-green)
[![skills.sh](https://skills.sh/b/Paldom/skillskit)](https://skills.sh/Paldom/skillskit)

From context to installable agent skills: research packs in, validated
skills.sh-ready skills out — scaffolding, eval-first authoring, validation, and
deployment included.

```mermaid
flowchart LR
    T(["💡 any topic"]) --> RK["🔍 <b>researchkit</b><br/>12 AI search providers in parallel:<br/>one cited report + archived sources"]
    RK -- "one-shot:<br/>teach every agent" --> SK["⚡ <b>skillskit</b><br/>research pack in, validated skill out —<br/>installable in 70+ agents via skills.sh"]
    RK -- "compounding:<br/>grow a memory" --> BK["🧠 <b>brainkit</b><br/>portable hybrid brain (OKF wiki + retrieval ladder),<br/>cited answers for agents and harnesses"]
    classDef here stroke:#f97316,stroke-width:3px;
    class SK here
```

**The one-shot path.** [researchkit](https://github.com/Paldom/researchkit) does the digging; skillskit turns the pack into a skill you install once and reuse in every agent. Prefer compounding memory over a packaged skill? Grow a brain with [brainkit](https://github.com/Paldom/brainkit).

```
research pack ──▶ /skill-from-research ──▶ validated skills ──▶ /publish-repo ──▶ skills.sh
                        │
                        └─▶ /create-skill-repo (when a new repo is needed)
```

## Quick start

Install with the [skills CLI](https://skills.sh) — auto-detects 70+ agents
(Claude Code, Codex, Cursor, Copilot, pi, …):

```bash
npx skills add Paldom/skillskit                  # all detected agents
npx skills add Paldom/skillskit -a codex -a pi   # or target specific agents
```

Or with the [GitHub CLI](https://cli.github.com/manual/gh_skill_install) (≥ 2.90):

```bash
gh skill install Paldom/skillskit
```

Or as a Claude Code plugin:

```
/plugin marketplace add Paldom/skillskit
/plugin install skillskit@skillskit
```

Then drop your research into a folder and say **"turn this research pack into a
skill"** — or invoke any skill directly with `/<skill-name>`.

Working inside this checkout? Codex and other Agent-Skills-standard agents
discover the same four skills via the repo's `.agents/skills/` — no install
needed.

## Skills

| Skill | Description |
| --- | --- |
| [skill-from-research](skills/skill-from-research/) | Turns a research pack (reports, notes, transcripts) into installable skills — inventories the pack, verifies claims against primary sources, authors each skill eval-first. |
| [create-skill-repo](skills/create-skill-repo/) | Scaffolds a complete standalone skills repository — GitHub repo, OSS hygiene, CI with a skills.sh consumer job, validation hooks, distribution manifests; the scaffold overlay stays uncommitted for your review. |
| [add-skill](skills/add-skill/) | Authors or improves a single skill in any repository via the eval-first workflow — trigger evals before the body, validated before done; benchmarks via the official skill-creator harness when installed. |
| [publish-repo](skills/publish-repo/) | Publishes a skills repository to skills.sh deliberately — pre-flight gates, visibility flip, protections, a versioned `gh skill` release, and consumer-style verification. |

## The flow

1. **Research** — gather everything about your topic into a pack (deep-research
   reports, notes, transcripts, examples). See
   [what makes a good pack](skills/skill-from-research/references/research-pack.md).
2. **Distill** — `/skill-from-research <path>`: the pack is inventoried, read in
   full, and verified against primary sources; each finding becomes an
   eval-first, single-purpose skill (a new repo is scaffolded via
   `/create-skill-repo` when needed).
3. **Review** — everything stays uncommitted in your working tree; you review,
   commit, and push.
4. **Ship** — `/publish-repo` walks the deliberate path to the skills.sh
   catalogue: gates, visibility, protections, release, verification.

Full walkthrough: [docs/guide.md](docs/guide.md).

## Repository structure

```
skills/                        # the four distributed skills (this is what installs)
  create-skill-repo/assets/template/   # the complete repo scaffold, shipped inside the skill
docs/                          # flow guide, authoring rulebook, eval methodology, deploying
scripts/                       # deterministic validator (shared by hooks and CI)
.claude/                       # dogfood: hooks that validate every SKILL.md write here
.claude-plugin/                # plugin + marketplace manifests
skills.sh.json                 # skills.sh repo-page groupings
```

## Working on this repo with an agent

This repo is agent-native and dogfoods its own rules: canonical agent
instructions live in [AGENTS.md](AGENTS.md) (CLAUDE.md imports it), hooks
validate every `SKILL.md` on write, `make check` runs the full validator, and CI
enforces the same gate plus a real `npx skills` consumer install on every PR.

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the
skill-proposal process and the eval-first authoring workflow. Please note the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Support

Questions, ideas, or something not working? Start with [SUPPORT.md](SUPPORT.md) —
bugs and skill proposals have [issue templates](../../issues/new/choose), and
security concerns go through [SECURITY.md](SECURITY.md) (never a public issue).

## License

[MIT](LICENSE) © 2026 Domonkos PAL
