<!-- Icon goes here, first thing on the page. Generate it with the
     icon-designer-skills pipeline (/icon-brief -> /icon-draw -> /icon-critique,
     you pick), save the master to assets/icon.svg, then replace this comment:

<p align="center">
  <img src="assets/icon.svg" alt="{{REPO_NAME}} icon" width="128"/>
</p>
-->

# {{REPO_TITLE}}

[![CI](https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{GITHUB_OWNER}}/{{REPO_NAME}}/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/{{GITHUB_OWNER}}/{{REPO_NAME}})](https://skills.sh/{{GITHUB_OWNER}}/{{REPO_NAME}})

{{REPO_DESCRIPTION}}

## Demo

<!-- Proof before prose — the thing that converts a visitor.
     Terminal work: /tape-demo (github.com/Paldom/terminaltor) writes a .tape you
     commit next to the GIF, so the demo regenerates instead of rotting.
     Anything with a browser: /walkthrough-storyboard then /walkthrough-record
     (github.com/Paldom/screenshooter).
     Commit the source and the render; caption what the reader is looking at. -->

## Quick start

```bash
npx skills add {{GITHUB_OWNER}}/{{REPO_NAME}}
```

Then talk to your agent — describe the task and the skill activates on its
description, or invoke it by name:

```text
/<skill-name> <what you want>
```

Every example in this README is something a *user* types: an install command, a
`/skill-name` invocation, or the plain-English ask a skill triggers on. Never a
script that lives inside a skill.

### Other ways to install

```bash
npx skills add {{GITHUB_OWNER}}/{{REPO_NAME}} -a codex -a pi   # target specific agents
gh skill install {{GITHUB_OWNER}}/{{REPO_NAME}}                # GitHub CLI >= 2.90
gh skill install {{GITHUB_OWNER}}/{{REPO_NAME}} <skill> --pin <tag>
```

```text
/plugin marketplace add {{GITHUB_OWNER}}/{{REPO_NAME}}
/plugin install {{REPO_NAME}}@{{REPO_NAME}}
```

## Skills

| Skill | Ask it when | Invoke |
| --- | --- | --- |
| _none yet_ | Skills are added via the workflow in [CONTRIBUTING.md](CONTRIBUTING.md). | |

## Repository structure

```
skills/                  # distributed skills, one folder per skill (SKILL.md + evals/ + scripts/)
docs/                    # authoring guide, eval methodology, README standard, deployment
scripts/                 # the gate: validator, eval scorer, self-checks
skills.sh.json           # skills.sh repo-page customization (groupings)
.claude/                 # agentic dev setup: hooks + bundled add-skill / publish-repo skills
.claude-plugin/          # plugin + marketplace manifests (makes this repo installable)
.local/                  # gitignored working area: sources, research, PROMPT.md
```

## Working on this repo with an agent

This repo is agent-native: canonical agent instructions live in
[AGENTS.md](AGENTS.md) (CLAUDE.md imports it), hooks validate and lint every write,
`make check` runs the full gate, and CI enforces the same on every PR. The bundled
`add-skill` skill walks the eval-first authoring workflow in
[docs/skill-authoring.md](docs/skill-authoring.md); the README shape is
[docs/readme-standard.md](docs/readme-standard.md). `make hooks` installs the
commit-time layer. Maintainers drive sessions with their own gitignored
`.local/PROMPT.md`.

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the skill-proposal
process, the authoring workflow, and the PR checklist. Please note the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Support

Questions, ideas, or something not working? Start with [SUPPORT.md](SUPPORT.md) —
bugs and skill proposals have [issue templates](../../issues/new/choose), and
security concerns go through [SECURITY.md](SECURITY.md) (never a public issue).

## License

[MIT](LICENSE) © {{YEAR}} {{GITHUB_OWNER}}

<!-- attribution:start -->
---

[![Built with skillskit](https://img.shields.io/badge/built%20with-skillskit-F5A623)](https://github.com/Paldom/skillskit)

Scaffolded with [skillskit](https://github.com/Paldom/skillskit) — eval-first Agent
Skills tooling. This line is yours to delete; nothing checks for it.
<!-- attribution:end -->
